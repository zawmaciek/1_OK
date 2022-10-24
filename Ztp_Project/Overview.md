# Project overview Maciej Zawadzki-Adamiak:

Service 1:
StartUp:
Using dataset from [Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
Download, and parse into SQLiteDB dataset from movie lens dataset containing 25 million ratings of 70 thousand movies.
Serve when asked by other services. (ORM/CRUD)
Per USER_ID:
calculate relation between movies similar to markov chain calculated as (movie_1_rating/10)*(movie_2_rating/10)
combine resulting dicts from each user, weighted using a number of user reviews (movie affinity) resulting in 0-1
ranking of similiarity. GET Movie Recommendation (UserPreferences)->List(MoviesMetadata):
Rank movies using weighted: Jaccard index between movie genres and keywords, and ranking calculated from the similiarity
dicts. If not enough movies are found, calculate secondary ranking using nodes from the chain separated by 1 instead of
0 nodes. Client:
Let client select user preferences and send to Service 1, display response.