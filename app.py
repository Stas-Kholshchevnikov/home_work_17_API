
from flask import request
from app_config import api, app, db
from flask_restx import Resource
from models.schems import movie_schema, movies_schema, director_schema, directors_schema, genres_schema, genre_schema
from models.sql_models import Movie, Director, Genre

movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


@movie_ns.route("/")
class MoviesView(Resource):
    """
    CBV для namespce '/movies'
    """
    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        movies = db.session.query(Movie)
        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)
        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)
        else:
            movies = movies.all()

        result = movies_schema.dump(movies)
        return result, 200

    def post(self):
        data_json = request.json
        new_film = Movie(**data_json)

        with db.session.begin():
            db.session.add(new_film)

        return "Новая запись создана", 201


@movie_ns.route("/<int:uid>")
class MovieView(Resource):
    """
        CBV для namespce '/movies/<uid>'
    """
    def get(self, uid: int):
        movie_by_uid = Movie.query.get(uid)

        if not movie_by_uid:
            return "Фильм по заданным параметрам не найден", 404

        result = movie_schema.dump(movie_by_uid)
        return result, 200

    def put(self, uid: int):
        new_data = request.json
        update_movie = db.session.query(Movie).filter(Movie.id == uid).update(new_data)

        if update_movie is None:
            return f"Запись с номером {uid} не найдена", 404

        db.session.commit()
        return "", 204

    def delete(self, uid):
        movie = Movie.query.get(uid)

        if not movie:
            return "Фильм не найден", 404

        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route("/")
class DirectorsView(Resource):
    """
        CBV для namespce '/directors'
    """
    def get(self):
        directors = Director.query.all()
        result = directors_schema.dump(directors)
        return result, 200

    def post(self):
        data_json = request.json
        new_director = Director(**data_json)
        with db.session.begin():
            db.session.add(new_director)
        return "Новая запись создана", 201


@director_ns.route("/<int:uid>")
class DirectorView(Resource):
    """
        CBV для namespce '/directors/<uid>'
    """
    def get(self, uid):
        director = Director.query.get(uid)
        if director:
            result = director_schema.dump(director)
            return result, 200
        else:
            return "Данных режесера по указанным параметрам нет", 404


    def put(self, uid: int):
        new_data = request.json
        update_director = db.session.query(Director).filter(Director.id == uid).update(new_data)

        if update_director is None:
            return f"Запись с номером {uid} не найдена", 404

        db.session.commit()
        return "", 204


    def delete(self, uid: int):
        director = Director.query.get(uid)

        if not director:
            return "Режиссер не найден", 404

        db.session.delete(director)
        db.session.commit()
        return "", 204

@genre_ns.route("/")
class GenresView(Resource):
    """
        CBV для namespce '/genres'
    """
    def get(self):
        genres = Genre.query.all()
        result = genres_schema.dump(genres)
        return result, 200

    def post(self):
        data_json = request.json
        new_genre = Genre(**data_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "Новая запись создана", 201


@genre_ns.route("/<int:uid>")
class GenreView(Resource):
    """
        CBV для namespce '/genres/<uid>'
    """
    def get(self, uid: int):
        genre = Genre.query.get(uid)
        if genre:
            result = genre_schema.dump(genre)
            return result, 200
        else:
            return "Данных жанра по указанным параметрам нет", 404

    def put(self, uid: int):
        new_data = request.json
        update_genre = db.session.query(Genre).filter(Genre.id == uid).update(new_data)

        if update_genre is None:
            return f"Запись с номером {uid} не найдена", 404

        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        genre = Genre.query.get(uid)

        if not genre:
            return "Жанр не найден", 404

        db.session.delete(genre)
        db.session.commit()
        return "", 204




if __name__ == '__main__':
    app.run(debug=True)
