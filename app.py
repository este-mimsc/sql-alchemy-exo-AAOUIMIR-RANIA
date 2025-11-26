"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# These extension instances are shared across the app and models
# so that SQLAlchemy can bind to the application context when the
# factory runs.
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    """Application factory used by Flask and the tests.

    The optional ``test_config`` dictionary can override settings such as
    the database URL to keep student tests isolated.
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    import models
    models.db = db  # injecter db de app.py dans models

    from models import User, Post
    # Import models here so SQLAlchemy is aware of them before migrations
    # or ``create_all`` run. Students will flesh these out in ``models.py``.
  # noqa: F401

    @app.route("/")
    def index():
        """Simple sanity check route."""

        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})

    @app.route("/users", methods=["GET", "POST"])
    def users():
        #lister les utilisateurs
        if request.method=="GET":
           users=User.query.all()
           users_list=[]
           for user in users:
               users_list.append({
                "id":user.id,
                "username":user.username
                                })
           return jsonify(users_list),200
        else:
        # Créer un nouvel utilisateur à partir du JSON
            data=request.get_json()
            if not data or "username" not in data:
                return jsonify({"error": "username is required"}), 400
            username=data["username"]
            exist=User.query.filter_by(username=username).first()
            if exist:
                return jsonify({"error":"username déja existe!!"}),409
            else:
                new=User(username=username)
                db.session.add(new)
                db.session.commit()
                # Return the created user data including id and username
                return jsonify({"id": new.id, "username": new.username}),201
                
           
            

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        if request.method=="GET":
            #lister les posts avec les informations de l'auteur.
            posts=Post.query.all()
            post_list=[]
            for post in posts:
                post_list.append({
                    "id":post.id,
                    "title":post.title,
                    "content":post.content,
                    "user_id":post.author.id,
                    "username":post.author.username
                })
            return jsonify(post_list), 200
        elif request.method=="POST":
            #ajouter des posts
            data=request.get_json()
            if not data or "title" not in data or "content" not in data or "user_id" not in data:
               return jsonify({"error": "title, content et user_id sont requis"}), 400
            title=data["title"]
            content=data["content"]
            user_id=data["user_id"]
            # Vérifier que l'utilisateur existe
            user = db.session.get(User, user_id)
            if not user:
               return jsonify({"error": "user_id invalide — cet utilisateur n'existe pas"}), 400
            else:
                new=Post(title=title,content=content,user_id=user_id)
                db.session.add(new)
                db.session.commit()
                return jsonify({"msg": "post bien ajouté", "id": new.id}), 201
            
        

    return app


# Expose a module-level application for convenience with certain tools
app = create_app()


if __name__ == "__main__":
    # Running ``python app.py`` starts the development server.
    app.run(debug=True)
