# app.py

import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from repository import JSONRepository
from service import RecipeService

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"

app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

repo = JSONRepository("data/recipes.json")
service = RecipeService(repo)


@app.route("/")
def index():
    """
    Главная страница: показывает рецепты + выпадающий список
    категорий (включая «Все»).
    """
    # 1) Получаем все рецепты
    all_recipes = service.get_all_recipes()

    # 2) Собираем список уникальных категорий
    all_categories = sorted({r.category for r in all_recipes})

    # 3) Считываем GET-параметр ?category=... (или пусто)
    cat = request.args.get("category", "").strip()

    # 4) Если указана категория и не пустая, фильтруем:
    if cat:
        recipes = [r for r in all_recipes if r.category.lower() == cat.lower()]
    else:
        # Иначе все
        recipes = all_recipes

    # 5) Передаём recipes, all_categories, selected_cat в шаблон
    return render_template("index.html",
                           recipes=recipes,
                           all_categories=all_categories,
                           selected_cat=cat)


@app.route("/recipes/<int:recipe_id>")
def view_recipe(recipe_id):
    """Просмотр одного рецепта (read-only)."""
    try:
        recipe = service.get_recipe_by_id(recipe_id)
        return render_template("view.html", recipe=recipe)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("index"))


# ----------------------------
# 1) Добавление (через JSON-метод ингредиентов)
# ----------------------------
@app.route("/recipes/new", methods=["GET", "POST"])
def new_recipe():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        steps = request.form.get("steps", "").strip()

        ingredients_json = request.form.get("ingredients_json", "[]")
        try:
            ingredients_data = json.loads(ingredients_json)
        except json.JSONDecodeError:
            ingredients_data = []

        # Загрузка картинки (если есть)
        image_file = request.files.get("image")
        image_url = ""
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(filepath)
            image_url = f"/static/uploads/{filename}"

        new_r = service.add_recipe(name, category, ingredients_data, steps, image_url)
        flash(f"Рецепт '{new_r.name}' (ID={new_r.id}) создан.")
        return redirect(url_for("index"))
    else:
        # GET -> показать форму
        return render_template("new.html")


# ----------------------------
# 2) Редактирование (JSON-метод ингредиентов)
# ----------------------------
@app.route("/recipes/<int:recipe_id>/edit", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    try:
        recipe = service.get_recipe_by_id(recipe_id)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        steps = request.form.get("steps", "").strip()

        # Получаем JSON-строку ингредиентов
        ingredients_json = request.form.get("ingredients_json", "[]")
        try:
            ingredients_data = json.loads(ingredients_json)
        except json.JSONDecodeError:
            ingredients_data = []

        # Если загружаем новую картинку
        image_file = request.files.get("image")
        new_image_url = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(filepath)
            new_image_url = f"/static/uploads/{filename}"

        try:
            updated = service.edit_recipe(
                recipe_id,
                name,
                category,
                ingredients_data,
                steps,
                new_image_url=new_image_url
            )
            flash(f"Рецепт (ID={updated.id}) обновлён.")
        except ValueError as ex:
            flash(str(ex))

        return redirect(url_for("index"))
    else:
        return render_template("edit.html", recipe=recipe)


@app.route("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    success = service.delete_recipe(recipe_id)
    if success:
        flash(f"Рецепт (ID={recipe_id}) удалён.")
    else:
        flash("Рецепт не найден.")
    return redirect(url_for("index"))


# ----------------------------
# 3) Масштабирование (временно)
# ----------------------------
@app.route("/recipes/<int:recipe_id>/scale", methods=["POST"])
def scale_recipe_temporarily(recipe_id):
    factor_str = request.form.get("factor", "1.0")
    try:
        factor = float(factor_str)
        scaled = service.scale_recipe_temporarily(recipe_id, factor)
        flash(f"Масштаб x{factor}, изменения не сохранены.")
        return render_template("scaled_view.html", recipe=scaled, factor=factor)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("index"))


# ----------------------------
# 4) Поиск (динамические категории)
# ----------------------------
@app.route("/search", methods=["GET", "POST"])
def search():
    results = None
    all_recipes = service.get_all_recipes()
    all_categories = sorted({r.category for r in all_recipes})

    if request.method == "POST":
        q_name = request.form.get("name", "").strip()
        q_ing = request.form.get("ingredient", "").strip()
        q_cat = request.form.get("category", "").strip()

        found_list = []
        if q_name:
            found_list.extend(service.find_by_name(q_name))
        if q_ing:
            found_list.extend(service.find_by_ingredient(q_ing))
        if q_cat:
            found_list.extend(service.filter_by_category(q_cat))

        unique_map = {}
        for r in found_list:
            unique_map[r.id] = r
        results = list(unique_map.values())

    return render_template("search.html",
                           results=results,
                           all_categories=all_categories)


if __name__ == "__main__":
    app.run(debug=True)
