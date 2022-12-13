from marshmallow import Schema, fields


class MovieSchema(Schema):
    """
    Schema для модели Movie
    """
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = director = fields.Pluck("GenreSchema", "name")
    director_id = fields.Int()
    director = fields.Pluck("DirectorSchema", "name")

    # director = fields.Nested("DirectorSchema", only=("name",))
    # genre = fields.Nested("GenreSchema", only=("name",))
    # Nested выводит director и genre в виде словаря {"id": value , "name": value}
    # only позволяет выводить только один ключ
    # Pluck выводит director и genre значение ключа "name"


class DirectorSchema(Schema):
    """
        Schema для модели Director
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    """
        Schema для модели Genre
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)