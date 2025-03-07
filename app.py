import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, Response
from sqlalchemy.orm import Session
import requests
from webscraper import get_subheaders
from models import Recipe, Image
from database import SessionLocal
import io
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pandas as pd
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


# Check if the app is running locally or on Render
environment = os.getenv('ENVIRONMENT', 'local')  # Default to 'local' if ENVIRONMENT is not set

# Load the database URL based on the environment
DATABASE_URL = os.getenv('DATABASE_URL')  # Both local and Render should provide this variable

# Optional: You can log or print the environment for debugging purposes
print(f"App is running in {environment} mode.")

# Ensure the DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please set it in the environment variables.")

# Create the engine instance
engine = create_engine(DATABASE_URL)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize rate limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])


def clean_subheader(title):
    """Cleans subheader text by removing unwanted characters."""
    return title.replace('“', '').replace('”', '').replace('(', '').replace(')', '').strip()


@app.route('/')
@limiter.limit("100 per minute")  # Limit homepage requests
def home():
    logging.debug('Home page is loading...')
    session = SessionLocal()
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 5
        offset = (page - 1) * per_page

        # Include the recipe_id in the query
        recipes = session.query(Recipe.id, Recipe.recipe_title, Recipe.recipe_content)\
                        .order_by(Recipe.id)\
                        .offset(offset).limit(per_page).all()
        
        # Now recipes will have (id, title, content)
        cleaned_recipes = [(clean_subheader(title), content, recipe_id) for recipe_id, title, content in recipes]

        total_recipes = session.query(Recipe).count()
        total_pages = (total_recipes + per_page - 1) // per_page

        return render_template('index.html', recipes=cleaned_recipes, page=page, total_pages=total_pages)

    except Exception as e:
        logging.error(f"Error in home route: {e}")
        return render_template('error.html')

    finally:
        session.close()



