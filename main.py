import os
from fastapi import FastAPI, HTTPException
from instagrapi import Client

app = FastAPI()
cl = Client()

# Render'daki gizli kasadan bilgileri alıp otomatik giriş yapıyoruz
IG_USER = os.getenv("IG_USERNAME")
IG_PASS = os.getenv("IG_PASSWORD")

if IG_USER and IG_PASS:
    try:
        cl.login(IG_USER, IG_PASS)
        print("Basariyla giris yapildi!")
    except Exception as e:
        print(f"Giris hatasi: {e}")

@app.get("/")
def read_root():
    return {"mesaj": "Instagram API Çalışıyor!"}

@app.get("/profil/{username}")
def get_user_data(username: str):
    try:
        # Oturum açıldığı için artık bu fonksiyon hata vermeden veriyi çekecek
        user_id = cl.user_id_from_username(username)
        user_info = cl.user_info(user_id)
        
        return {
            "username": user_info.username,
            "full_name": user_info.full_name,
            "followers": user_info.follower_count,
            "following": user_info.following_count,
            "biography": user_info.biography,
            "profile_pic": str(user_info.profile_pic_url)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
