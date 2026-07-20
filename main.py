import os
import requests
import time
from flask import Flask
from threading import Thread

# --- RENDER İÇİN FLASK WEB SUNUCUSU ---
app = Flask('')

@app.route('/')
def home():
    return "Bot sorunsuz sekilde aktif ve calisiyor!"

def run_web_server():
    # Render sisteminin otomatik verdigi port numarasini okur
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()
# -------------------------------------

BOTLAR = [
    {
        "token": "8444679695:AAFDR0zVoJgvfIWAQEns4XbH2JYsXTwz4EM",
        "chat_ids": ["@denemecar00"],
        "mesajlar": [
            "KİMSE YENEMEZ",
            "KİMSE SUSTURAMAZ",
            "KİMSE İNATLAŞAMAZ",
            "KİMSE ZITLAŞAMAZ",
            "KİMSE DURDURAMAZ"
        ],
        "index": 0,
        "sure":15,
        "son_gonderim": 0
    },
    {
        "token": "8559320902:AAG7Yeui0_6gHZrbLJqjcJD9uTp5XYVScS4",
        "chat_ids": ["@denemecar00"],
        "mesajlar": [
            "99",
            "66",
            "99",
            "66",
            "99"
        ],
        "index": 0,
        "sure":20,
        "son_gonderim": 0
    },
    {
        "token": "8401816464:AAHrLxyWuneDEIDy1GA1Mc_RVPLffQRkNA8",
        "chat_ids": ["@denemecar00"],
        "mesajlar": [
            "ANA NIZI GÖTÜN DEN",
            "SİKEYİ M TÜREMELER",
            "ANAN IN BURUN",
            "DELİKLERİNİ DÖLLERİM XD",
            "SUSTURABİLEN DURDURABİLEN YOK #"
        ],
        "index": 0,
        "sure":15,
        "son_gonderim": 0
    },
    {
        "token": "8678850317:AAGSfRnnQnRl07uuP4TIx28dg6lVdavkp7c",
        "chat_ids": ["@denemecar00"],
        "mesajlar": [
            "ANAN IN",
            "AM INA",
            "ÇAK I",
            "SOKARI M",
            "xdxd"
        ],
        "index": 0,
        "sure":10,
        "son_gonderim": 0
    },
    {
        "token": "8401816464:AAHrLxyWuneDEIDy1GA1Mc_RVPLffQRkNA8",
        "chat_ids": ["@denemecar00"],
        "mesajlar": [
            "ANAN IN AM INA",
            "ZEBEL MÜHRÜ BASARIM",
            "ANAN IN GÖTÜ NE",
            "HO OK ATAY IM",
            "ANAN IN AĞZINI DÖLLERİM"
        ],
        "index": 0,
        "sure":25,
        "son_gonderim": 0
    }
]

# Yazıyor göstergesi
def yaziyor(bot, chat_id):
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot['token']}/sendChatAction",
            data={
                "chat_id": chat_id,
                "action": "typing"
            },
            timeout=10
        )
    except Exception:
        pass

def gonder(bot):
    mesaj = bot["mesajlar"][bot["index"]]
    for chat_id in bot["chat_ids"]:
        yaziyor(bot, chat_id)
        time.sleep(3)
        try:
            requests.post(
                f"https://api.telegram.org/bot{bot['token']}/sendMessage",
                data={
                    "chat_id": chat_id,
                    "text": mesaj
                },
                timeout=10
            )
            print("Gönderildi:", chat_id, "->", mesaj)
        except Exception as e:
            print("Mesaj gonderilemedi:", e)
            
    bot["index"] = (bot["index"] + 1) % len(bot["mesajlar"])

# Web sunucusunu ana döngü başlamadan önce tetikliyoruz
keep_alive()

while True:
    try:
        simdi = time.time()
        for bot in BOTLAR:
            if simdi - bot["son_gonderim"] >= bot["sure"]:
                gonder(bot)
                bot["son_gonderim"] = simdi
    except Exception as e:
        print("Hata oldu ama bot devam ediyor:", e)

    time.sleep(1)
