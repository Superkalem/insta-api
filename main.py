from fastapi import FastAPI, HTTPException
import cloudscraper
from bs4 import BeautifulSoup

app = FastAPI(title="Anonim Profil API")

@app.get("/profile/{username}")
def get_profile(username: str):
    # Cloudscraper ile gerçek bir kullanıcı (Chrome/Windows) taklidi yapıyoruz
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    url = f"https://www.picuki.com/profile/{username}"
    
    # requests.get yerine cloudscraper kullanıyoruz
    response = scraper.get(url)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=404, 
            detail=f"Güvenlik duvarı aşılamadı veya profil gizli. Durum Kodu: {response.status_code}"
        )
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        # Profil fotoğrafı linkini HTML'den bul
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
        raise HTTPException(status_code=500, detail="Sayfa HTML yapısı okunamadı veya Cloudflare Captcha (Doğrulama) ekranına düşüldü.")
