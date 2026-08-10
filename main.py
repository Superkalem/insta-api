from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Anonim Profil API")

@app.get("/profile/{username}")
def get_profile(username: str):
    # İsteklerin bot gibi görünmemesi için standart bir tarayıcı başlığı
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    # Giriş zorunluluğunu tamamen aşmak için veriyi anonim görüntüleyici üzerinden çekiyoruz
    url = f"https://www.picuki.com/profile/{username}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Profil bulunamadı veya aracı site yanıt vermiyor.")
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        # Profil fotoğrafı linkini HTML'den bul ve çıkar
        profile_pic = soup.find("img", {"class": "profile-avatar"})['src']
        
        # Takipçi sayısının olduğu bölümü bul
        followers_element = soup.find("span", {"class": "followed_by"})
        followers = followers_element.text.strip() if followers_element else "Bulunamadı"
        
        return {
            "username": username,
            "profile_picture": profile_pic,
            "followers": followers,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Veri okunurken hata oluştu. Hata: {str(e)}")
