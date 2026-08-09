from fastapi import FastAPI, HTTPException
import instaloader

app = FastAPI()
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
    compress_json=False
)

@app.get("/")
def home():
    return {"mesaj": "Instagram API Calisiyor!"}

@app.get("/profil/{username}")
def get_profile(username: str):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "profile_pic_url": profile.profile_pic_url,
            "followers": profile.followers,
            "following": profile.followees,
            "is_private": profile.is_private,
            "post_count": profile.mediacount
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
