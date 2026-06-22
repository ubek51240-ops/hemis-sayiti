# -*- coding: utf-8 -*-
"""
O'zbek tilida sonlarni so'zga aylantirish
Masalan: 1000000 -> "bir million so'm"
"""

# Birliklar
UNITS = ['', 'bir', 'ikki', 'uch', 'to\'rt', 'besh', 'olti', 'yetti', 'sakkiz', 'to\'qqiz']

# O'nliklar
TENS = ['', 'o\'n', 'yigirma', 'o\'ttiz', 'qirq', 'ellik', 'oltmish', 'yetmish', 'sakson', 'to\'qson']

# Yuzliklar
HUNDREDS = ['', 'bir yuz', 'ikki yuz', 'uch yuz', 'to\'rt yuz', 'besh yuz', 'olti yuz', 'yetti yuz', 'sakkiz yuz', 'to\'qqiz yuz']

# Katta birliklar
LARGE_UNITS = [
    ('', ''),
    ('ming', 'ming'),
    ('million', 'million'),
    ('milliard', 'milliard'),
    ('trillion', 'trillion'),
]


def convert_less_than_thousand(n):
    """1000 dan kichik sonni so'zga aylantirish"""
    if n == 0:
        return ''
    
    result = []
    
    # Yuzliklar
    hundred = n // 100
    if hundred > 0:
        result.append(HUNDREDS[hundred])
    
    # O'nliklar va birliklar
    remainder = n % 100
    if remainder > 0:
        ten = remainder // 10
        unit = remainder % 10
        
        if ten > 0:
            result.append(TENS[ten])
        if unit > 0:
            result.append(UNITS[unit])
    
    return ' '.join(result)


def number_to_words_uzbek(n):
    """
    Sonni o'zbek tilida so'zga aylantirish
    Masalan: 1500000 -> "bir million besh yuz ming"
    """
    if n == 0:
        return 'nol'
    
    if n < 0:
        return 'minus ' + number_to_words_uzbek(-n)
    
    result = []
    unit_index = 0
    
    while n > 0:
        chunk = n % 1000
        if chunk > 0:
            chunk_words = convert_less_than_thousand(chunk)
            if unit_index > 0:
                chunk_words += ' ' + LARGE_UNITS[unit_index][0]
            result.append(chunk_words)
        n //= 1000
        unit_index += 1
    
    # Teskari tartibda qaytarish (eng kattasidan boshlab)
    return ' '.join(reversed(result))


def format_money_uzbek(amount):
    """
    Pul summasini o'zbek tilida formatlash
    Masalan: 1500000 -> "1 500 000 so'm (bir million besh yuz ming so'm)"
    """
    try:
        amount = int(amount)
    except (ValueError, TypeError):
        return str(amount)
    
    # Sonni formatlash (3 xonali bo'linish)
    formatted_number = '{:,}'.format(amount).replace(',', ' ')
    
    # So'z ko'rinishi
    words = number_to_words_uzbek(amount)
    
    return f"{formatted_number} so'm ({words} so'm)"


def format_money_short(amount):
    """Qisqa format: 1 500 000 so'm"""
    try:
        amount = int(amount)
    except (ValueError, TypeError):
        return str(amount)
    
    return '{:,}'.format(amount).replace(',', ' ') + " so'm"
