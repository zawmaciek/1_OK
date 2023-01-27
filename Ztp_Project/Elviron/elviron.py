import enum
import itertools
import pickle
from abc import ABC
from multiprocessing.pool import ThreadPool
from os import path
from typing import Optional

import networkx as nx
from tqdm import tqdm

from movie import MovieID
from orm import ORM


class Matcher(ABC):
    def __init__(self) -> None:
        pass

    def connect_to_db(self) -> None:
        pass

    def calculate(self, recreate: bool = False) -> None:
        pass

    def match(self, request: list[str]) -> list[tuple[str, str]]:
        pass

    def exit(self) -> None:
        pass


class MatcherType(enum.Enum):
    ELVIRON = enum.auto()


class MatcherFactory:
    @staticmethod
    def build(type: MatcherType) -> Optional[Matcher]:
        if type == MatcherType.ELVIRON:
            return Elviron()
        else:
            return None


class Elviron(Matcher):

    def __init__(self):
        super().__init__()
        self.orm = ORM(db_path=r'/Users/mzawadzki-adamiak/PycharmProjects/1_Sem/Ztp_Project/movies_data.db',
                       minimal_views_of_film=300)
        self.minimal_views = 0
        self.movies_count = 0
        self.graph = nx.Graph()
        self.descriptions_by_ids = None
        self.names_to_ids = None
        self.ids_to_names = None

    def connect_to_db(self) -> None:
        self.orm.connect()
        self.ids_to_names = self.orm.get_all_ids_to_names()
        self.names_to_ids = {self.ids_to_names[id]: id for id in self.ids_to_names}
        self.descriptions_by_ids = self.orm.get_all_overviews_by_ids()

    @staticmethod
    def calculate_ratio(data: tuple[list[tuple[MovieID, float]], dict[MovieID, set[str]]]) -> list[
        tuple[MovieID, MovieID, float]]:
        movies = data[0]
        genres_per_movie = data[1]
        combinations = itertools.combinations(movies, 2)
        to_add = []
        for option in combinations:
            movie_id_1 = option[0][0]
            movie_id_2 = option[1][0]
            if len(genres_per_movie[movie_id_1].intersection(genres_per_movie[movie_id_2])) > 0:
                to_add.append((movie_id_1, movie_id_2, option[0][1] * option[1][1] / 25))
        return to_add

    def calculate(self, recreate: bool = False) -> None:
        def avg(input: list[float]) -> float:
            return sum(input) / len(input)

        if path.exists("save.pickle") and not recreate:
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
        print('Fetching ratings per user')
        movies = self.orm.get_ratings_per_user()
        work_graph = nx.Graph()
        users_to_process = [(movies[user_id], genres_per_movie) for user_id in filtered_user_ids]
        print('Calculating ratios')
        with ThreadPool(processes=10) as pool:
            # call a function on each item in a list and handle results
            ratios = [result for result in pool.map_async(self.calculate_ratio, users_to_process).get()]
        ratios = list(itertools.chain.from_iterable(ratios))
        print('Calculating graph')
        for ratio in tqdm(ratios):
            if work_graph.has_edge(ratio[0], ratio[1]):
                work_graph[ratio[0]][ratio[1]]['ratios'].append(ratio[2])
            else:
                work_graph.add_edge(ratio[0], ratio[1])
                work_graph[ratio[0]][ratio[1]]['ratios'] = [ratio[2]]
        for edge in tqdm(work_graph.edges):
            self.graph.add_edge(edge[0], edge[1], weight=avg(work_graph[edge[0]][edge[1]]['ratios']))
        with open('save.pickle', 'wb') as handle:
            print('SAVED')
            pickle.dump(self.graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def match(self, request: list[str]) -> list[tuple[str, str]]:
        try:
            movie_id = self.names_to_ids[request[0]]
            movies = self.graph.neighbors(movie_id)
            weighted_movies = [(movie, self.graph[movie_id][movie]["weight"]) for movie in movies]
            top_3 = sorted(weighted_movies, key=lambda movie: movie[1], reverse=True)[:3]
            return [(self.ids_to_names[movie[0]], self.descriptions_by_ids[movie[0]]) for movie in top_3]
        except Exception as e:
            print(e)
            return []

    def exit(self) -> None:
        self.orm.disconnect()


if __name__ == '__main__':
    elviron = Elviron()
    elviron.connect_to_db()
    elviron.calculate(recreate=True)
