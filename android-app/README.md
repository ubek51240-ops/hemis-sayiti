# 📱 Test-sinov-ucun - Android APK

Bu loyiha Capacitor asosida sayt ni Android ilovaga o'rab beradi.

## 🎯 Xususiyatlari

- ✅ Saytni to'g'ridan-to'g'ri ilova ichida ochadi (`capacitor.config.json` → `server.url`)
- ✅ Offline cache (Service Worker)
- ✅ Offline forma navbati (IndexedDB)
- ✅ Internet kelganda avtomatik sync
- ✅ Native back button
- ✅ Native network status listener

## 📋 Talablar (APK qurish uchun)

Kompyuterda:
- **Node.js 18+** ✓ (o'rnatilgan)
- **Android Studio** ([yuklab olish](https://developer.android.com/studio))
- **JDK 17** (Android Studio ichida keladi)
- **Android SDK** (Android Studio o'rnatganda sozlanadi)

## 🚀 APK qurish - bosqichma-bosqich

### 1. Server URL ni sozlash

`capacitor.config.json` faylini oching va `server.url` ni o'zgartiring:

```json
"server": {
  "url": "https://sizning-saytingiz.com"
}
```

**Muhim**: HTTPS bo'lishi shart (yoki `cleartext: true` bilan HTTP).

Development uchun ngrok ishlating yoki production saytingiz URL sini bering.

### 2. Asset sync

```bash
cd android-app
npx cap sync android
```

### 3. Android Studio'da ochish

```bash
npx cap open android
```

Bu Android Studio ni ochadi (agar o'rnatgan bo'lsangiz).

### 4. APK build

Android Studio ichida:
- Menu → **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
- Yoki terminal orqali:

```bash
cd android
./gradlew assembleDebug
```

APK fayl quyidagi joyda yaratiladi:
```
android-app/android/app/build/outputs/apk/debug/app-debug.apk
```

### 5. Telefonga o'rnatish

1. Telefonda **Settings** → **Security** → **Unknown sources** ni yoqing
2. APK faylni telefonga ko'chiring (USB, Telegram, email va h.k.)
3. APK faylni toping va oching
4. "Install" tugmasini bosing

## 🔧 Sozlamalar

### App nomi va ID o'zgartirish
`capacitor.config.json`:
```json
{
  "appId": "uz.talabaqabul.app",
  "appName": "Test-sinov-ucun"
}
```

### Icon va Splash screen

Android Studio ichida:
- `android/app/src/main/res/mipmap-*` - ilova ikonasi
- `android/app/src/main/res/drawable-*` - splash screen

Yoki `@capacitor/assets` ishlatib avtomatik yaratish:

```bash
npm i -D @capacitor/assets
# icon.png (1024x1024) ni android-app/resources/ ga qo'ying
npx capacitor-assets generate --android
```

## 🌐 Production uchun

1. **Signing key yaratish**:
```bash
keytool -genkey -v -keystore talaba-qabul.keystore \
  -alias talaba-qabul -keyalg RSA -keysize 2048 -validity 10000
```

2. `android/app/build.gradle` ga signing config qo'shing

3. Release APK:
```bash
cd android
./gradlew assembleRelease
```

## 🐛 Troubleshooting

**"server URL not accessible"** - HTTPS bo'lmagan bo'lsa `cleartext: true` qo'shing

**White screen** - `Service-Worker-Allowed` header'ni saytda sozlash kerak

**Offline ishlamayapti** - birinchi marta online bo'lib login qilish kerak (cache uchun)

## 📝 Muhim izoh

Bu ilova **RUN ONLINE-FIRST** yondashuvi bilan ishlaydi:
1. Birinchi ochilganda: internet kerak (sayt yuklanadi va cachelanadi)
2. Login qilingandan keyin: offline ham ishlaydi
3. Offline holatda yozuvlar IndexedDB ga saqlanadi
4. Internet kelganda avtomatik sync
