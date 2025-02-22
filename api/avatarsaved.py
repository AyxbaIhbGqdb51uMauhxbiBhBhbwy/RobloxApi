from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/api/avatarsaved")
async def get_avatars(user: str):
    if not user:
        return {"error": "User parameter is required"}

    search_url = f"https://users.roblox.com/v1/users/search?keyword={user}&limit=1"
    search_response = requests.get(search_url)

    if search_response.status_code != 200 or not search_response.json().get("data"):
        return {"error": "User not found"}

    user_id = search_response.json()["data"][0]["id"]

    outfits_url = f"https://avatar.roblox.com/v1/users/{user_id}/outfits?itemsPerPage=50"
    outfits_response = requests.get(outfits_url)

    if outfits_response.status_code != 200:
        return {"error": "Failed to fetch avatars"}

    outfits_data = outfits_response.json().get("data", [])

    avatars = [
        {
            "outfitId": outfit["id"],
            "name": outfit["name"],
            "image": f"https://www.roblox.com/outfit-thumbnail/image?outfitId={outfit['id']}&width=420&height=420&format=png"
        }
        for outfit in outfits_data
    ]

    return {"user": user, "avatars": avatars}
