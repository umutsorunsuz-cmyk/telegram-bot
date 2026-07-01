import asyncio
import time
from telethon import TelegramClient, errors

api_id =32706386
api_hash = "b25f4f8f75789a67f0172d12d9f759d2"

client = TelegramClient("hesap1", api_id, api_hash)

group1 = -1003926759594
group2 = -1004297329547


messages1 = [
    "anana atlı suvari",
    "kılıcıyla dalarım xd",
    "ananın gözlerine",
    "kaynar sular döküceğim",
    "kimse"
]

messages2 = [
    "anana atlı süvari",
    "kılıcıyla dalarımxd",
    "ananın gözlerine ",
    "kaynar sular döküceğim xd",
    "kimse"
]


# bağlantı kontrol
async def reconnect():

    while not client.is_connected():

        try:
            print("🔄 Yeniden bağlanıyor...")
            await client.connect()

            if client.is_connected():
                print("✅ Bağlantı geri geldi")

        except Exception as e:
            print("❌ Bağlanamadı:", e)

        await asyncio.sleep(5)



async def safe_start():

    while True:
        try:
            await client.start()
            print("✅ Telegram bağlandı")
            break

        except Exception as e:
            print("Bağlantı hatası:", e)
            await asyncio.sleep(5)



async def typing(chat):

    try:
        async with client.action(chat, "typing"):
            await asyncio.sleep(2)

    except:
        pass



async def send(chat, msg):

    try:

        if not client.is_connected():
            await reconnect()


        await typing(chat)

        await client.send_message(chat, msg)

        print("📤 Gönderildi:", msg)


    except errors.FloodWaitError as e:

        print("⛔ Flood bekleme:", e.seconds)

        await asyncio.sleep(e.seconds)


    except Exception as e:

        print("⚠ Gönderme hatası:", e)

        await asyncio.sleep(5)



async def loop():

    i = 0

    while True:

        try:

            if not client.is_connected():

                print("📡 İnternet/bağlantı yok bekleniyor")

                await reconnect()


            msg1 = messages1[i % len(messages1)]
            msg2 = messages2[i % len(messages2)]


            await send(group1, msg1)

            await asyncio.sleep(2)


            await send(group2, msg2)


            i += 1


            await asyncio.sleep(8)


        except Exception as e:

            print("🔥 Döngü hatası:", e)

            await asyncio.sleep(5)



async def main():

    await safe_start()

    print("🚀 Bot 7/24 aktif")

    await loop()



while True:

    try:

        asyncio.run(main())


    except Exception as e:

        print("💥 Yeniden başlıyor:", e)

        time.sleep(5)
