import _sqlite3
from collections import Counter
from search_manager import AccessToken
import requests  # type: ignore

CLIENT_ID = "zalzndjimwb5e6k9vo6pbe37vtbe6n"


def user_top_genres(userID, top_n=3):
    conn = _sqlite3.connect("reviews.db")
    cursor = conn.cursor()
    cursor.execute("SELECT genre FROM reviews WHERE userID = ?", (userID,))
    rows = cursor.fetchall()
    conn.close()

    genre_counter = Counter()

    for row in rows:
        genres = row[0].split(",")
        for g in genres:
            genre_counter[g.strip().lower()] += 1

    top_genres = [genre for genre, _ in genre_counter.most_common(top_n)]
    return top_genres


def match_ids(gnames):
    access_token = AccessToken()
    if not access_token:
        print("Failed to get access token.")
        return []

    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {access_token}"}
    genre_query = "fields name, id; limit 100;"
    response = requests.post(
        "https://api.igdb.com/v4/genres", headers=headers, data=genre_query
    )

    if response.status_code != 200:
        print("Failed to get genre list.")
        return []

    genres_data = response.json()
    gnames_lower = [name.lower() for name in gnames]
    matched_ids = [g["id"] for g in genres_data if g["name"].lower() in gnames_lower]

    return matched_ids


def get_trending_games_by_genres(genre_ids, limit=10):
    if not genre_ids:
        return []

    access_token = AccessToken()
    if not access_token:
        return []

    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {access_token}"}
    popularity_query = (
        f"fields game_id, value; "
        f"sort value desc; "
        f"where popularity_type = 1; "
        f"limit 50;"
    )

    response1 = requests.post(
        "https://api.igdb.com/v4/popularity_primitives",
        headers=headers,
        data=popularity_query,
    )

    if response1.status_code != 200:
        print("Failed to get popularity data.")
        return []

    popular_game_ids = [entry["game_id"] for entry in response1.json()]
    game_query = (
        f"fields id, name, genres.name, release_dates.y, themes; "
        f"where id = ({','.join(map(str, popular_game_ids))}); "
        f"where themes != (42) & rating >= 90 & rating_count >= 300;"
        f"limit 50;"
    )

    response2 = requests.post(
        "https://api.igdb.com/v4/games", headers=headers, data=game_query
    )

    if response2.status_code != 200:
        print("Failed to get game data.")
        return []

    all_games = response2.json()

    filtered_games = [
        game
        for game in all_games
        if "genres" in game and any(g["id"] in genre_ids for g in game["genres"])
    ]

    return filtered_games[:limit]


def recommend_games_for_user(userID):
    if not userID.isdigit() or len(userID) == 0:
        print(f"Received userID: {userID}")
        print("Error: Invalid userID")
        return

    print(f"\n Generating recommendations for user {userID}...\n")
    top_genres = user_top_genres(userID)

    if not top_genres:
        print("No genre data found for this user.")
        return

    genre_ids = match_ids(top_genres)

    if not genre_ids:
        print("No matching genre IDs found.")
        return

    games = get_trending_games_by_genres(genre_ids)

    if not games:
        print("No trending games found in those genres.")
        return

    print("\n Recommended Trending Games:\n")
    for game in games:
        id = game.get("id")
        name = game.get("name", "Unknown")
        genres = [g["name"] for g in game.get("genres", [])] if "genres" in game else []
        release_year = game.get("release_dates", [{}])[0].get("y", "Unknown")

        print(f"Name: {name}")
        print(f"id: {id}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Release Year: {release_year}")
        print("")


if __name__ == "__main__":
    userID = input("Enter your userID for recommendations: ").strip()
    recommend_games_for_user(userID)
