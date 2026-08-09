import os
from fastapi import FastAPI, HTTPException
from instagrapi import Client

app = FastAPI()
cl = Client()

# Sahte hesabının kullanıcı adı ve şifresini buraya yazabilirsin 
# (Veya daha önce Render ayarlarına eklediğimiz gizli değişkenlerden alır)
IG_USERNAME = os.getenv("IG_USERNAME", "buraya_kullanici_adi_yaz")
IG_PASSWORD = os.getenv("IG_PASSWORD", "buraya_sifre_yaz")

# Sunucu başlarken otomatik giriş yap
try:
    cl.login(IG_USERNAME, IG_PASSWORD)
    print("Instagram'a basariyla giris yapildi!")
except Exception as e:
    print(f"Giris basarisiz: {e}")

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
