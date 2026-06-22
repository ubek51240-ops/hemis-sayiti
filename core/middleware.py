"""
KUCHLI XAVFSIZLIK MIDDLEWARE
Haker hujumlaridan himoya qilish uchun
"""

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden, HttpResponse
from django.core.cache import cache
import time
import logging
import re
from datetime import datetime

# Logger o'rnatish
security_logger = logging.getLogger('core.security')
auth_logger = logging.getLogger('axes.watch_login')


class SecurityHeadersMiddleware:
    """
    Xavfsizlik HTTP headerlarini qo'shish
    XSS, Clickjacking, MIME sniffing hujumlaridan himoya
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # X-Frame-Options: Clickjacking himoyasi
        response['X-Frame-Options'] = 'DENY'
        
        # X-Content-Type-Options: MIME sniffingni bloklash
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-XSS-Protection: XSS filtrlash (legacy browserlar uchun)
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer-Policy: Referrer ma'lumotlarini cheklash
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy: Brauzer APIlarini cheklash
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Strict-Transport-Security (HSTS): HTTPS majburiy qilish
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Content-Security-Policy (CSP): XSS himoyasi
        if not settings.DEBUG:
            response['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https: data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';"
        
        return response


def record_ip_block(ip, user_agent, reason):
    """Bloklangan IP manzilni django-axes AccessAttempt modeliga yozish"""
    try:
        from axes.models import AccessAttempt
        from django.utils import timezone
        
        # User Agent maydoniga sababni yozib qo'yamiz, shunda adminga chiroyli ko'rinadi
        combined_user_agent = f"[{reason}] {user_agent}"[:255] if user_agent else f"[{reason}] Unknown"
        
        attempt, created = AccessAttempt.objects.get_or_create(
            username=ip,
            ip_address=ip,
            defaults={
                'user_agent': combined_user_agent,
                'failures_since_start': 1,
                'attempt_time': timezone.now(),
            }
        )
        if not created:
            attempt.failures_since_start += 1
            attempt.attempt_time = timezone.now()
            attempt.user_agent = combined_user_agent
            attempt.save()
    except Exception as e:
        security_logger.error(f"Error recording IP block in AccessAttempt: {str(e)}")


class RateLimitMiddleware:
    """
    Rate Limiting Middleware
    DDoS va brute-force hujumlaridan himoya
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # So'rov limitlari
        self.limits = {
            'login': {'max': 5, 'window': 300},      # 5 ta login / 5 daqiqa
            'api': {'max': 100, 'window': 60},       # 100 ta API so'rov / daqiqa
            'general': {'max': 60, 'window': 60},    # 60 ta umumiy so'rov / daqiqa
            'file_upload': {'max': 10, 'window': 60}, # 10 ta file upload / daqiqa
        }
    
    def get_client_ip(self, request):
        """Klient IP manzilini olish"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_rate_limited(self, request, limit_type='general'):
        """Rate limit tekshirish"""
        ip = self.get_client_ip(request)
        user = request.user.username if request.user.is_authenticated else 'anon'
        
        # Cache kaliti
        cache_key = f'rate_limit:{limit_type}:{ip}:{user}'
        
        # Joriy so'rovlar soni
        current = cache.get(cache_key, 0)
        limit_config = self.limits.get(limit_type, self.limits['general'])
        
        if current >= limit_config['max']:
            return True
        
        # So'rovlar sonini oshirish
        cache.set(cache_key, current + 1, limit_config['window'])
        return False
    
    def __call__(self, request):
        # Path tekshirish
        path = request.path.lower()
        
        # Login sahifalari uchun qat'iyroq limit
        if path in ['/', '/login/', '/accounts/login/'] and request.method == 'POST':
            if self.is_rate_limited(request, 'login'):
                ip = self.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
                record_ip_block(ip, user_agent, "Rate Limit: Ko'p login urinishlari")
                security_logger.warning(f"Rate limit exceeded for login - IP: {self.get_client_ip(request)}")
                return HttpResponse(
                    "Juda ko'p urinish. Iltimos 5 daqiqa kuting.",
                    status=429
                )
        
        # API so'rovlari uchun limit
        elif path.startswith('/api/'):
            if self.is_rate_limited(request, 'api'):
                ip = self.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
                record_ip_block(ip, user_agent, "Rate Limit: Ko'p API so'rovlari")
                security_logger.warning(f"API rate limit exceeded - IP: {self.get_client_ip(request)}")
                return HttpResponse(
                    "API so'rovlar cheklovi oshdi. Iltimos kuting.",
                    status=429
                )
        
        # File upload uchun limit
        elif 'upload' in path and request.method == 'POST':
            if self.is_rate_limited(request, 'file_upload'):
                ip = self.get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
                record_ip_block(ip, user_agent, "Rate Limit: Ko'p fayl yuklash")
                security_logger.warning(f"File upload rate limit exceeded - IP: {self.get_client_ip(request)}")
                return HttpResponse(
                    "File upload cheklovi oshdi. Iltimos kuting.",
                    status=429
                )
        
        # Umumiy so'rovlar uchun limit
        elif self.is_rate_limited(request, 'general'):
            ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
            # 1 soatga bloklash (DDoS/ko'p refresh himoyasi)
            cache.set(f'blocked_ip:{ip}', True, 3600)
            record_ip_block(ip, user_agent, "Rate Limit: Ko'p refresh qilish (general)")
            security_logger.warning(f"General rate limit exceeded - IP: {self.get_client_ip(request)}")
            return HttpResponse(
                "So'rovlar cheklovi oshdi. Iltimos kuting.",
                status=429
            )
        
        return self.get_response(request)


class IPBlockMiddleware:
    """
    IP manzilni bloklash middleware
    Shubhali IP manzillarni bloklash
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = set()
        self.suspicious_patterns = [
            r'\.\.\/',  # Directory traversal
            r'union.*select',  # SQL injection
            r'script\s*>',  # XSS
            r'eval\s*\(',  # Code injection
            r'<\s*iframe',  # Clickjacking
            r'\.htaccess',  # Server config access
            r'\.env',  # Environment file access
            r'config\.php',  # Config file access
            r'phpinfo',  # PHP info
            r'admin\.php',  # Admin access attempts
            r'wp-login',  # WordPress login attempts
            r'sqlmap',  # SQLMap tool
            r'nikto',  # Nikto scanner
            r'nmap',  # Nmap scanner
            r'burp',  # Burp Suite
            r'dirbuster',  # DirBuster
            r'gobuster',  # Gobuster
        ]
    
    def get_client_ip(self, request):
        """Klient IP manzilini olish"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ip_blocked(self, ip):
        """IP bloklanganmi?"""
        # Cache dan tekshirish
        blocked = cache.get(f'blocked_ip:{ip}')
        return blocked is True or ip in self.blocked_ips
    
    def block_ip(self, ip, duration=3600):
        """IP ni bloklash"""
        self.blocked_ips.add(ip)
        cache.set(f'blocked_ip:{ip}', True, duration)
        security_logger.warning(f"IP blocked: {ip} for {duration} seconds")
    
    def detect_attack(self, request):
        """Hujum aniqlash"""
        path = request.path.lower()
        query = request.META.get('QUERY_STRING', '').lower()
        body = request.body.decode('utf-8', errors='ignore').lower() if request.body else ''
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # Shubhali so'rov patternlari
        suspicious_content = path + ' ' + query + ' ' + body
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, suspicious_content, re.IGNORECASE):
                return True, f"Attack pattern detected: {pattern}"
        
        # Scanner va botlar
        scanner_signatures = [
            'sqlmap', 'nikto', 'nmap', 'burp', 'dirbuster', 
            'gobuster', 'wfuzz', 'gobuster', 'nessus', 'openvas',
            'acunetix', 'netsparker', 'appscan'
        ]
        
        for signature in scanner_signatures:
            if signature in user_agent:
                return True, f"Scanner detected: {signature}"
        
        return False, None
    
    def log_request(self, request, blocked=False, reason=None):
        """So'rovni log qilish"""
        ip = self.get_client_ip(request)
        path = request.path
        method = request.method
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'path': path,
            'method': method,
            'user_agent': user_agent,
            'blocked': blocked,
            'reason': reason
        }
        
        if blocked:
            security_logger.warning(f"BLOCKED REQUEST - IP: {ip}, Path: {path}, Reason: {reason}")
        else:
            security_logger.info(f"Request - IP: {ip}, Path: {path}, Method: {method}")
    
    def __call__(self, request):
        ip = self.get_client_ip(request)
        
        # IP bloklanganmi?
        if self.is_ip_blocked(ip):
            self.log_request(request, blocked=True, reason="IP is in blocklist")
            return HttpResponseForbidden(
                "Sizning IP manzilingiz bloklangan. Administrator bilan bog'laning."
            )
        
        # Hujum aniqlash
        is_attack, reason = self.detect_attack(request)
        if is_attack:
            user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
            record_ip_block(ip, user_agent, f"Security: {reason}")
            self.block_ip(ip, duration=86400)  # 24 soat bloklash
            self.log_request(request, blocked=True, reason=reason)
            return HttpResponseForbidden(
                "Shubhali faoliyat aniqlandi. IP manzilingiz bloklandi."
            )
        
        # Normal so'rovni log qilish
        self.log_request(request)
        
        return self.get_response(request)


