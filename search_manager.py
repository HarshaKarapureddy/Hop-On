import requests  # type: ignore

CLIENT_ID = "zalzndjimwb5e6k9vo6pbe37vtbe6n"
CLIENT_SECRET = "7o2jgjh9m6h0nb5ucyiz93juox1jpr"


def AccessToken():
    auth_url = "https://id.twitch.tv/oauth2/token"
    auth_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    token_response = requests.post(auth_url, data=auth_data)

    if token_response.status_code != 200:
        return None
    return token_response.json().get("access_token")


def SearchGS(game_name):
    if not game_name:
        return None

    access_token = AccessToken()
    if not access_token:
        return None

    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {access_token}"}

    query = f'search "{game_name}"; fields id, name, genres.name, release_dates.y, cover.url; limit 50;'
    igdb_url = "https://api.igdb.com/v4/games"
    try:
        response = requests.post(igdb_url, headers=headers, data=query)
        if response.status_code != 200:
            return None
        games = response.json()
        return games if games else None
    except:
        return None


def SearchGEN(genres_list):
    if not genres_list:
        print("No genres provided.")
        return None

    access_token = AccessToken()
    if not access_token:
        print("Failed to get access token.")
        return None

    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {access_token}"}

    genre_query = "fields name, id; limit 50;"
    try:
        genre_response = requests.post(
            "https://api.igdb.com/v4/genres", headers=headers, data=genre_query
        )
        if genre_response.status_code != 200:
            print(f"Error fetching genres: {genre_response.status_code}")
            return None
    except:
        return None

    genres = genre_response.json()
    matched_genres = []

    for genre_input in genres_list:
        matched = next(
            (
                g
                for g in genres
                if g["name"].strip().lower() == genre_input.strip().lower()
            ),
            None,
        )
        if matched:
            matched_genres.append(matched["id"])

    if not matched_genres:
        print("No genres matched.")
        return None

    genre_ids = ",".join(map(str, matched_genres))
    print(genre_ids)
    query = (
        f"fields id, name, genres.name, release_dates.y, cover.url; "
        f"where genres = ({genre_ids}) & themes != (42) & rating >= 90 & rating_count >= 300; "
        f"sort popularity desc; "
        f"limit 50;"
    )

    try:
        response = requests.post(
            "https://api.igdb.com/v4/games", headers=headers, data=query
        )
        if response.status_code != 200:
            print(f"Error fetching games: {response.status_code}")
            return None
        games = response.json()
        if not games:
            print("No games found for the given genres.")
        return games if games else None
    except:
        return None
