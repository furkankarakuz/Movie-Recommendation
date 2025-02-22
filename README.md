# Movie Recommendation System

This repository contains a movie recommendation system implemented using various machine learning algorithms. The purpose of this project is to provide personalized movie suggestions based on a user's preferences.

## Features

- Personalized movie recommendations based on user ratings.
- Ability to select different algorithms for recommendation (e.g., collaborative filtering, content-based filtering).
- Support for rating-based recommendations.

## Setup and Installation

### Requirements
- Python 3.x
- pandas
- numpy
- scikit-learn
- Surprise
- Flask (Optional, if implementing a web interface)

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/furkankarakuz/movie_recommendation.git
    cd movie_recommendation
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the movie recommendation script:
    ```bash
    python recommend.py
    ```

4. (Optional) If a web interface is included, run the Flask server:
    ```bash
    flask run
    ```

## Usage

### Recommendation

To generate recommendations for a user, input their movie ratings and use the available algorithms to provide personalized suggestions.

1. **Collaborative Filtering**: Recommend movies based on user similarity.
2. **Content-Based Filtering**: Recommend movies based on content features (e.g., genre, director).

### Example Code Snippet

```python
from recommendation_system import get_movie_recommendations

# Sample user ratings
user_ratings = {
    'movie_1': 5,
    'movie_2': 3,
    'movie_3': 4,
}

recommendations = get_movie_recommendations(user_ratings)
print("Recommended Movies:", recommendations)