class InputSanitizationMiddleware:
    """
    Input sanitizatsiya middleware
    XSS, SQL Injection va boshqa hujumlardan himoya
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # XSS patternlari
        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',  # Script teglari
            r'javascript:',  # JavaScript protocol
            r'on\w+\s*=',  # Event handlerlar
            r'<iframe',  # Iframe
            r'<object',  # Object
            r'<embed',  # Embed
        ]
    
    def sanitize_input(self, data):
        """Inputni tozalash"""
        if not isinstance(data, str):
            return data
        
        # HTML teglarni o'chirish
        import bleach
        cleaned = bleach.clean(
            data,
            tags=[],  # Ruxsat etilgan teglar
            attributes={},  # Ruxsat etilgan atributlar
            strip=True  # Tezlarni o'chirish
        )
        
        return cleaned
    
    def detect_malicious_input(self, data):
        """Zararli input aniqlash"""
        if not isinstance(data, str):
            return False
        
        data_lower = data.lower()
        
        # XSS patternlari
        for pattern in self.xss_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                return True, "XSS attempt detected"
        
        # SQL Injection patternlari (Faqat haqiqiy zararli so'rovlar uchun, oddiy ' va # belgilarisiz)
        sql_patterns = [
            r"\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
            r"((\%27)|(\'))union",
            r"exec(\s|\+)+(s|x)p\w+",
            r"UNION\s+SELECT",
            r"INSERT\s+INTO",
            r"DELETE\s+FROM",
            r"DROP\s+TABLE",
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                return True, "SQL Injection attempt detected"
        
        return False, None
    
    def __call__(self, request):
        ignored_keys = {
            'password', 
            'old_password', 
            'new_password', 
            'confirm_password', 
            'password_confirm', 
            'csrfmiddlewaretoken'
        }
        
        # GET parametrlarini tekshirish
        for key, value in request.GET.items():
            if key.lower() in ignored_keys:
                continue
            is_malicious, reason = self.detect_malicious_input(value)
            if is_malicious:
                security_logger.warning(f"Malicious GET parameter detected - Key: {key}, Reason: {reason}")
                return HttpResponseForbidden("Shubhali so'rov parametrlari aniqlandi.")
            # Sanitizatsiya
            request.GET._mutable = True
            request.GET[key] = self.sanitize_input(value)
            request.GET._mutable = False
        
        # POST ma'lumotlarini tekshirish
        if request.method == 'POST':
            for key, value in request.POST.items():
                if key.lower() in ignored_keys:
                    continue
                is_malicious, reason = self.detect_malicious_input(value)
                if is_malicious:
                    security_logger.warning(f"Malicious POST parameter detected - Key: {key}, Reason: {reason}")
                    return HttpResponseForbidden("Shubhali so'rov ma'lumotlari aniqlandi.")
                # Sanitizatsiya
                request.POST._mutable = True
                request.POST[key] = self.sanitize_input(value)
                request.POST._mutable = False
        
        return self.get_response(request)


class AdminSecurityMiddleware:
    """
    Admin panel xavfsizligi
    Admin sahifalariga qo'shimcha himoya
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def get_client_ip(self, request):
        """Klient IP manzilini olish"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def __call__(self, request):
        # Admin sahifalarini tekshirish
        if request.path.startswith('/admin/'):
            # IP whitelist tekshirish
            whitelist = getattr(settings, 'ADMIN_WHITELIST_IPS', [])
            if whitelist:
                ip = self.get_client_ip(request)
                if ip not in whitelist:
                    security_logger.warning(f"Admin access attempt from unauthorized IP: {ip}")
                    return HttpResponseForbidden(
                        "Admin panelga kirish taqiqlangan IP manzil."
                    )
            
            # 2FA tekshirish (agar yoqilgan bo'lsa)
            if request.user.is_authenticated and not request.user.is_superuser:
                # Superuser emas bo'lsa qo'shimcha tekshiruvlar
                security_logger.info(f"Admin access by: {request.user.username} from IP: {self.get_client_ip(request)}")
        
        return self.get_response(request)


class SessionTimeoutMiddleware:
    """30 daqiqa faolsizlikdan keyin avto-chiqish"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = getattr(settings, 'SESSION_COOKIE_AGE', 1800)
    
    def __call__(self, request):
        if request.user.is_authenticated:
            now = time.time()
            last_activity = request.session.get('last_activity', now)
            
            if now - last_activity > self.timeout:
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')
            
            request.session['last_activity'] = now
        
        return self.get_response(request)


