from fastapi import FastAPI
import requests

app = FastAPI()

def get_favorite_game(user_id):
    url = f"https://games.roblox.com/v2/users/{user_id}/favorite/games?limit=1"
    response = requests.get(url)
    
    if response.status_code == 200 and response.json().get("data"):
        return response.json()["data"][0]["name"]
    return "No favorite game found"

@app.get("/api/info")
async def get_info(user: str):
    if not user:
        return {"error": "User parameter is required"}

    search_url = f"https://users.roblox.com/v1/users/search?keyword={user}&limit=1"
    search_response = requests.get(search_url)

    if search_response.status_code != 200 or not search_response.json().get("data"):
        return {"error": "User not found"}

    user_data = search_response.json()["data"][0]
    user_id = user_data["id"]

    profile_url = f"https://users.roblox.com/v1/users/{user_id}"
    profile_response = requests.get(profile_url)

    if profile_response.status_code != 200:
        return {"error": "Failed to fetch profile data"}

    profile_data = profile_response.json()

    return {
        "Username": profile_data["name"],
        "UserID": profile_data["id"],
        "DisplayName": profile_data["displayName"],
        "CreationDate": profile_data["created"],
        "FavoriteGame": get_favorite_game(user_id),
        "Description": profile_data["description"] or "No description available"
    }
