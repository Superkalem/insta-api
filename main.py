from fastapi import FastAPI, HTTPException
from instagrapi import Client

app = FastAPI()
cl = Client()

@app.get("/")
def read_root():
    return {"mesaj": "Gelişmiş Instagram API Çalışıyor!"}

@app.get("/profil/{username}")
def get_user_data(username: str):
    try:
        user_id = cl.user_id_from_username(username)
        user_info = cl.user_info(user_id)
        
        profil_verisi = {
            "username": user_info.username,
            "full_name": user_info.full_name,
            "followers": user_info.follower_count,
            "following": user_info.following_count,
            "biography": user_info.biography,
            "profile_pic": str(user_info.profile_pic_url)
        }
        
        return profil_verisi
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