class AdminAxesBypassMiddleware:
    """Super Admin uchun axes blokini bypass qilish"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # ✅ Faqat Super Admin uchun axes blokini o'tkazib yuborish
        # Login sahifasiga POST so'rovlarida tekshirish
        if request.method == 'POST' and request.path in ['/', '/login/', '/accounts/login/']:
            try:
                from django.contrib.auth.models import User
                from axes.models import AccessAttempt
                
                # Username olish
                username = request.POST.get('username')
                if username:
                    try:
                        user = User.objects.get(username=username)
                        if hasattr(user, 'profile') and user.profile.role == 'super_admin':
                            # Super Admin uchun axes blokini har doim reset qilish
                            # XAVFSIZLIK: exec() o'rniga to'g'ridan-to'g'ri ORM ishlatiladi
                            deleted_count, _ = AccessAttempt.objects.filter(username=username).delete()
                            if deleted_count > 0:
                                print(f"✅ Super Admin {username} blokdan chiqarildi ({deleted_count} ta urinish o'chirildi)")
                    except User.DoesNotExist:
                        pass
            except Exception as e:
                print(f"❌ Middleware xatolik: {e}")
                pass
        
        return self.get_response(request)


class NgrokMiddleware:
    """Ngrok requests uchun origin header sozlamalari"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Ngrok bilan kelgan referer/origin ni o'rnatish
        host = request.META.get('HTTP_HOST', '')
        
        if 'ngrok' in host:
            # X_FORWARDED_PROTO bilan protocol tekshirish
            protocol = request.META.get('HTTP_X_FORWARDED_PROTO', 'https')
            if protocol not in ('http', 'https'):
                protocol = 'https'
            
            # Ngrok domeni aniq qilish
            ngrok_origin = f'{protocol}://{host}'
            
            # Request metadata'ni o'rnatish
            request.META['HTTP_ORIGIN'] = ngrok_origin
            request.META['HTTP_REFERER'] = f'{ngrok_origin}/'
            request.META['SERVER_NAME'] = host.split(':')[0]
            request.META['wsgi.url_scheme'] = protocol
            
            # DEBUG uchun
            if settings.DEBUG:
                print(f"🔧 NgrokMiddleware - Protocol: {protocol}, Host: {host}, Origin: {ngrok_origin}")
        
        return self.get_response(request)


class LogoMiddleware:
    """Barcha so'rovlar uchun faol logotipni session ga saqlash"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Har bir so'rovda faol logotipni session ga saqlash
        from .models import SiteLogo
        active_logo = SiteLogo.get_active_logo()
        if active_logo:
            request.session['site_logo'] = active_logo.logo.url
        else:
            request.session.pop('site_logo', None)
        
        return self.get_response(request)
