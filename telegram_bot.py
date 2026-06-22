#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import urllib.request
import urllib.parse
import time
from dotenv import load_dotenv

# .env fayldan o'zgaruvchilarni yuklash
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SITE_URL = os.getenv("SITE_URL", "https://nonracial-seldomly-bryce.ngrok-free.dev")

if not TOKEN:
    print("XATOLIK: TELEGRAM_BOT_TOKEN topilmadi! Iltimos, .env faylini tekshiring.")

API_URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_request(method, data=None):
    """Telegram API ga so'rov yuborish funksiyasi (Tashqi kutubxonalarsiz)"""
    url = API_URL + method
    headers = {"Content-Type": "application/json"}
    
    req_data = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Telegram API xatoligi ({method}): {e}")
        return None

def send_message(chat_id, text, reply_markup=None):
    """Oddiy matnli xabar yuborish"""
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return send_request("sendMessage", payload)

def get_updates(offset=None):
    """Yangi xabarlarni olish (Long Polling)"""
    payload = {"timeout": 30}
    if offset:
        payload["offset"] = offset
    return send_request("getUpdates", payload)

def get_main_keyboard():
    """Asosiy menyu tugmalari"""
    return {
        "keyboard": [
            [{"text": "🚀 Tizim Haqida"}, {"text": "💻 Demo kirish"}],
            [{"text": "✨ Imkoniyatlar"}, {"text": "📱 Mobil Ilova"}],
            [{"text": "📞 Aloqa / Yordam"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

def handle_message(message):
    """Kelgan matnli xabarlarni qayta ishlash"""
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user_name = message["from"].get("first_name", "Foydalanuvchi")

    if text == "/start":
        welcome_text = (
            f"👋 *Assalomu alaykum, {user_name}!*\\n\\n"
            f"🎓 *Mini-HEMIS* — Oliy va o'rta maxsus ta'lim muassasalari uchun "
            f"kengaytirilgan, tezkor va xavfsiz boshqaruv axborot tizimining rasmiy botiga xush kelibsiz!\\n\\n"
            f"Bu bot orqali tizim imkoniyatlari bilan tanishishingiz, demo versiyasini sinab ko'rishingiz "
            f"va biz bilan bog'lanishingiz mumkin. Menyu tugmalaridan birini tanlang 👇"
        )
        send_message(chat_id, welcome_text, get_main_keyboard())

    elif text == "🚀 Tizim Haqida":
        about_text = (
            "📌 *Mini-HEMIS Tizimi Haqida*\\n\\n"
            "Bu platforma ta'lim muassasalarida talabalar, o'qituvchilar, arizalar va kontrakt "
            "to'lovlarini to'liq avtomatlashtirish uchun ishlab chiqilgan.\\n\\n"
            "Tizim eng zamonaviy xavfsizlik protokollari bilan himoyalangan bo'lib, "
            "foydalanish uchun juda qulay va tezkor hisoblanadi. Shuningdek, tizimning "
            "alohida Android ilovasi ham mavjud!"
        )
        send_message(chat_id, about_text)

    elif text == "💻 Demo kirish":
        demo_text = (
            "💻 *Tizimning Demo Versiyasi*\\n\\n"
            "Tizimning to'liq imkoniyatlarini brauzer orqali sinab ko'rishingiz mumkin:\\n\\n"
            f"🔗 *Sayt manzili:* {SITE_URL}\\n\\n"
            "🔑 *Sinov uchun ma'lumotlar:*\\n"
            "• Roli: `Admin / Operator / Talaba`\\n"
            "ℹ️ _Eslatma: Tizim mobil qurilmalar uchun to'liq moslashtirilgan (Responsive)._"
        )
        
        inline_markup = {
            "inline_keyboard": [
                [{"text": "🌐 Saytga o'tish", "url": SITE_URL}]
            ]
        }
        send_message(chat_id, demo_text, inline_markup)

    elif text == "✨ Imkoniyatlar":
        features_text = (
            "🌟 *Mini-HEMIS Tizimining Asosiy Imkoniyatlari:*\\n\\n"
            "1️⃣ *Arizalar Tizimi*: Talabalar o'qishini ko'chirish, hujjat topshirish va boshqa arizalarni onlayn yuborishadi.\\n"
            "2️⃣ *Jonli Efir (WebRTC)*: Tizim ichida real-vaqtda video darslar yoki jonli efirlar tashkil qilish imkoniyati.\\n"
            "3️⃣ *Real-vaqtda Chat*: Talabalar va operatorlar o'rtasida reaksiyalar va stikerlarni qo'llab-quvvatlovchi jonli chat.\\n"
            "4️⃣ *Kontrakt Nazorati*: Buxgalteriya va talaba to'lovlarini avtomatlashtirilgan monitoring qilish.\\n"
            "5️⃣ *Ommaviy Excel Import*: Fakultet, mutaxassislik va talabalar ro'yxatini Excel orqali bir necha soniyada yuklash.\\n"
            "6️⃣ *Yuqori Xavfsizlik*: Brute-force hujumlaridan himoya va tizimni avtomatlashtirilgan xavfsizlik skaneri.\\n"
            "7️⃣ *Dinamik CMS*: Sayt logotipi, sahifalar matnlari va sozlamalarini admin paneldan oson o'zgartirish."
        )
        send_message(chat_id, features_text)

    elif text == "📱 Mobil Ilova":
        app_text = (
            "📱 *Android Mobil Ilova (Capacitor)*\\n\\n"
            "Tizimdan telefon orqali yanada qulayroq foydalanish uchun Android APK tayyorlangan!\\n\\n"
            "📥 *Ilova imkoniyatlari:*\\n"
            "• Push-bildirishnomalar\\n"
            "• Oflayn rejimda ishlash (Internet uzilganda ma'lumotlar navbati)\\n"
            "• Tezkor yuklanish va qulay interfeys\\n\\n"
            "Ilovani yuklab olish uchun adminstrator bilan bog'laning."
        )
        send_message(chat_id, app_text)

    elif text == "📞 Aloqa / Yordam":
        contact_text = (
            "📞 *Biz bilan aloqa*\\n\\n"
            "Savollar, takliflar yoki tizimni o'rnatish bo'yicha yordam kerakmi?\\n\\n"
            "👤 *Telegram:* @your_support\\n"
            "📧 *Email:* support@example.com\\n\\n"
            "✍️ Bizga yozing, sizga tez fursatda yordam beramiz!"
        )
        send_message(chat_id, contact_text)

    else:
        unknown_text = "🤷‍♂️ Kechirasiz, bu buyruqni tushunmadim. Iltimos, menyu tugmalaridan foydalaning."
        send_message(chat_id, unknown_text, get_main_keyboard())

def main():
    if not TOKEN:
        return

    print("🤖 Telegram Bot ishga tushdi... (Ctrl+C bilan to'xtatish)")
    offset = None
    
    while True:
        try:
            updates = get_updates(offset)
            if updates and updates.get("ok"):
                for update in updates.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update:
                        handle_message(update["message"])
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🤖 Bot faoliyati to'xtatildi.")
            break
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
