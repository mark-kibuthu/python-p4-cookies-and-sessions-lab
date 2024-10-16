#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate
from models import db, Article

app = Flask(__name__)
app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    articles_list = [article.to_dict() for article in articles]
    return jsonify(articles_list), 200

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0)
    session['page_views'] += 1

    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    article = Article.query.get(id)
    if article:
        return jsonify(article.to_dict()), 200
    else:
        return jsonify({'message': 'Article not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
