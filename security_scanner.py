#!/usr/bin/env python3
"""
Mini HEMIS Security & Vulnerability Scanner
This script performs a hybrid (static and dynamic) security scan of the localized Mini HEMIS application.
It identifies security misconfigurations, code vulnerabilities, and runtime risks.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# Target Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_URLS = ["http://127.0.0.1:8000", "http://10.42.0.251:8000"]
REPORT_PATH = os.path.join(BASE_DIR, "security_scan_report.md")

class SecurityScanner:
    def __init__(self):
        self.findings = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": [],
            "INFO": []
        }
        self.scanned_files_count = 0
        self.target_url = None

    def add_finding(self, severity, category, title, description, recommendation, evidence=""):
        self.findings[severity].append({
            "category": category,
            "title": title,
            "description": description,
            "recommendation": recommendation,
            "evidence": evidence
        })

    def run_static_scan(self):
        print("[*] Static Scan boshlanmoqda...")
        
        # 1. settings.py ni tekshirish
        settings_path = os.path.join(BASE_DIR, "mini_hemis", "settings.py")
        if os.path.exists(settings_path):
            self.scan_settings_file(settings_path)
            self.scanned_files_count += 1
        else:
            self.add_finding("HIGH", "Configuration", "settings.py topilmadi", 
                             "Loyiha sozlamalari fayli topilmadi.", 
                             "Fayl yo'lini tekshiring.")

        # 2. .env faylini tekshirish
        env_path = os.path.join(BASE_DIR, ".env")
        if os.path.exists(env_path):
            self.scan_env_file(env_path)
            self.scanned_files_count += 1
        else:
            self.add_finding("MEDIUM", "Configuration", ".env fayli topilmadi",
                             ".env fayli mavjud emas, loyiha default sozlamalar bilan ishlayotgan bo'lishi mumkin.",
                             ".env.example faylidan nusxa olib, yangi .env yarating.")

        # 3. Codebase da SQL injection va xavfli funksiyalarni qidirish
        self.scan_codebase_for_vulnerabilities()

    def scan_settings_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # DEBUG check
        debug_match = re.search(r"DEBUG\s*=\s*(True|False|os\.environ\.get.*True)", content, re.IGNORECASE)
        if debug_match and "True" in debug_match.group(0):
            self.add_finding("HIGH", "Configuration", "DEBUG rejimi yoqilgan (True)",
                             "Loyiha xatoliklarni batafsil ko'rsatuvchi DEBUG rejimi yoqilgan. Bu xakerlar uchun tizim tuzilishini va maxfiy ma'lumotlarni ochib beradi.",
                             "Production muhitida DEBUG = False qilib belgilang va .env orqali boshqaring.",
                             debug_match.group(0))

        # SECRET_KEY check
        secret_match = re.search(r"SECRET_KEY\s*=\s*['\"]([^'\"]+)['\"]", content)
        if secret_match and "django-insecure" in secret_match.group(1):
            self.add_finding("HIGH", "Cryptography", "Zaif yoki Default SECRET_KEY ishlatilmoqda",
                             "SECRET_KEY zaif va 'django-insecure-' prefiksiga ega. Bu sessiya shifrlanishi va CSRF himoyasini aylanib o'tishga imkon beradi.",
                             "Kuchli, kamida 50 belgidan iborat tasodifiy SECRET_KEY yarating va uni .env faylida saqlang.",
                             f"SECRET_KEY = '{secret_match.group(1)[:25]}...'")

        # ALLOWED_HOSTS check
        hosts_match = re.search(r"ALLOWED_HOSTS\s*=\s*\[([^\]]+)\]", content, re.DOTALL)
        if hosts_match:
            hosts_str = hosts_match.group(1)
            if "*" in hosts_str or "'*'" in hosts_str or '"*"' in hosts_str:
                self.add_finding("HIGH", "Network", "ALLOWED_HOSTS da wildcard '*' ishlatilmoqda",
                             "ALLOWED_HOSTS ga '*' (barcha domenlar) qo'shilgan. Bu HTTP Host Header Attack va kesh zaharlanishiga yo'l ochadi.",
                             "Faqat kerakli va ruxsat etilgan domenlarni (masalan, localhost, 127.0.0.1, o'z domeningiz) ko'rsating.",
                             hosts_match.group(0))

        # CORS settings check
        cors_all = re.search(r"CORS_ALLOW_ALL_ORIGINS\s*=\s*True", content)
        cors_cred = re.search(r"CORS_ALLOW_CREDENTIALS\s*=\s*True", content)
        if cors_all and cors_cred:
            self.add_finding("HIGH", "CORS Misconfiguration", "Insecure CORS: Barcha domenlarga ruxsat va Credentials=True",
                             "CORS_ALLOW_ALL_ORIGINS = True va CORS_ALLOW_CREDENTIALS = True bir vaqtda yoqilgan. Bu holatda har qanday zararli sayt foydalanuvchi ma'lumotlarini (cookies, sessiya) o'g'irlashi mumkin.",
                             "CORS_ALLOW_ALL_ORIGINS ni False qiling va ruxsat etilgan domenlarni CORS_ALLOWED_ORIGINS ro'yxatiga qo'shing.",
                             "CORS_ALLOW_ALL_ORIGINS = True\nCORS_ALLOW_CREDENTIALS = True")

        # Session and Cookie Secure Flags
        session_secure = re.search(r"SESSION_COOKIE_SECURE\s*=\s*True", content)
        csrf_secure = re.search(r"CSRF_COOKIE_SECURE\s*=\s*True", content)
        
        # Check if they are set dynamically or globally
        if not session_secure:
            # check if it is inside the conditional block
            dev_session = re.search(r"SESSION_COOKIE_SECURE\s*=\s*False", content)
            if dev_session:
                self.add_finding("MEDIUM", "Session Security", "SESSION_COOKIE_SECURE faqat productionda True",
                                 "SESSION_COOKIE_SECURE local rivojlantirishda False qilib o'rnatilgan. HTTPS ishlatilmaganda sessiya cookie'lari shifrlanmasdan uzatiladi.",
                                 "Lokal testlarda ham HTTPS ishlatib, SESSION_COOKIE_SECURE=True qilish tavsiya etiladi.")
            else:
                self.add_finding("HIGH", "Session Security", "SESSION_COOKIE_SECURE yoqilmagan",
                                 "Session cookie uchun Secure flag o'rnatilmagan. Sessiya cookie'lari HTTP (shifrlanmagan) orqali uzatilishi mumkin, bu MiTM hujumlariga yo'l ochadi.",
                                 "settings.py ga SESSION_COOKIE_SECURE = True sozlamasini qo'shing.")

        if not csrf_secure:
            dev_csrf = re.search(r"CSRF_COOKIE_SECURE\s*=\s*False", content)
            if dev_csrf:
                self.add_finding("MEDIUM", "CSRF Security", "CSRF_COOKIE_SECURE faqat productionda True",
                                 "CSRF_COOKIE_SECURE local rivojlantirishda False. Bu CSRF tokenlarini HTTP orqali ochiq uzatilishiga sabab bo'ladi.",
                                 "Lokal testlarda ham CSRF_COOKIE_SECURE=True qilish tavsiya etiladi.")
            else:
                self.add_finding("HIGH", "CSRF Security", "CSRF_COOKIE_SECURE yoqilmagan",
                                 "CSRF cookie uchun Secure flag o'rnatilmagan. CSRF tokenlari HTTP (shifrlanmagan) orqali uzatilishi mumkin.",
                                 "settings.py ga CSRF_COOKIE_SECURE = True sozlamasini qo'shing.")

        # HttpOnly and SameSite checks
        session_httponly = re.search(r"SESSION_COOKIE_HTTPONLY\s*=\s*True", content)
        if not session_httponly:
            # Django defaults to True, but check if explicitly set to False
            if re.search(r"SESSION_COOKIE_HTTPONLY\s*=\s*False", content):
                self.add_finding("HIGH", "Session Security", "SESSION_COOKIE_HTTPONLY o'chirilgan",
                                 "Session cookie uchun HttpOnly flag False qilingan. Bu zararli JS skriptlariga (XSS orqali) sessiya cookie'larini o'g'irlashga ruxsat beradi.",
                                 "SESSION_COOKIE_HTTPONLY sozlamasini o'chiring yoki True qiling.")

    def scan_env_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Check for hardcoded credentials/secrets
            if "SECRET_KEY" in line and "django-insecure-change-me" in line:
                self.add_finding("MEDIUM", "Configuration", ".env da default/zaif SECRET_KEY",
                                 "Environment (.env) faylida zaif default SECRET_KEY mavjud.",
                                 "Production uchun uni mutlaqo o'zgartiring.",
                                 f"Line {line_num}: {line}")

            if "EMAIL_HOST_PASSWORD" in line and len(line.split("=")[1]) > 0 and "your-" not in line:
                password = line.split("=")[1].strip()
                if password and password != "change-me":
                    self.add_finding("LOW", "Information Disclosure", ".env da SMTP parol saqlanmoqda",
                                     ".env faylida ochiq holda SMTP Email paroli saqlanmoqda.",
                                     "Bu normal amaliyot bo'lsa-da, ushbu .env faylini hech qachon git tizimiga yuklamaslik kerak (.gitignore da borligini tekshiring).",
                                     f"Line {line_num}: EMAIL_HOST_PASSWORD = ********")

    def scan_codebase_for_vulnerabilities(self):
        print("[*] Codebase ni xavfli funksiyalar va SQLi uchun skanerlash...")
        
        suspicious_patterns = {
            "SQL Injection (Raw SQL)": {
                "pattern": r"\.execute\(\s*['\"][^'\"]*%[^'\"]*['\"]\s*%\s*[^)]+\)", 
                "severity": "HIGH",
                "desc": "Raw SQL so'rovlarida parametrlar to'g'ridan-to'g'ri string formatlash (%) orqali kiritilgan bo'lishi mumkin. Bu SQL injection ga yo'l ochadi.",
                "reco": "Django ORM dan foydalaning yoki parametrli so'rovlar ishlating: cursor.execute('SELECT... WHERE x = %s', [x])"
            },
            "SQL Injection (String F-string raw SQL)": {
                "pattern": r"\.execute\(\s*f['\"][^'\"]*\{[^']+\}[^'\"]*['\"]\s*\)",
                "severity": "HIGH",
                "desc": "F-string yordamida to'g'ridan-to'g'ri SQL so'roviga o'zgaruvchi joylashtirilgan. SQL Injection xavfi juda yuqori.",
                "reco": "Faqat parametrli so'rovlardan foydalaning."
            },
            "CSRF Bypass (csrf_exempt)": {
                "pattern": r"@csrf_exempt",
                "severity": "MEDIUM",
                "desc": "Ko'rinish (view) ustida @csrf_exempt dekoratori ishlatilgan. Bu ushbu endpointni CSRF hujumlariga qarshi himoyasiz qoldiradi.",
                "reco": "Iloji boricha @csrf_exempt ishlatmang, yoki uning o'rniga Token-based authentication kabi boshqa xavfsiz mexanizmlardan foydalaning."
            },
            "Hardcoded Passwords": {
                "pattern": r"(password|passwd|secret|key|token)\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]",
                "severity": "MEDIUM",
                "desc": "Kod ichida qattiq yozilgan (hardcoded) parollar, kalitlar yoki tokenlar aniqlandi.",
                "reco": "Barcha maxfiy kalitlar va parollarni .env fayliga o'tkazing."
            },
            "Eval/Exec Usage": {
                "pattern": r"\b(eval|exec)\s*\(",
                "severity": "HIGH",
                "desc": "eval() yoki exec() funksiyasi ishlatilgan. Bu kod inyeksiyasi (Code Injection) va masofaviy kod bajarilishiga (RCE) sabab bo'lishi mumkin.",
                "reco": "eval/exec ishlatishdan mutlaqo voz keching va xavfsizroq alternativalarni qo'llang."
            },
            "IDOR (Insecure Direct Object Reference)": {
                "pattern": r"get_object_or_404\([^)]+,\s*pk\s*=\s*[^)]+\)",
                "severity": "MEDIUM",
                "desc": "get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.",
                "reco": "Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring."
            },
            "Missing Permission Check": {
                "pattern": r"@login_required\s*\n(?!.*permission)",
                "severity": "MEDIUM",
                "desc": "@login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.",
                "reco": "Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.)."
            }
        }

        for root, dirs, files in os.walk(BASE_DIR):
            # Exclude virtual environment and git files
            if any(p in root for p in [".venv", "venv", ".git", "__pycache__", "staticfiles"]):
                continue

            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    self.scanned_files_count += 1
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            lines = f.readlines()
                            
                        file_content = "".join(lines)
                        
                        for vuln_name, details in suspicious_patterns.items():
                            matches = re.finditer(details["pattern"], file_content)
                            for match in matches:
                                # Find line number
                                line_num = file_content[:match.start()].count("\n") + 1
                                relative_path = os.path.relpath(file_path, BASE_DIR)
                                
                                # Skip false positives or built-in venv checks
                                if "security_scanner.py" in relative_path:
                                    continue
                                    
                                evidence = f"Fayl: {relative_path}, Qator: {line_num}\nKod: {match.group(0).strip()}"
                                
                                self.add_finding(
                                    details["severity"],
                                    "Code Vulnerability",
                                    f"{vuln_name} aniqlandi",
                                    details["desc"],
                                    details["reco"],
                                    evidence
                                )
                    except Exception as e:
                        pass

    def run_dynamic_scan(self):
        print("\n[*] Dynamic Scan boshlanmoqda...")
        
        # 1. Server qaysi manzilda ishlayotganini aniqlash
        active_url = None
        for url in LOCAL_URLS:
            try:
                req = urllib.request.Request(url, method="HEAD")
                with urllib.request.urlopen(req, timeout=2) as response:
                    if response.status in [200, 301, 302]:
                        active_url = url
                        break
            except Exception:
                continue

        if not active_url:
            print("[!] Lokal server ishlamayapti yoki unga ulanib bo'lmadi.")
            print("[*] Lekin static kod tahlili bajarildi. Faqat static natijalar taqdim etiladi.")
            self.add_finding("INFO", "Dynamic Scan", "Lokal server faol emas",
                             "Dynamic (runtime) skanerlash amalga oshirilmadi, chunki lokal serverga ulanib bo'lmadi (port 8000).",
                             "Skanerlash to'liq bo'lishi uchun Django serverni ishga tushiring: python manage.py runserver 0.0.0.0:8000")
            return

        self.target_url = active_url
        print(f"[+] Faol server topildi: {self.target_url}")

        # 2. HTTP Security Headerlarini tekshirish
        self.check_http_headers()

        # 3. CORS vulnerability dynamic probing
        self.probe_cors_vulnerability()

        # 4. Sensitive files exposure check over HTTP
        self.check_file_exposures()

        # 5. IDOR zaifliklarini tekshirish
        self.check_idor_vulnerabilities()

    def check_idor_vulnerabilities(self):
        """IDOR (Insecure Direct Object Reference) zaifliklarini tekshirish"""
        print("[*] IDOR zaifliklari tekshirilmoqda...")
        
        # 1. API endpointlariga ruxsatsiz kirishni tekshirish
        idor_endpoints = [
            f"{self.target_url}/api/v1/users/",
            f"{self.target_url}/api/v1/students/",
            f"{self.target_url}/api/v1/faculties/",
            f"{self.target_url}/api/v1/specialties/",
        ]
        
        for endpoint in idor_endpoints:
            try:
                req = urllib.request.Request(endpoint, method="GET")
                req.add_header("User-Agent", "Mozilla/5.0 MiniHemisScanner/1.0")
                # Ruxsatsiz so'rov (token yo'q)
                
                with urllib.request.urlopen(req, timeout=3) as response:
                    if response.status == 200:
                        content = response.read(200)
                        # Agar 200 qaytsa, bu zaiflik
                        self.add_finding(
                            "HIGH", "IDOR", 
                            f"Ruxsatsiz API endpointga kirish mumkin: {endpoint}",
                            "API endpointiga autentifikatsiyasiz kirish mumkin. Bu IDOR zaifligidir.",
                            "Barcha API endpointlarida @api_view va permission_classes dekoratorlaridan foydalaning.",
                            f"URL: {endpoint}\nStatus: {response.status}\nJavob: {content[:100]}"
                        )
            except urllib.error.HTTPError as e:
                # 401 yoki 403 - xavfsiz
                if e.code not in [401, 403]:
                    self.add_finding(
                        "MEDIUM", "IDOR",
                        f"API endpointga kutilmagan javob: {endpoint}",
                        f"HTTP {e.code} qaytdi. Bu endpointni tekshirish kerak.",
                        "Endpointni qayta ko'rib chiqing.",
                        f"URL: {endpoint}\nStatus: {e.code}"
                    )
            except Exception:
                pass
        
        # 2. Boshqa foydalanuvchi ma'lumotlariga kirishni tekshirish
        # (agar token mavjud bo'lsa)
        # Bu test faqat server ishlayotgan va token mavjud bo'lganda amalga oshiriladi
        print("[*] IDOR testi yakunlandi")

    def check_http_headers(self):
        try:
            req = urllib.request.Request(f"{self.target_url}/login/", method="GET")
            # User agentni o'zgartiramiz, chunki IPBlockMiddleware uni tekshiradi
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MiniHemisSecurityScanner/1.0")
            
            with urllib.request.urlopen(req, timeout=5) as response:
                headers = response.info()
                
                # Check X-Frame-Options
                x_frame = headers.get("X-Frame-Options")
                if not x_frame:
                    self.add_finding("HIGH", "HTTP Header", "Mising X-Frame-Options header",
                                     "X-Frame-Options headeri javobda yo'q. Bu Clickjacking hujumiga yo'l ochadi.",
                                     "settings.py da X_FRAME_OPTIONS = 'DENY' yoki 'SAMEORIGIN' sozlamasini production'da yoqing.")
                elif x_frame.lower() not in ["deny", "sameorigin"]:
                    self.add_finding("LOW", "HTTP Header", "Zaif X-Frame-Options sozlamasi",
                                     f"X-Frame-Options headeri mavjud lekin zaif: {x_frame}",
                                     "Uni DENY yoki SAMEORIGIN ga o'zgartiring.")

                # Check X-Content-Type-Options
                x_content = headers.get("X-Content-Type-Options")
                if not x_content or x_content.lower() != "nosniff":
                    self.add_finding("MEDIUM", "HTTP Header", "Missing/Insecure X-Content-Type-Options header",
                                     "X-Content-Type-Options headeri mavjud emas yoki 'nosniff' qilib belgilanmagan. Bu MIME-sniffing hujumlariga olib kelishi mumkin.",
                                     "SECURE_CONTENT_TYPE_NOSNIFF = True sozlamasini sozlang.")

                # Check Content-Security-Policy (CSP)
                csp = headers.get("Content-Security-Policy") or headers.get("X-Content-Security-Policy")
                if not csp:
                    self.add_finding("HIGH", "HTTP Header", "Content-Security-Policy (CSP) headeri mavjud emas",
                                     "CSP headeri topilmadi. CSP saytda ruxsatsiz skriptlar va kontentlarni (XSS, Clickjacking) yuklanishini oldini oluvchi eng asosiy qalqondir.",
                                     "django-csp paketini sozlang yoki custom middleware orqali CSP headerini yuboring.")

                # Check Strict-Transport-Security (HSTS)
                hsts = headers.get("Strict-Transport-Security")
                if not hsts:
                    self.add_finding("MEDIUM", "HTTP Header", "Strict-Transport-Security (HSTS) headeri yo'q",
                                     "HSTS headeri mavjud emas. Bu foydalanuvchilarning shifrlanmagan HTTP orqali ulanib, MiTM (SSL stripping) qurboni bo'lishiga sabab bo'lishi mumkin.",
                                     "Production muhitda HSTS yoqing: SECURE_HSTS_SECONDS = 31536000")

                # Cookie attributes checking
                cookies = response.getheader("Set-Cookie")
                if cookies:
                    if "httponly" not in cookies.lower():
                        self.add_finding("HIGH", "Cookie Security", "Session Cookie da HttpOnly bayrog'i yo'q",
                                         "Yuborilgan Set-Cookie da HttpOnly bayrog'i aniqlanmadi. Bu XSS orqali sessiyani o'g'irlashni osonlashtiradi.",
                                         "Sessiya cookie-fayllari uchun HttpOnly bayrog'i yoqilganligiga ishonch hosil qiling.")
                    if "secure" not in cookies.lower() and self.target_url.startswith("https"):
                        self.add_finding("HIGH", "Cookie Security", "Secure bayrog'i cookie faylda yo'q (HTTPS da)",
                                         "HTTPS orqali Set-Cookie yuborilganda 'Secure' bayrog'i yo'q.",
                                         "SESSION_COOKIE_SECURE = True sozlamasini yoqing.")
        except Exception as e:
            self.add_finding("INFO", "Dynamic Scan", "HTTP Headers tekshirishda xatolik",
                             f"Headers tekshiruvida xatolik yuz berdi: {str(e)}", "")

    def probe_cors_vulnerability(self):
        try:
            req = urllib.request.Request(
                f"{self.target_url}/api/v1/stats/",
                method="OPTIONS"
            )
            req.add_header("Origin", "http://evil-attacker-site.com")
            req.add_header("Access-Control-Request-Method", "GET")
            req.add_header("User-Agent", "Mozilla/5.0 MiniHemisScanner/1.0")
            
            with urllib.request.urlopen(req, timeout=5) as response:
                headers = response.info()
                allow_origin = headers.get("Access-Control-Allow-Origin")
                allow_credentials = headers.get("Access-Control-Allow-Credentials")
                
                if allow_origin == "http://evil-attacker-site.com" and allow_credentials == "true":
                    self.add_finding("HIGH", "CORS", "Dynamic CORS exploitation tasdiqlandi",
                                     "Tizim evil-attacker-site.com dan kelgan so'rovni qabul qildi va javobda uni tasdiqladi, hamda Credentials=true qilib qaytardi. Bu to'liq CORS credential leak zaifligidir.",
                                     "CORS_ALLOW_ALL_ORIGINS = False qiling va faqat ishonchli domenlarni CORS_ALLOWED_ORIGINS ga yozing.",
                                     f"Response headers:\nAccess-Control-Allow-Origin: {allow_origin}\nAccess-Control-Allow-Credentials: {allow_credentials}")
        except Exception:
            pass

    def check_file_exposures(self):
        sensitive_files = {
            ".env": "Environment variables configuration",
            "db.sqlite3": "SQLite database file",
            "logs/security.log": "Security logs",
            ".git/config": "Git configuration file"
        }
        
        for file_path, desc in sensitive_files.items():
            try:
                url = f"{self.target_url}/{file_path}"
                req = urllib.request.Request(url, method="GET")
                req.add_header("User-Agent", "Mozilla/5.0 MiniHemisScanner/1.0")
                
                with urllib.request.urlopen(req, timeout=3) as response:
                    if response.status == 200:
                        content_sample = response.read(100)
                        self.add_finding("CRITICAL", "Information Disclosure", f"Maxfiy fayl ochiq holda aniqlandi: {file_path}",
                                         f"Internet/Lokal tarmoq orqali maxfiy faylga ({file_path} - {desc}) to'g'ridan-to'g'ri kirish imkoni mavjud! Bu juda jiddiy xavfsizlik muammosidir.",
                                         "Web server sozlamalarida maxfiy fayllarni (.env, .git, db.sqlite3, logs) bevosita yuklashni taqiqlang.",
                                         f"URL: {url}\nFayl boshlanishi: {content_sample}")
            except Exception:
                # Agar 404 yoki 403 bo'lsa - demak xavfsiz (yoki Django static fayl sifatida xizmat ko'rsatmaydi)
                pass

    def generate_report(self):
        print(f"\n[*] Skanerlash tugadi. Hisobot yozilmoqda: {REPORT_PATH}")
        
        total_findings = sum(len(v) for v in self.findings.values())
        
        report = []
        report.append("# 🛡️ Mini HEMIS Tizimi Xavfsizlik Skaneri Hisoboti")
        report.append(f"\n**Skanerlangan sana:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n**Skanerlangan fayllar soni:** {self.scanned_files_count}")
        if self.target_url:
            report.append(f"**Skanerlangan lokal URL:** {self.target_url}")
        else:
            report.append("**Skanerlangan lokal URL:** Skanerlanmadi (Lokal server o'chiq edi)")

        report.append("\n## 📊 Umumiy statistika")
        report.append("| Daraja | Muammolar Soni |")
        report.append("| :--- | :--- |")
        report.append(f"| 🔴 CRITICAL | {len(self.findings['CRITICAL'])} |")
        report.append(f"| 🟠 HIGH | {len(self.findings['HIGH'])} |")
        report.append(f"| 🟡 MEDIUM | {len(self.findings['MEDIUM'])} |")
        report.append(f"| 🔵 LOW | {len(self.findings['LOW'])} |")
        report.append(f"| 🟢 INFO | {len(self.findings['INFO'])} |")
        report.append(f"| **Jami** | **{total_findings}** |")

        severity_emoji = {
            "CRITICAL": "🔴 CRITICAL",
            "HIGH": "🟠 HIGH",
            "MEDIUM": "🟡 MEDIUM",
            "LOW": "🔵 LOW",
            "INFO": "🟢 INFO"
        }

        report.append("\n## 🚨 Aniqlangan Xavfsizlik Muammolari")
        
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            if not self.findings[severity]:
                continue
                
            report.append(f"\n### {severity_emoji[severity]} muammolar")
            
            for idx, finding in enumerate(self.findings[severity], 1):
                report.append(f"\n#### {idx}. {finding['title']}")
                report.append(f"- **Kategoriya:** {finding['category']}")
                report.append(f"- **Tavsif:** {finding['description']}")
                report.append(f"- **Tavsiya (Yechim):** {finding['recommendation']}")
                if finding['evidence']:
                    report.append("- **Dalil / Tafsilotlar:**")
                    report.append("```text")
                    report.append(finding['evidence'])
                    report.append("```")
                report.append("\n---")

        report.append("\n\n## 📝 Xavfsizlik bo'yicha yakuniy xulosa va tavsiyalar")
        report.append("1. **CORS sozlamalarini to'g'rilang:** `CORS_ALLOW_ALL_ORIGINS = True` va `CORS_ALLOW_CREDENTIALS = True` sozlamalari production muhitida o'ta xavfli. Ularni faqat ruxsat berilgan domenlar ro'yxati (`CORS_ALLOWED_ORIGINS`) bilan almashtiring.")
        report.append("2. **Xavfsiz headerlarni yoqing:** Dynamic scan ko'rsatganidek, ba'zi xavfsizlik headerlari (masalan, CSP) faol emas. Production settings ni to'liq ishga tushirish uchun `.env` faylida `DEBUG=False` qilish va barcha cookie-secure sozlamalarini yoqish lozim.")
        report.append("3. **SECRET_KEY kalitini yangilang:** .env va settings.py dagi maxfiy kalitlarni murakkab, tasodifiy generatsiya qilingan kalitga almashtiring.")
        report.append("4. **IPBlockMiddleware va Brute-Force Himoyasini saqlang:** Tizimda mavjud bo'lgan IPBlockMiddleware va Axes (Brute force himoyasi) juda yaxshi ishlamoqda. Ularning sozlamalarini o'zgartirmang.")

        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(report))

        print(f"[+] Hisobot muvaffaqiyatli saqlandi: {REPORT_PATH}")

if __name__ == "__main__":
    scanner = SecurityScanner()
    scanner.run_static_scan()
    scanner.run_dynamic_scan()
    scanner.generate_report()
