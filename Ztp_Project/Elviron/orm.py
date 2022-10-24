import sqlite3

from typing import NewType

from Ztp_Project.Elviron.movie import MovieID

UserID = NewType("UserID", str)


class ORM:
    def __init__(self, db_path: str, minimal_views_of_film: int = 300) -> None:
        self.path = db_path
        self.con = None
        self.cur = None
        self.minimal_views = minimal_views_of_film

    def connect(self) -> None:
        if self.con is None:
            self.con = sqlite3.connect(self.path)
            if self.cur is None:
                self.cur = self.con.cursor()

    def get_ratings_count_per_user(self) -> dict[UserID, int]:
        results = self.cur.execute(
            'SELECT A.userId ,COUNT(A.movieId) from ratings A WHERE A.movieId IN (SELECT B.id from movies_metadata B WHERE CAST(B.vote_count AS int)>?) GROUP BY A.userId',
            (self.minimal_views,)).fetchall()
        return {UserID(result[0]): result[1] for result in results}

    def get_ratings_per_user(self, user_id: UserID) -> list[tuple[MovieID, float]]:
        results = self.cur.execute(
            "SELECT A.movieId,A.rating FROM ratings A WHERE A.userId=? AND A.movieId IN (SELECT B.id from movies_metadata B WHERE CAST(B.vote_count AS int)>?)",
            (user_id, self.minimal_views)).fetchall()
        return [(MovieID(result[0]), float(result[1])) for result in results]

    def disconnect(self):
        self.con.close()

    def get_all_movie_ids(self) -> list[MovieID]:
        results = self.cur.execute('SELECT id from movies_metadata WHERE CAST(vote_count AS int)>?',
                                   (self.minimal_views,)).fetchall()
        return [MovieID(result[0]) for result in results]
