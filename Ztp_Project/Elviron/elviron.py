from tqdm import tqdm
import numpy as np

from movie import MovieID
from orm import ORM

"""
TODO: remove
minimal views vs user count
0
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
        # TODO: Adjust minimal views of the film
        self.orm = ORM(db_path=r'C:\Users\zawma\Desktop\OK_1Sem\Ztp_Project\movies_data.db', minimal_views_of_film=300)
        # TODO: Adjust minimal views of user
        self.minimal_views = 400

    def connect_to_db(self) -> None:
        self.orm.connect()

    def calculate(self) -> None:
        print('Fetching all movie ids')
        movies_ids = self.orm.get_all_movie_ids()
        movies_count = len(movies_ids)
        print(movies_count)
        movie_sim_matrix = np.zeros((movies_count, movies_count), dtype='float')
        movies_id_to_tab_id_map = {MovieID(MovieId): id for id, MovieId in enumerate(movies_ids)}
        print('Fetching ratings counts per user')
        ratings_map = self.orm.get_ratings_count_per_user()
        print(len(ratings_map))
        filtered_user_ids = [user_id for user_id in ratings_map if ratings_map[user_id] > self.minimal_views]
        # TODO: add multiprocessing, group by genre, optimise
        for user_id in tqdm(filtered_user_ids):
            ratings = self.orm.get_ratings_per_user(user_id)
            for i in range(len(ratings)):
                for j in range(i + 1, len(ratings)):
                    movie_sim_matrix[movies_id_to_tab_id_map[ratings[i][0]], movies_id_to_tab_id_map[ratings[j][0]]] += (ratings[i][1] * ratings[j][1] * ratings_map[user_id]-self.minimal_views-1) / 25
        print(movie_sim_matrix)

    def match(self, movie_ids: list[MovieID]) -> list[MovieID]:
        pass

    def exit(self) -> None:
        self.orm.disconnect()


if __name__ == '__main__':
    elviron = Elviron()
    elviron.connect_to_db()
    elviron.calculate()
