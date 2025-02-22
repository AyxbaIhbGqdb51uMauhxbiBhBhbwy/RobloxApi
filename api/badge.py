from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/api/badge")
async def get_badges(user: str):
    if not user:
        return {"error": "User parameter is required"}

    # Cari UserID berdasarkan Username
    search_url = f"https://users.roblox.com/v1/users/search?keyword={user}&limit=1"
    search_response = requests.get(search_url)

    if search_response.status_code != 200 or not search_response.json().get("data"):
        return {"error": "User not found"}

    user_id = search_response.json()["data"][0]["id"]

    # Ambil daftar badge pengguna
    badge_url = f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100"
    badge_response = requests.get(badge_url)

    if badge_response.status_code != 200:
        return {"error": "Failed to fetch badges"}

    badges_data = badge_response.json().get("data", [])

    badges = [
        {
            "id": badge["id"],
            "name": badge["name"],
            "description": badge.get("description", "No description available"),
            "image": badge["iconImageId"]
        }
        for badge in badges_data
    ]

    return {"user": user, "badges": badges}
