from pydantic import BaseModel
from tqdm import tqdm
import numpy as np

from movie import MovieID
from orm import ORM

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
        self.minimal_views = 350
        self.movie_sim_matrix = None
        self.movies_id_to_tab_id_map = None
        self.movies_count = 0

    def connect_to_db(self) -> None:
        self.orm.connect()

    def calculate(self) -> None:
        print('Fetching all movie ids')
        movies_ids = self.orm.get_all_movie_ids()
        self.movies_count = len(movies_ids)
        print(self.movies_count)
        self.movie_sim_matrix = np.zeros((self.movies_count, self.movies_count), dtype='float')
        self.movies_id_to_tab_id_map = {MovieID(movie_id): id for id, movie_id in enumerate(movies_ids)}
        self.movies_tab_id_to_id_map = {id: movie_id for movie_id, id in self.movies_id_to_tab_id_map.items()}
        print('Fetching ratings counts per user')
        ratings_map = self.orm.get_ratings_count_per_user()
        print(len(ratings_map))
        filtered_user_ids = [user_id for user_id in ratings_map if ratings_map[user_id] > self.minimal_views]
        for user_id in tqdm(filtered_user_ids):
            ratings = self.orm.get_ratings_per_user(user_id)
            for i in range(len(ratings)):
                for j in range(i + 1, len(ratings)):
                    value = (ratings[i][1] * ratings[j][1] * ratings_map[user_id] - self.minimal_views - 1) / 25
                    self.movie_sim_matrix[self.movies_id_to_tab_id_map[ratings[i][0]], self.movies_id_to_tab_id_map[
                        ratings[j][0]]] += value
                    self.movie_sim_matrix[self.movies_id_to_tab_id_map[ratings[j][0]], self.movies_id_to_tab_id_map[
                        ratings[i][0]]] += value

    def match(self, request: list[MovieID]) -> list[tuple[MovieID,float]]:
        movie_id = request[0]
        movies = dict()
        for i in range(self.movies_count):
            movies[self.movies_tab_id_to_id_map[i]] = self.movie_sim_matrix[movie_id][i]
        sorted_results = [(k, v) for k, v in sorted(movies.items(), key=lambda item: item[1], reverse=True)]
        return sorted_results[0:5]

    def exit(self) -> None:
        self.orm.disconnect()


if __name__ == '__main__':
    elviron = Elviron()
    elviron.connect_to_db()
    elviron.calculate()
