import os
import requests
import time
from flask import Flask
from threading import Thread

# --- RENDER İÇİN FLASK WEB SUNUCUSU ---
app = Flask('')

@app.route('/')
def home():
    return "Akilli Spam Korumali ve Kilitlenmeyen Sunucu Aktif!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()
# -------------------------------------

BOTLAR = [
    {
        "token": "8679022632:AAFTJahPjxFqijWFdhQRxwl0UDBctic8nj4",
        "chat_ids": ["-1003930885725"],
        "mesajlar": ["KİMSE YENEMEZ", "KİMSE SUSTURAMAZ", "KİMSE İNATLAŞAMAZ", "KİMSE ZITLAŞAMAZ", "KİMSE DURDURAMAZ"],
        "index": 0,
        "sure": 35,  # Ban yememesi için süreler uzatıldı
        "son_gonderim": 0
    },
    {
        "token": "8207117026:AAFdBpVbb2_-asIXQhcpGrqQIbd6lmZ3toQ",
        "chat_ids": ["-1003930885725"],
        "mesajlar": ["99", "66", "99", "66", "99"],
        "index": 0,
        "sure": 50,
        "son_gonderim": 0
    },
    {
        "token": "8823088191:AAHI-J9KlVGk-7LuudNY9gh5iD7URi_fS5M",
        "chat_ids": ["-1003930885725"],
        "mesajlar": ["ANA NIZI GÖTÜN DEN", "SİKEYİ M TÜREMELER", "ANAN IN BURUN", "DELİKLERİNİ DÖLLERİM XD", "SUSTURABİLEN DURDURABİLEN YOK #"],
        "index": 0,
        "sure": 40,
        "son_gonderim": 0
    },
    {
        "token": "8404710859:AAFSlQ7bUQ0SK87zRUk0oj7zjce3tL9E2NE",
        "chat_ids": ["-1003930885725"],
        "mesajlar": ["ANAN IN", "AM INA", "ÇAK I", "SOKARI M", "xdxd"],
        "index": 0,
        "sure": 30,
        "son_gonderim": 0
    },
    {
        "token": "8738362829:AAF3rvT8aaL-SGu2bdeNXQCS3NCAx7lLznI",
        "chat_ids": ["-1003930885725"],
        "mesajlar": ["ANAN IN AM INA", "ZEBEL MÜHRÜ BASARIM", "ANAN IN GÖTÜ NE", "HO OK ATAY IM", "ANAN IN AĞZINI DÖLLERİM"],
        "index": 0,
        "sure": 65,
        "son_gonderim": 0
    }
]

def yaziyor(bot, chat_id):
    try:
        requests.post(
            f"https://telegram.org{bot['token']}/sendChatAction",
            data={"chat_id": chat_id, "action": "typing"},
            timeout=5
        )
    except Exception:
        pass

def gonder(bot):
    mesaj = bot["mesajlar"][bot["index"]]
    for chat_id in bot["chat_ids"]:
        yaziyor(bot, chat_id)
        time.sleep(2)
        try:
            res = requests.post(
                f"https://telegram.org{bot['token']}/sendMessage",
                data={"chat_id": chat_id, "text": mesaj},
                timeout=5
            )
            
            # --- AKILLI TELEGRAM CEZA VE KİLİTLEME SİSTEMİ ---
            if res.status_code == 429:
                # Telegram'dan gelen tam ceza saniyesini okur (Yoksa otomatik 40 saniye uyur)
                ceza_suresi = res.json().get("parameters", {}).get("retry_after", 40)
                print(f"Telegram Limitine Takildi! Bot {ceza_suresi} saniye kendini kilitliyor...")
                time.sleep(ceza_suresi)
                continue
                
            print("Gönderildi:", chat_id, "->", mesaj)
        except Exception as e:
            print("Mesaj gonderilemedi:", e)
            
    bot["index"] = (bot["index"] + 1) % len(bot["mesajlar"])

def bot_ana_dongu():
    while True:
        try:
            simdi = time.time()
            for bot in BOTLAR:
                if simdi - bot["son_gonderim"] >= bot["sure"]:
                    gonder(bot)
                    bot["son_gonderim"] = simdi
        except Exception as e:
            print("Döngü hatası:", e)
        time.sleep(1)

# İki sistemi de ayrı kollarda güvenle başlat
keep_alive()

bot_thread = Thread(target=bot_ana_dongu)
bot_thread.start()
