import json
from typing import List
from urllib import request


class ESLoader:
    def __init__(self, url: str):
        self.url = url

    def load_to_es(self, records: List[dict], index_name: str):
        '''
        Метод для сохранения записей в Elasticsearch.
        :param records: список данных на запись, который должен быть следующего вида:
        [
            {
                "id": "tt123456",
                "genre": ["Action", "Horror"],
                "writers": [
                    {
                        "id": "123456",
                        "name": "Great Divider"
                    },
                    ...
                ],
                "actors": [
                    {
                        "id": "123456",
                        "name": "Poor guy"
                    },
                    ...
                ],
                "actors_names": ["Poor guy", ...],
                "writers_names": [ "Great Divider", ...],
                "imdb_rating": 8.6,
                "title": "A long time ago ...",
                "director": ["Daniel Switch", "Carmen B."],
                "description": "Long and boring description"
            }
        ]
        Если значения нет или оно N/A, то нужно менять на None
        В списках значение N/A надо пропускать
        :param index_name: название индекса, куда будут сохраняться данные
        '''
        prepared_movies = list()
        for movie in records:
            prepared_movie = dict(movie)
            prepared_movie['actors_names'] = ', '.join(prepared_movie['actors_names'])
            prepared_movie['writers_names'] = ', '.join(prepared_movie['writers_names'])
            prepared_movies.append(prepared_movie)

        data_rows = list()
        for movie in prepared_movies:
            data_rows.append(json.dumps({"index": {"_index": "movies", "_id": movie['id']}}))
            data_rows.append(json.dumps(movie))

        data = '\n'.join(data_rows) + '\n'
        req = request.Request(f'{self.url}/_bulk', method='POST', data=data.encode(), headers={
            'Content-Type': 'application/x-ndjson'
        })
        request.urlopen(req)
