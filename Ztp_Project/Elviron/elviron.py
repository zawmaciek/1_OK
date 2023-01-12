import itertools
import pickle
from collections import Counter
from os import path

from tqdm import tqdm

from movie import MovieID
from orm import ORM
import networkx as nx

"""0
244982

50
22153

100
6302

150
2242

200
849

250
356

300
144

350
62"""


class Elviron:
    def __init__(self):
        self.orm = ORM(db_path=r'C:\Users\zawma\Desktop\OK_1Sem\Ztp_Project\movies_data.db', minimal_views_of_film=300)
        self.minimal_views = 250
        self.movies_count = 0
        self.graph = nx.Graph()

    def connect_to_db(self) -> None:
        self.orm.connect()
        self.ids_to_names = self.orm.get_all_ids_to_names()
        self.names_to_ids = {self.ids_to_names[id]: id for id in self.ids_to_names}

    @staticmethod
    def calculate_ratio(movies: list[tuple[MovieID, float]], genres_per_movie: dict[MovieID, set[str]]) -> list[
        tuple[MovieID, MovieID, float]]:
        combinations = itertools.combinations(movies, 2)
        to_add = []
        for option in combinations:
            movie_id_1 = option[0][0]
            movie_id_2 = option[1][0]
            if len(genres_per_movie[movie_id_1].intersection(genres_per_movie[movie_id_2])) > 0:
                to_add.append((movie_id_1, movie_id_2, option[0][1] * option[1][1] / 25))
        return to_add

    def calculate(self) -> None:
        def avg(input: list[float]) -> float:
            return sum(input) / len(input)

        if path.exists("save.pickle"):
            print("LOADING FROM PICKLED STATE")
            with open('save.pickle', 'rb') as handle:
                self.graph = pickle.load(handle)
            return None

        print('Fetching all movie ids')
        movies_ids = self.orm.get_all_movie_ids()
        print('Adding nodes')
        self.graph.add_nodes_from(movies_ids)
        self.movies_count = len(movies_ids)
        print(self.movies_count)
        print('Fetching ratings counts per user')
        ratings_map = self.orm.get_ratings_count_per_user()
        print(len(ratings_map))
        filtered_user_ids = [user_id for user_id in ratings_map if ratings_map[user_id] > self.minimal_views]
        print('Fetching genres per id')
        genres_per_movie = self.orm.get_genres_per_movie_id()
        calculated_movies = Counter()
        work_graph = nx.Graph()
        for user_id in tqdm(filtered_user_ids):
            movies = self.orm.get_ratings_per_user(user_id)
            titles = [self.ids_to_names[movie[0]] for movie in movies]
            calculated_movies.update(titles)
            ratios = self.calculate_ratio(movies, genres_per_movie)
            for ratio in ratios:
                if work_graph.has_edge(ratio[0], ratio[1]):
                    work_graph[ratio[0]][ratio[1]]['ratios'].append(ratio[2])
                else:
                    work_graph.add_edge(ratio[0], ratio[1])
                    work_graph[ratio[0]][ratio[1]]['ratios'] = [ratio[2]]
        for edge in tqdm(work_graph.edges):
            self.graph.add_edge(edge[0], edge[1], weight=avg(work_graph[edge[0]][edge[1]]['ratios']))
        print(calculated_movies.most_common()[:10])
        with open('save.pickle', 'wb') as handle:
            pickle.dump(self.graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def match(self, request: list[str]) -> list[tuple[str, float]]:
        try:
            movie_id = self.names_to_ids[request[0]]
            movies = self.graph.neighbors(movie_id)
            weighted_movies = [(self.ids_to_names[movie], self.graph[movie_id][movie]["weight"]) for movie in movies]
            return sorted(weighted_movies, key=lambda movie: movie[1], reverse=True)[:10]
        except Exception as e:
            print(e)
            return []

    def exit(self) -> None:
        self.orm.disconnect()


if __name__ == '__main__':
    elviron = Elviron()
    elviron.connect_to_db()
    elviron.calculate()
