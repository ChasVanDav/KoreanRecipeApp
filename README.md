# 🍜 Korean Recipe App

This is a Flask-based web application where users can **browse, search, and manage Korean recipes**. The app scrapes **Korean recipe titles** from a CNN article and automatically fetches the related **YouTube cooking video** with the highest views. Users can **upload images, edit, delete, and export recipe data**, making it a comprehensive tool for discovering and organizing Korean dishes.

### What Users Can Do

- Explore a curated list of Korean recipes automatically gathered from a trusted source.
- Watch the most relevant YouTube cooking video for each recipe directly from the app.
- Search and filter through the recipes using keywords.
- Upload their own images for recipes.
- Edit or delete existing recipes to keep their collection up-to-date.
- Export their saved recipe data for offline use or sharing.
- Enjoy a smooth and efficient experience thanks to rate-limiting features that optimize performance.

![alt text](static/images/screenshot1.png)
![alt text](static/images/screenshot2.png)
![alt text](static/images/screenshot3.png)
![alt text](static/images/screenshot4.png)

## 🎯 Features

- 🔍 **Web Scraping**: Extracts Korean recipe titles from a CNN article.
- 🎧 **YouTube API Integration**: Fetches relevant cooking videos based on the recipe title.
- 🏢 **PostgreSQL Database**: Stores scraped data and YouTube metadata.
- 🎨 **Image Upload**: Allows users to upload images for recipes.
- ✏️ **Edit & Delete Recipes**: Modify or remove saved recipes.
- 📌 **Pagination & Search**: Easily browse and find recipes.
- ⏳ **Rate Limiting**: Prevents excessive API requests and ensures smooth performance.
- 📂 **Data Import/Export**: Supports bulk data operations.

---

## 🚀 Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Database:** PostgreSQL
- **API Integration:** YouTube Data API v3
- **Other:** Python-dotenv for environment variables

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/ChasVanDav/KoreanRecipeApp.git
cd KoreanRecipeApp
```

### 2. Create a Virtual Environment & Install Dependencies

```sh
python -m venv venv
# Activate virtual environment:
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add:

```
YOUTUBE_API_KEY=your_youtube_api_key_here
DATABASE_URL=postgresql://your_username@localhost/your_database_name
```

### 4. Initialize the Database

### Restore the Database from the Dump

Restore the database from the provided dump file.
Run this command:

```
pg_restore -h localhost -U postgres -d target_database_name -F c path_to_database_dump.sql
```

![alt text](static/images/Database_Columns.png)

#### Run the Database Initialization Script

```sh
python init_db.py
```

### 5. Run the Application

```sh
python app.py
```

Access the app at: `http://127.0.0.1:5000/`

---

## 🧡 Contributing

🍔 Fork the repository

🌱 Create a new branch

`git checkout -b feature-branch`

📂 Commit your changes

`git commit -m "Added new feature"`

🚀 Push to the branch

`git push origin feature-branch`

🔥 Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📋 To-Do List

- 📊 **Add data visualization** for insights into recipe and YouTube-related data
