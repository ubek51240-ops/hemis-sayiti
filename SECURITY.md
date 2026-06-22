# 🔒 Kuchli Xavfsizlik Tizimi

Bu loyiha haker hujumlaridan himoya qilish uchun kuchli xavfsizlik tizimi bilan jihozlangan.

## 🛡️ Himoya Turlari

### 1. **DDoS va Brute-Force Himoyasi**
- **Rate Limiting**: Har bir IP uchun so'rovlar cheklangan
  - Login: 5 ta urinish / 5 daqiqa
  - API: 100 ta so'rov / daqiqa
  - Umumiy: 60 ta so'rov / daqiqa
  - File Upload: 10 ta / daqiqa
- **Django-Axes**: Login urinishlarini kuzatish va bloklash
- **Django-Defender**: Qo'shimcha brute-force himoyasi

### 2. **XSS (Cross-Site Scripting) Himoyasi**
- **Content Security Policy (CSP)**: Faqat o'z manbadan skript yuklash
- **Input Sanitization**: Barcha kiruvchi ma'lumotlarni tozalash
- **Bleach**: HTML teglarni filtrlash
- **X-XSS-Protection**: Brauzer darajasida himoya

### 3. **SQL Injection Himoyasi**
- **Django ORM**: Parametrlangan so'rovlardan foydalanish
- **Input Validation**: Shubhali SQL patternlarni bloklash
- **Input Sanitization**: Maxsus belgilarni filtrlash

### 4. **Clickjacking Himoyasi**
- **X-Frame-Options: DENY**: Saytni iframe ga yuklashni bloklash
- **CSP frame-ancestors**: Qo'shimcha himoya

### 5. **Session va Cookie Xavfsizligi**
- **HttpOnly Cookies**: JavaScript dan cookie'larni yashirish
- **Secure Cookies**: Faqat HTTPS orqali uzatish
- **SameSite=Strict**: CSRF himoyasi
- **Session Timeout**: 30 daqiqa faolsizlikdan keyin avto-chiqish

### 6. **HTTPS va SSL/TLS**
- **HSTS (HTTP Strict Transport Security)**: HTTPS majburiy qilish
- **SSL Redirect**: HTTP dan HTTPS ga avtomatik yo'naltirish
- **Secure Headers**: Xavfsizlik HTTP headerlari

### 7. **IP Bloklash va Monitoring**
- **IPBlockMiddleware**: Shubhali IP manzillarni bloklash
- **Attack Detection**: SQLMap, Nikto, Burp Suite kabi scannerlarni aniqlash
- **Request Logging**: Barcha so'rovlarni log qilish

### 8. **Admin Panel Xavfsizligi**
- **IP Whitelist**: Faqat ruxsat etilgan IP lar admin panelga kira oladi
- **Kuchli Parol Talablari**: 
  - Minimum 12 ta belgi
  - Katta va kichik harflar
  - Raqamlar
  - Maxsus belgilar
- **Brute-force Himoyasi**: Admin uchun qat'iyroq cheklovlar

### 9. **File Upload Xavfsizligi**
- **File Type Validation**: Faqat ruxsat etilgan formatlar
- **File Size Limit**: Maksimum 10 MB
- **Malware Scanning**: Yukiayotgan fayllarni tekshirish

### 10. **Monitoring va Logging**
- **Security Logs**: `logs/security.log`
- **Auth Logs**: `logs/auth.log`
- **Access Attempts**: Barcha kirish urinishlari
- **Rotating Logs**: Avtomatik log aylantirish

## 📋 O'rnatish

### 1. Paketlarni o'rnatish
```bash
pip install -r requirements.txt
```

### 2. `.env` faylini sozlash
```bash
cp .env.example .env
# .env faylini tahrirlang
```

### 3. Xavfsizlik sozlamalarini yangilash
```bash
cp complete_settings.py core/settings.py
```

### 4. Ma'lumotlar bazasini yangilash
```bash
python manage.py migrate
python manage.py migrate defender
```

### 5. Superuser yaratish (kuchli parol bilan)
```bash
python manage.py createsuperuser
```

## ⚙️ Xavfsizlik Sozlamalari

### `settings.py` da quyidagi sozlamalar qo'shilgan:

```python
# Session va Cookie
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Browser Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSP
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
```

## 🔍 Monitoring

### Log fayllari:
- `logs/django.log` - Umumiy loglar
- `logs/security.log` - Xavfsizlik hodisalari
- `logs/auth.log` - Autentifikatsiya urinishlari

### Log ko'rish:
```bash
# Real-time security log
tail -f logs/security.log

# Auth log
tail -f logs/auth.log
```

## 🚨 Xavfsizlik Hodisalari

Agar hujum aniqlansa:
1. **Avtomatik bloklash**: IP manzil 24 soatga bloklanadi
2. **Log yozish**: Barcha ma'lumotlar saqlanadi
3. **Xabar yuborish**: Administratorga xabar yuboriladi (sozlangan bo'lsa)

## 📞 Aloqa

Xavfsizlik muammolari uchun:
- Email: security@yourdomain.com
- Telegram: @your_support

## 📝 Muhim Eslatmalar

1. **SECRET_KEY** ni har doim maxfiy saqlang
2. **DEBUG=False** production'da
3. **HTTPS** ishlatish majburiy
4. **PostgreSQL** ma'lumotlar bazasini ishlating (SQLite emas)
5. **Redis** cache uchun ishlating (mumkin bo'lsa)
6. **AWS S3** fayllar uchun ishlating (mumkin bo'lsa)
7. **Muntazam yangilanishlar** - paketlarni yangilab turing

## ✅ Xavfsizlik Checklist

- [ ] `.env` fayli to'g'ri sozlangan
- [ ] `DEBUG=False` production'da
- [ ] Kuchli `SECRET_KEY` (50+ belgi)
- [ ] HTTPS yoqilgan
- [ ] PostgreSQL ishlatilmoqda
- [ ] Admin whitelist IP sozlangan
- [ ] Loglar muntazam tekshirilmoqda
- [ ] Parollar kuchli (12+ belgi)
- [ ] 2FA yoqilgan (tavsiya etiladi)
- [ ] Muntazam backup olinmoqda

---

**Oxirgi yangilanish**: 2026-05-11
**Versiya**: 2.0 (Kuchli Xavfsizlik)
