# Mini Hemis - Internetdan Ochiq Qilish Qo'llanmasi

## Kerakli Narsalar
- Kompyuterda Mini Hemis proekti
- Internet ulanishi
- Terminal/Command Line

---

## USUL 1: Ngrok (Eng Oson va Tezkor)

### 1-Qadam: Ngrok Yuklab Olish
```bash
# Ngrok yuklab olish
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xf ngrok-v3-stable-linux-amd64.tgz
```

### 2-Qadam: Ngrok Authtoken Olish
1. [ngrok.com](https://ngrok.com) ga kirib ro'yxatdan o'ting
2. Dashboarddan authtoken oling
3. Tokenni qo'llang:
```bash
./ngrok authtoken YOUR_TOKEN_HERE
```

### 3-Qadam: Django Serverini Ishga Tushirish
```bash
cd /home/riva/mini_hemis
python manage.py runserver 0.0.0.0:8000
```

### 4-Qadam: Ngrok Tunnel Ochish
Yangi terminalda:
```bash
./ngrok http 8000
```

### 5-Qadam: Saytni Ko'rish
Ngrok sizga shunday URL beradi:
```
https://random-name.ngrok.io
```

Bu URL orqali istalgan joydan saytingizga kirishingiz mumkin!

---

## USUL 2: Cloudflare Tunnel (Bepul)

### 1-Qadam: Cloudflared Yuklab Olish
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### 2-Qadam: Cloudflare Account Ga Kirish
```bash
cloudflared tunnel login
```

### 3-Qadam: Tunnel Yaratish
```bash
cloudflared tunnel --url http://localhost:8000
```

---

## USUL 3: Port Forwarding (Router orqali)

### 1-Qadam: Django uchun Sozlamalar
**settings.py ni oching:**
```python
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']
```

### 2-Qadam: Serverni Ishga Tushirish
```bash
python manage.py runserver 0.0.0.0:8000
```

### 3-Qadam: Router Sozlamalari
1. Router admin paneliga kirish (odatda 192.168.1.1)
2. "Port Forwarding" bo'limini toping
3. Qo'shing:
   - External Port: 8000
   - Internal Port: 8000
   - IP: Sizning kompyuteringiz IP manzili

### 4-Qadam: Tashqi IP ni Topish
```bash
curl ifconfig.me
```

### 5-Qadam: Saytni Ko'rish
Browserda: `http://YOUR_IP:8000`

---

## Xavfsizlik Uchun Muhim Sozlamalar

### Production Uchun settings.py
```python
# Xavfsizlik sozlamalari
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'localhost']

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/path/to/static/'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mini_hemis',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Gunicorn Ishga Tushirish
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 mini_hemis.wsgi:application
```

---

## Test Uchun Eng Yaxshi Usul

**Ngrok bilan to'liq test:**
```bash
# 1-terminal
cd /home/riva/mini_hemis
python manage.py runserver 0.0.0.0:8000

# 2-terminal
./ngrok http 8000
```

Bu usul bilan:
- Xavfsiz HTTPS olish
- Tezda o'rnatish
- Hech qanday router sozlamlarisiz
- Mobile telefonlarda ham ishlaydi

---

## Qollanma

| Usul | Qiyinlik | Xavfsizlik | Tezlik |
|------|----------|------------|--------|
| Ngrok | Oson | Yaxshi | Tez |
| Cloudflare | Oson | Juda Yaxshi | Tez |
| Port Forwarding | Qiyin | Yomon | O'rtacha |

**Boshlang'ich uchun Ngrok eng yaxshi tanlov!**

---

## Muammolar va Yechimlar

### "Connection Refused" xatosi
```bash
# Django server to'g'ri ishlayotganini tekshiring
curl http://localhost:8000
```

### "Invalid Host" xatosi
```python
# settings.py da qo'shing
ALLOWED_HOSTS = ['*']
```

### Firewall muammosi
```bash
# 8000 port ochish
sudo ufw allow 8000
```

---

## Muvaffaqiyat Testi

Saytni ochilgandan so'ng quyidagilarni tekshiring:
1. Login ishlaydimi?
2. Chat ishlaydimi?
3. Static files yuklanadimi?
4. Mobile versiyada ishlaydimi?

Hammasi ishlasa, tabriklayman! Endi saytingiz internetdan ochiq!
