# -*- coding: utf-8 -*-
"""Movie Recommendation.ML.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CazKwV-nyXShJemU2UwVPLut-ddSA4N_
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error, f1_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

print(ratings.head())
print(movies.head())

print(ratings.isnull().sum())
print(movies.isnull().sum())

ratings.dropna(inplace=True)
movies.dropna(inplace=True)

merged_data = pd.merge(ratings, movies, on='movieId')
print(merged_data.head())

user_movie_matrix = merged_data.pivot_table(index='userId', columns='title', values='rating')
print(user_movie_matrix.head())

user_movie_matrix.fillna(0, inplace=True)

#user based
user_similarity = cosine_similarity(user_movie_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)
print(user_similarity_df.head())

#item based
item_similarity = cosine_similarity(user_movie_matrix.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)
print(item_similarity_df.head())

def predict_ratings(user_id, user_movie_matrix, similarity_matrix):
    similar_users = similarity_matrix[user_id]
    ratings = np.dot(similar_users, user_movie_matrix.fillna(0)) / np.array([np.abs(similar_users).sum()])
    return ratings

train_data, test_data = train_test_split(ratings, test_size=0.2, random_state=42)

import numpy as np
from sklearn.metrics import mean_squared_error

def rmse(predictions, targets):
    return np.sqrt(mean_squared_error(targets, predictions))


predictions = np.array([2.5, 3.0, 3.5, 4.0])
actuals = np.array([2.0, 3.2, 3.7, 4.2])

print("RMSE:", rmse(predictions, actuals))

def rmse(predictions, targets):
    return np.sqrt(mean_squared_error(targets, predictions))
print("RMSE:", rmse(predictions, actuals))

#simple CLI
movie_id = int(input("Enter movie ID: "))
recommendations = predict_ratings(movie_id, user_movie_matrix, user_similarity)
print("Top Recommendations:", recommendations[:10])



import csv
import os

def load_movie_data(file_path):
    """
    Load movie data from a CSV file and return a list of dictionaries.
    """
    movie_list = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert 'genres' to a list if multiple genres are separated by '|'
            row['genres'] = row['genres'].split('|')  # Assuming genres are separated by '|'
            movie_list.append({
                # "movieId": row["movieid"],  # Retain movie ID if needed for later use
                "title": row["title"],
                "genres": row["genres"]
            })
    return movie_list

def get_movie_details(title, movie_data):
    """
    Retrieve the details of a movie from the database using its title.
    """
    for movie in movie_data:
        if movie["title"].strip().lower() == title.strip().lower():
            return movie
    return None

def suggest_movie(preferred_genres, movie_data):
    """
    Suggest a movie based on preferred genres.
    """
    for movie in movie_data:
        if any(genre in preferred_genres for genre in movie["genres"]):
            return movie
    return None

# Set the file path for the movies dataset
file_path = os.path.join(os.getcwd(), 'movies.csv')  # This uses the current working directory
print(f"Looking for the dataset at: {file_path}")

# Load the movie database
try:
    movie_data = load_movie_data(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please check the path and try again.")
    exit()

# Collect input for four movie titles
user_selected_movies = []
print("Enter four movie titles:")

for i in range(4):
    title = input(f"Movie {i + 1}: ")
    details = get_movie_details(title, movie_data)
    if details:
        user_selected_movies.append(details)
    else:
        print(f"Movie '{title}' not found in the database.")

if not user_selected_movies:
    print("No valid movies entered. Unable to make suggestions.")
else:
    # Segregate genres from selected movies
    preferred_genres = set()
    for movie in user_selected_movies:
        preferred_genres.update(movie["genres"])

    print(f"Preferred Genres: {', '.join(preferred_genres)}")

    # Suggest a movie based on genres
    suggestion = suggest_movie(preferred_genres, movie_data)
    if suggestion:
        print("Suggested Movie:")
        print(f"Title: {suggestion['title']}")
        print(f"Genres: {', '.join(suggestion['genres'])}")
    else:
        print("No suitable movie found based on your preferences.")



import numpy as np
from scipy.sparse import csr_matrix

def predict_ratings(user_id, user_movie_matrix, similarity_matrix):

    similar_users = similarity_matrix[user_id]

    # Convert user_movie_matrix to a dense array and fill NaNs with 0
    user_movie_matrix_dense = user_movie_matrix.toarray()
    user_movie_matrix_dense[np.isnan(user_movie_matrix_dense)] = 0

    ratings = np.dot(similar_users, user_movie_matrix_dense) / np.array([np.abs(similar_users).sum()])
    return ratings

from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

user_movie_matrix = csr_matrix(user_movie_matrix)

U, sigma, Vt = svds(user_movie_matrix, k=50)
sigma = np.diag(sigma)
predicted_ratings = np.dot(np.dot(U, sigma), Vt)
print(predicted_ratings)