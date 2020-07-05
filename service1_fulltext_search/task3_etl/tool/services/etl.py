import json
import sqlite3
from collections import defaultdict
from typing import List, Dict, Set

from tool.services.es_loader import ESLoader


class ETL:
    def __init__(self, conn: sqlite3.Connection, es_loader: ESLoader):
        self.es_loader = es_loader
        self.conn = conn

    def load(self, index_name: str):
        '''
        Основной метод для нашего ETL.
        Обязательно используйте метод load_to_es, это будет проверяться
        :param index_name: название индекса, в который будут грузиться данные
        '''
        data = self.retrieve_data()
        self.es_loader.load_to_es(data, 'movies')

    def retrieve_data(self) -> List[dict]:
        writers = self.retrieve_writers()
        actors = self.retrieve_actors()
        movie_id_to_actor_ids = self.retrieve_movie_id_to_actor_ids()

        id_to_writer = {writer['id']: writer for writer in writers}
        id_to_actor = {actor['id']: actor for actor in actors}

        return self.retrieve_movies(id_to_writer, id_to_actor, movie_id_to_actor_ids)

    def retrieve_writers(self) -> List[dict]:
        writers = list()
        for writer_id, name in self.conn.execute('select * from writers;'):
            if writer_id is None or name is None:
                continue

            writers.append({
                'id': writer_id,
                'name': name
            })

        return writers

    def retrieve_actors(self) -> List[dict]:
        actors = list()
        for actor_id, name in self.conn.execute('select * from actors;'):
            if actor_id is None or name is None:
                continue

            actor_id = int(actor_id)
            actors.append({
                'id': actor_id,
                'name': name
            })

        return actors

    def retrieve_movie_id_to_actor_ids(self) -> Dict[str, Set[int]]:
        movie_id_to_actor_ids = defaultdict(set)
        for movie_id, actor_id in self.conn.execute('select movie_id, actor_id from movie_actors;'):
            if movie_id is None or actor_id is None:
                continue

            actor_id = int(actor_id)
            movie_id_to_actor_ids[movie_id].add(actor_id)

        return movie_id_to_actor_ids

    def retrieve_movies(
            self,
            id_to_writer: Dict[str, dict],
            id_to_actor: Dict[int, dict],
            movie_id_to_actor_ids: Dict[str, Set[int]]
    ) -> List[dict]:
        movies = list()

        for movie_id, genres, writer_id, writers_json, imdb_rating, title, directors, description in self.conn.execute(
                'select id, genre, writer, writers, imdb_rating, title, director, plot from movies;'
        ):
            if movie_id == 'N/A' or imdb_rating == 'N/A' or title == 'N/A' or description == 'N/A':
                continue

            if writer_id:
                writers = [{'id': writer_id}]
            else:
                try:
                    writers = json.loads(writers_json)
                except Exception:
                    continue

            movies.append({
                'id': movie_id,
                'genre': genres.split(', ') if genres else [],
                'writers': [id_to_writer[writer['id']] for writer in writers],
                'actors': [id_to_actor[actor_id] for actor_id in movie_id_to_actor_ids[movie_id]],
                'imdb_rating': float(imdb_rating),
                'title': title,
                'director': directors.split(', ') if directors else [],
                'description': description
            })

        for movie in movies:
            movie['actors_names'] = [actor['name'] for actor in movie['actors']]
            movie['writers_names'] = [writer['name'] for writer in movie['writers']]

        return movies
