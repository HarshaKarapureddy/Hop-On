import requests

CLIENT_ID = "zalzndjimwb5e6k9vo6pbe37vtbe6n"
CLIENT_SECRET = "7o2jgjh9m6h0nb5ucyiz93juox1jpr"

def AcessToken():
    auth_url = "https://id.twitch.tv/oauth2/token"
    auth_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    token_response = requests.post(auth_url, data=auth_data)
    
    if token_response.status_code != 200:
        return None
    return token_response.json().get("access_token")


def SearchGS(game_name):
    if not game_name:
        return None
        
    access_token = AcessToken()
    if not access_token:
        return None
    
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    
    query = f'search "{game_name}"; fields name, genres.name, release_dates.y, cover.url; limit 5;'
    igdb_url = "https://api.igdb.com/v4/games"
    try:
        response = requests.post(igdb_url, headers=headers, data=query)
        if response.status_code != 200:
            return None
        games = response.json()
        return games if games else None
    except:
        return None

def SearchGEN(genres_list, result_limit=5):
    if not genres_list:
        return None
        
    access_token = AcessToken()
    if not access_token:
        return None
    
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }

    genre_query = 'fields name, id; limit 50;'
    try:
        genre_response = requests.post("https://api.igdb.com/v4/genres", headers=headers, data=genre_query)
        if genre_response.status_code != 200:
            return None
    except:
        return None

    genres = genre_response.json()
    matched_genres = []
    
    for genre_input in genres_list:
        matched = next((g for g in genres if g["name"].lower() == genre_input.lower()), None)
        if matched:
            matched_genres.append(matched["id"])

    if not matched_genres:
        return None

    genre_ids = ','.join(map(str, matched_genres))
    query = (
        f'fields name, genres.name, release_dates.y, cover.url; '
        f'where genres = ({genre_ids}); '
        f'sort popularity desc; '
        f'limit {result_limit};'
    )
    
    try:
        response = requests.post("https://api.igdb.com/v4/games", headers=headers, data=query)
        if response.status_code != 200:
            return None
        games = response.json()
        return games if games else None
    except:
        return None

def main():
    access_token = AcessToken()
    if not access_token:
        print("Failed to authenticate with Twitch API")
        return

    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }

    print("\nChoose an option:")
    print("1. Search by Game Name")
    print("2. Search by Genre")
    choice = input("Enter 1 or 2: ").strip()

    if choice not in ["1", "2"]:
        print("Invalid not in the range of 1-2.")
        return

    if choice == "1":
        game_name = input("Enter game name: ").strip()
        if not game_name:
            print("Please enter a valid game name.")
            return

        games = SearchGS(game_name)
        if not games:
            print("Sorry! No games found.")
            return

    elif choice == "2":
        genre_input = input("Enter genres (Adventure, Indie, Shooter), separated by commas please: ").strip().lower()
        if not genre_input:
            print("Please select at least one genre.")
            return

        genres_list = [genre.strip() for genre in genre_input.split(",")]
        
        try:
            result_limit = int(input("How many results (MAX 10)? ").strip())
            if result_limit < 1 or result_limit > 10:
                print("Invalid result limit. Please enter a value between 1-10.")
                return
        except ValueError:
            result_limit = 5

        games = SearchGEN(genres_list, result_limit)
        if not games:
            print("Sorry! No games found for the specified genres.")
            return

    print("\nResults:\n")
    for game in games:
        name = game.get("name", "Unknown")
        genres = [g["name"] for g in game.get("genres", [])] if "genres" in game else ["N/A"]
        release_year = game.get("release_dates", [{}])[0].get("y", "Unknown")
        cover = game.get("cover", {}).get("url", "No cover")
        
        print(f"Name: {name}")
        print(f"Release Year: {release_year}")
        print(f"Genres: {', '.join(genres)}")
        print(f"Cover: {cover}\n")

if __name__ == "__main__":
    main()