@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])  # Return empty JSON if no query

    per_page = 5 # pagination settings 

    with SessionLocal() as session:
        indexed_recipes = session.query(Recipe.id, Recipe.recipe_title, Recipe.recipe_content).order_by(Recipe.id).all()

        recipe_index_map = {recipe.id: i for i, recipe in enumerate(indexed_recipes)}

        results = session.query(Recipe).filter(Recipe.search_vector.match(query)).all()
    
        paginated_results = []
        for recipe in results:
            index = recipe_index_map.get(recipe.id, -1)
            if index != -1:
                page = (index // per_page) +1 
                paginated_results.append({
                    "title": recipe.recipe_title,
                    "description": recipe.recipe_content,
                    "page": page
                })
    return jsonify(paginated_results)

@app.route('/double_filter_search', methods=['GET'])
def double_filter_search():
    # Get flavor profile and meat type from request args
    flavor_profile = request.args.get('flavor_profile', '')
    meat_type = request.args.get('meat_type', '')
    query = request.args.get('q', '').strip() 

    per_page = 5

    try:
        with SessionLocal() as session:
            # Start building the query
            query_db = session.query(Recipe.id, Recipe.recipe_title, Recipe.recipe_content).order_by(Recipe.id)
            
            # Apply filters
            if flavor_profile:
                query_db = query_db.filter(Recipe.recipe_content.ilike(f'%{flavor_profile}%'))
            if meat_type:
                query_db = query_db.filter(Recipe.recipe_content.ilike(f'%{meat_type}%'))
            if query:
                query_db = query_db.filter(Recipe.search_vector.match(query))

            # Fetch the filtered results
            indexed_recipes = query_db.all()

            # Paginate results
            page = int(request.args.get('page', 1))  # Default to page 1
            start_index = (page - 1) * per_page
            end_index = start_index + per_page

            paginated_results = indexed_recipes[start_index:end_index]

            # Prepare the response data
            results = []
            for recipe in paginated_results:
                index = indexed_recipes.index(recipe)
                page_number = (index // per_page) + 1  # Calculate the page number for each recipe
                results.append({
                    "id": recipe.id, 
                    "title": recipe.recipe_title,
                    "description": recipe.recipe_content,
                    "page": page_number
                })

            # Total pages based on the number of results
            total_pages = (len(indexed_recipes) + per_page - 1) // per_page

            return jsonify({
                "results": results,
                "total_pages": total_pages,
                "current_page": page
            })

    except Exception as e:
        logging.error(f"Error in double filter search route: {e}")
        return jsonify({'error': 'An error occurred while processing the search.'})




# TESTING BACKEND DATABASE CALLS
# @app.route('/api/recipes', methods=['GET'])
# @limiter.limit("10 per minute")  # Limit API calls
# def get_all_recipes():
#     with SessionLocal() as session:
#         recipes = session.query(Recipe).all()
#         if not recipes:
#             return jsonify({"message": "No recipes found"}), 404

#         recipes_data = [
#             {
#                 "id": recipe.id,
#                 "title": recipe.recipe_title,
#                 "content": recipe.recipe_content,
#                 "video_id": recipe.video_id,
#                 "video_url": recipe.video_url
#             }
#             for recipe in recipes
#         ]

#         return jsonify(recipes_data)

# @app.route('/api/images', methods=['GET'])
# @limiter.limit("10 per minute")  # Limit API calls
# def get_all_images():
#     with SessionLocal() as session:
#         images = session.query(Image).all()
#         if not images:
#             return jsonify({"message": "No images found"}), 404

#         images_data = [
#             {
#                 "id": image.id,
#                 "filename": image.filename,
#                 "recipe_id": image.recipe_id
#             }
#             for image in images
#         ]

#         return jsonify(images_data)


@app.route('/video_data/<string:title>', methods=['GET'])
@limiter.limit("10 per minute")  # Limit YouTube API calls
def get_video_data(title):
    with SessionLocal() as session:
        recipe = session.query(Recipe).filter(Recipe.recipe_title == title).first()
        if recipe and recipe.video_id:
            return jsonify({
                "video_id": recipe.video_id,
                "video_url": recipe.video_url,
                "video_title": recipe.video_title,
                "video_metadata": recipe.video_metadata
            })

        return jsonify({"error": "Recipe not found"}), 404


@app.route("/upload_image", methods=["POST"])
@limiter.limit("3 per minute")  # Limit image uploads
def upload_image():
    file = request.files.get("file")
    recipe_id = request.form.get("recipe_id")

    if not file or not recipe_id:
        return "File or recipe ID not provided", 400

    try:
        image_data = file.read()
        filename = file.filename
        
        with SessionLocal() as session:
            recipe = session.query(Recipe).filter(Recipe.id == int(recipe_id)).first()
            if not recipe:
                return f"No recipe found with ID {recipe_id}", 404

            new_image = Image(
                filename=filename,
                image_data=image_data,
                recipe_id=recipe.id
            )
            session.add(new_image)
            session.commit()

        return render_template('success.html', name=filename)

    except Exception as e:
        logging.error(f"Error uploading image: {e}")
        return f"An error occurred: {e}", 500


@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    session = SessionLocal()
    try:
        recipe = session.query(Recipe).get(recipe_id)
        if not recipe:
            flash("Recipe not found", "error")
            return redirect(url_for('home'))  
        
        if request.method == 'POST':
            new_title = request.form['title']
            new_content = request.form['content']
            recipe.recipe_title = new_title
            recipe.recipe_content = new_content
            session.commit()
            flash("Recipe updated successfully!", "success")
            return redirect(url_for('home'))

        return render_template('edit_recipe.html', recipe=recipe)

    except Exception as e:
        logging.error(f"Error in edit route: {e}")
        flash("An error occurred while editing the recipe", "error")
        return render_template('error.html')

    finally:
        session.close()


@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    session = SessionLocal()
    try:
        recipe = session.query(Recipe).get(recipe_id)
        if not recipe:
            flash("Recipe not found", "error")
            return redirect(url_for('home'))  

        session.delete(recipe)
        session.commit()
        flash("Recipe deleted successfully!", "success")
        return redirect(url_for('home'))

    except Exception as e:
        logging.error(f"Error in delete route: {e}")
        flash("An error occurred while deleting the recipe", "error")
        return render_template('error.html')

    finally:
        session.close()


@app.route("/export_csv")
def export_csv():
    try:
        query = "SELECT id, recipe_title, recipe_content, video_id, video_url, video_title, video_metadata FROM recipe"
        df = pd.read_sql(query, engine)  # Load data into DataFrame

        if df.empty:
            logging.warning("Attempted CSV export, but the recipe table is empty.")
            return render_template("error.html", message="No recipes found to export."), 404

        csv_data = df.to_csv(index=False)  # Convert to CSV format
        response = Response(csv_data, mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=recipe_export.csv"

        return response

    except Exception as e:
        logging.error(f"Error exporting CSV: {e}", exc_info=True)
        return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)


# custom error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {e}")
    return render_template('error.html', error_message=str(e)), 500

# Handle rate limit errors
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({"error": "Too many requests, slow down"}), 429

if __name__ == '__main__':
    app.run(debug=True)

