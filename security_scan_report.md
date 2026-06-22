# 🛡️ Mini HEMIS Tizimi Xavfsizlik Skaneri Hisoboti

**Skanerlangan sana:** 2026-06-15 12:30:03

**Skanerlangan fayllar soni:** 78
**Skanerlangan lokal URL:** Skanerlanmadi (Lokal server o'chiq edi)

## 📊 Umumiy statistika
| Daraja | Muammolar Soni |
| :--- | :--- |
| 🔴 CRITICAL | 0 |
| 🟠 HIGH | 3 |
| 🟡 MEDIUM | 99 |
| 🔵 LOW | 1 |
| 🟢 INFO | 1 |
| **Jami** | **104** |

## 🚨 Aniqlangan Xavfsizlik Muammolari

### 🟠 HIGH muammolar

#### 1. Insecure CORS: Barcha domenlarga ruxsat va Credentials=True
- **Kategoriya:** CORS Misconfiguration
- **Tavsif:** CORS_ALLOW_ALL_ORIGINS = True va CORS_ALLOW_CREDENTIALS = True bir vaqtda yoqilgan. Bu holatda har qanday zararli sayt foydalanuvchi ma'lumotlarini (cookies, sessiya) o'g'irlashi mumkin.
- **Tavsiya (Yechim):** CORS_ALLOW_ALL_ORIGINS ni False qiling va ruxsat etilgan domenlarni CORS_ALLOWED_ORIGINS ro'yxatiga qo'shing.
- **Dalil / Tafsilotlar:**
```text
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
```

---

#### 2. Eval/Exec Usage aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** eval() yoki exec() funksiyasi ishlatilgan. Bu kod inyeksiyasi (Code Injection) va masofaviy kod bajarilishiga (RCE) sabab bo'lishi mumkin.
- **Tavsiya (Yechim):** eval/exec ishlatishdan mutlaqo voz keching va xavfsizroq alternativalarni qo'llang.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/middleware.py, Qator: 362
Kod: exec(
```

---

#### 3. Eval/Exec Usage aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** eval() yoki exec() funksiyasi ishlatilgan. Bu kod inyeksiyasi (Code Injection) va masofaviy kod bajarilishiga (RCE) sabab bo'lishi mumkin.
- **Tavsiya (Yechim):** eval/exec ishlatishdan mutlaqo voz keching va xavfsizroq alternativalarni qo'llang.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/middleware.py, Qator: 497
Kod: exec(
```

---

### 🟡 MEDIUM muammolar

#### 1. .env da default/zaif SECRET_KEY
- **Kategoriya:** Configuration
- **Tavsif:** Environment (.env) faylida zaif default SECRET_KEY mavjud.
- **Tavsiya (Yechim):** Production uchun uni mutlaqo o'zgartiring.
- **Dalil / Tafsilotlar:**
```text
Line 5: SECRET_KEY=django-insecure-change-me
```

---

#### 2. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 208
Kod: get_object_or_404(LandingNews, pk=pk)
```

---

#### 3. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 224
Kod: get_object_or_404(LandingNews, pk=pk)
```

---

#### 4. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 872
Kod: get_object_or_404(Application, pk=pk)
```

---

#### 5. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1191
Kod: get_object_or_404(Student, pk=pk)
```

---

#### 6. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1311
Kod: get_object_or_404(Student, pk=pk)
```

---

#### 7. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1426
Kod: get_object_or_404(Student, pk=pk)
```

---

#### 8. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1628
Kod: get_object_or_404(Student, pk=pk)
```

---

#### 9. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2257
Kod: get_object_or_404(ExcelDownloadRequest, pk=pk)
```

---

#### 10. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2636
Kod: get_object_or_404(Faculty, pk=pk)
```

---

#### 11. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2670
Kod: get_object_or_404(Faculty, pk=pk)
```

---

#### 12. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2693
Kod: get_object_or_404(Specialty, pk=pk)
```

---

#### 13. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2730
Kod: get_object_or_404(Specialty, pk=pk)
```

---

#### 14. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2754
Kod: get_object_or_404(Specialty, pk=pk)
```

---

#### 15. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4073
Kod: get_object_or_404(Announcement, pk=pk)
```

---

#### 16. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4305
Kod: get_object_or_404(ChatMessage, pk=message_id)
```

---

#### 17. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4335
Kod: get_object_or_404(ChatMessage, pk=message_id)
```

---

#### 18. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4351
Kod: get_object_or_404(ChatMessage, pk=message_id)
```

---

#### 19. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4382
Kod: get_object_or_404(ChatMessage, pk=pk, sender=request.user)
```

---

#### 20. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4397
Kod: get_object_or_404(ChatMessage, pk=pk, sender=request.user)
```

---

#### 21. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4949
Kod: get_object_or_404(SiteLogo, pk=pk)
```

---

#### 22. IDOR (Insecure Direct Object Reference) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** get_object_or_404 orqali obyekt olishda foydalanuvchi huquqlari tekshirilmayapti. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir get_object_or_404 dan oldin foydalanuvchining ushbu obyektga kirish huquqini tekshiring.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4993
Kod: get_object_or_404(SiteLogo, pk=pk)
```

---

#### 23. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 109
Kod: @login_required
```

---

#### 24. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 174
Kod: @login_required
```

---

#### 25. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 200
Kod: @login_required
```

---

#### 26. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 216
Kod: @login_required
```

---

#### 27. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 303
Kod: @login_required
```

---

#### 28. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 659
Kod: @login_required
```

---

#### 29. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 665
Kod: @login_required
```

---

#### 30. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 684
Kod: @login_required
```

---

#### 31. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 756
Kod: @login_required
```

---

#### 32. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 864
Kod: @login_required
```

---

#### 33. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 906
Kod: @login_required
```

---

#### 34. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1077
Kod: @login_required
```

---

#### 35. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1090
Kod: @login_required
```

---

#### 36. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1189
Kod: @login_required
```

---

#### 37. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1301
Kod: @login_required
```

---

#### 38. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1416
Kod: @login_required
```

---

#### 39. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1452
Kod: @login_required
```

---

#### 40. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1524
Kod: @login_required
```

---

#### 41. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1587
Kod: @login_required
```

---

#### 42. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1617
Kod: @login_required
```

---

#### 43. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 1666
Kod: @login_required
```

---

#### 44. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2145
Kod: @login_required
```

---

#### 45. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2157
Kod: @login_required
```

---

#### 46. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2172
Kod: @login_required
```

---

#### 47. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2216
Kod: @login_required
```

---

#### 48. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2248
Kod: @login_required
```

---

#### 49. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2313
Kod: @login_required
```

---

#### 50. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2385
Kod: @login_required
```

---

#### 51. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2402
Kod: @login_required
```

---

#### 52. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2460
Kod: @login_required
```

---

#### 53. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2513
Kod: @login_required
```

---

#### 54. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2583
Kod: @login_required
```

---

#### 55. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2627
Kod: @login_required
```

---

#### 56. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2661
Kod: @login_required
```

---

#### 57. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2684
Kod: @login_required
```

---

#### 58. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2721
Kod: @login_required
```

---

#### 59. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2744
Kod: @login_required
```

---

#### 60. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2777
Kod: @login_required
```

---

#### 61. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2871
Kod: @login_required
```

---

#### 62. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2961
Kod: @login_required
```

---

#### 63. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 2997
Kod: @login_required
```

---

#### 64. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3022
Kod: @login_required
```

---

#### 65. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3052
Kod: @login_required
```

---

#### 66. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3077
Kod: @login_required
```

---

#### 67. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3127
Kod: @login_required
```

---

#### 68. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3155
Kod: @login_required
```

---

#### 69. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3187
Kod: @login_required
```

---

#### 70. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3209
Kod: @login_required
```

---

#### 71. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3239
Kod: @login_required
```

---

#### 72. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3672
Kod: @login_required
```

---

#### 73. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3718
Kod: @login_required
```

---

#### 74. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3838
Kod: @login_required
```

---

#### 75. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 3932
Kod: @login_required
```

---

#### 76. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4006
Kod: @login_required
```

---

#### 77. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4040
Kod: @login_required
```

---

#### 78. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4067
Kod: @login_required
```

---

#### 79. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4080
Kod: @login_required
```

---

#### 80. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4235
Kod: @login_required
```

---

#### 81. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4301
Kod: @login_required
```

---

#### 82. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4332
Kod: @login_required
```

---

#### 83. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4347
Kod: @login_required
```

---

#### 84. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4379
Kod: @login_required
```

---

#### 85. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4394
Kod: @login_required
```

---

#### 86. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4415
Kod: @login_required
```

---

#### 87. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4686
Kod: @login_required
```

---

#### 88. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4700
Kod: @login_required
```

---

#### 89. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4714
Kod: @login_required
```

---

#### 90. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4805
Kod: @login_required
```

---

#### 91. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4914
Kod: @login_required
```

---

#### 92. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4942
Kod: @login_required
```

---

#### 93. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4963
Kod: @login_required
```

---

#### 94. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 4986
Kod: @login_required
```

---

#### 95. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 5053
Kod: @login_required
```

---

#### 96. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 5075
Kod: @login_required
```

---

#### 97. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 5109
Kod: @login_required
```

---

#### 98. Missing Permission Check aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** @login_required dekoratori ishlatilgan, lekin qo'shimcha ruxsat tekshiruvi yo'q. Bu IDOR zaifligiga olib kelishi mumkin.
- **Tavsiya (Yechim):** Har bir view da foydalanuvchi rolini tekshiring (is_super_admin, is_admin va h.k.).
- **Dalil / Tafsilotlar:**
```text
Fayl: core/views.py, Qator: 5174
Kod: @login_required
```

---

#### 99. CSRF Bypass (csrf_exempt) aniqlandi
- **Kategoriya:** Code Vulnerability
- **Tavsif:** Ko'rinish (view) ustida @csrf_exempt dekoratori ishlatilgan. Bu ushbu endpointni CSRF hujumlariga qarshi himoyasiz qoldiradi.
- **Tavsiya (Yechim):** Iloji boricha @csrf_exempt ishlatmang, yoki uning o'rniga Token-based authentication kabi boshqa xavfsiz mexanizmlardan foydalaning.
- **Dalil / Tafsilotlar:**
```text
Fayl: core/api/v1/views.py, Qator: 227
Kod: @csrf_exempt
```

---

### 🔵 LOW muammolar

#### 1. .env da SMTP parol saqlanmoqda
- **Kategoriya:** Information Disclosure
- **Tavsif:** .env faylida ochiq holda SMTP Email paroli saqlanmoqda.
- **Tavsiya (Yechim):** Bu normal amaliyot bo'lsa-da, ushbu .env faylini hech qachon git tizimiga yuklamaslik kerak (.gitignore da borligini tekshiring).
- **Dalil / Tafsilotlar:**
```text
Line 11: EMAIL_HOST_PASSWORD = ********
```

---

### 🟢 INFO muammolar

#### 1. Lokal server faol emas
- **Kategoriya:** Dynamic Scan
- **Tavsif:** Dynamic (runtime) skanerlash amalga oshirilmadi, chunki lokal serverga ulanib bo'lmadi (port 8000).
- **Tavsiya (Yechim):** Skanerlash to'liq bo'lishi uchun Django serverni ishga tushiring: python manage.py runserver 0.0.0.0:8000

---


## 📝 Xavfsizlik bo'yicha yakuniy xulosa va tavsiyalar
1. **CORS sozlamalarini to'g'rilang:** `CORS_ALLOW_ALL_ORIGINS = True` va `CORS_ALLOW_CREDENTIALS = True` sozlamalari production muhitida o'ta xavfli. Ularni faqat ruxsat berilgan domenlar ro'yxati (`CORS_ALLOWED_ORIGINS`) bilan almashtiring.
2. **Xavfsiz headerlarni yoqing:** Dynamic scan ko'rsatganidek, ba'zi xavfsizlik headerlari (masalan, CSP) faol emas. Production settings ni to'liq ishga tushirish uchun `.env` faylida `DEBUG=False` qilish va barcha cookie-secure sozlamalarini yoqish lozim.
3. **SECRET_KEY kalitini yangilang:** .env va settings.py dagi maxfiy kalitlarni murakkab, tasodifiy generatsiya qilingan kalitga almashtiring.
4. **IPBlockMiddleware va Brute-Force Himoyasini saqlang:** Tizimda mavjud bo'lgan IPBlockMiddleware va Axes (Brute force himoyasi) juda yaxshi ishlamoqda. Ularning sozlamalarini o'zgartirmang.