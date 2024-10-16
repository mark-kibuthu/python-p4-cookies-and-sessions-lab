#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# Route to clear session
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

# Route to list all articles
@app.route('/articles')
def index_articles():
    # Query all articles
    articles = Article.query.all()
    
    # Convert each article to a dictionary to return in JSON
    articles_list = [
        {
            'id': article.id,
            'title': article.title,
            'content': article.content[:100]  # Just a preview of the first 100 characters
        } for article in articles
    ]
    
    return jsonify(articles_list), 200

# Route to view a specific article by its id
@app.route('/articles/<int:id>')
def show_article(id):
    # Set initial value of page_views to 0 if not already set
    session['page_views'] = session.get('page_views', 0)
    
    # Increment page views for each article view
    session['page_views'] += 1

    # If page views exceed 3, return an error message
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    # Retrieve the article by id
    article = Article.query.get(id)
    
    if article:
        # Return the article data as JSON
        return jsonify({
            'id': article.id,
            'title': article.title,
            'content': article.content
        }), 200
    else:
        # If the article isn't found, return a 404 error
        return jsonify({'message': 'Article not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(port=5555)
