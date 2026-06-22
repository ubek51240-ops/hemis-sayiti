#!/usr/bin/env python3
"""
Excel namuna faylini yaratish uchun skript
"""

import pandas as pd
import os

def create_sample_excel():
    """Talaba ma'lumotlari uchun namuna Excel faylini yaratish"""
    
    # Namuna ma'lumotlar
    data = {
        'Ism': ['Aliyev Ali', 'Karimova Karima', 'To\'chiev To\'chirbek', 'Nazarova Nazira'],
        'Familiya': ['Aliyev', 'Karimova', 'To\'chiev', 'Nazarova'],
        'Sharif': ['Ali o\'g\'li', 'Karim qizi', 'To\'chirbek o\'g\'li', 'Nazira qizi'],
        'Tug\'ilgan sana': ['2000-01-15', '2001-05-20', '2000-11-10', '2001-08-25'],
        'Telefon': ['998901234567', '998902345678', '998903456789', '998904567890'],
        'Email': ['ali@example.com', 'karima@example.com', 'tochirbek@example.com', 'nazira@example.com'],
        'Manzil': ['Toshkent shahar, Yunusobod tumani', 'Samarqand shahar', 'Buxoro shahar', 'Farg\'ona shahar'],
        'Jinsi': ['Erkak', 'Ayol', 'Erkak', 'Ayol'],
        'Pasport seriyasi': ['AA1234567', 'BB2345678', 'CC3456789', 'DD4567890'],
        'Fakultet': ['Informatika', 'Matematika', 'Fizika', 'Kimyo'],
        'Yo\'nalish': ['Komp\'yuter injiniring', 'Amaliy matematika', 'Nazariy fizika', 'Organik kimyo'],
        'Kurs': ['3', '2', '4', '1'],
        'Guruh': ['IT-301', 'MAT-201', 'FIZ-401', 'KIM-101'],
        'O\'qish turi': ['Kunduzgi', 'Sirtqi', 'Kechki', 'Kunduzgi'],
        'Kontrakt miqdori': ['15000000', '12000000', '18000000', '14000000'],
        'Ota-ona ismi': ['Aliyev Vali', 'Karimov O\'tkir', 'To\'chiev Bahodir', 'Nazarov Rustam'],
        'Ota-ona telefon': ['998911111111', '998922222222', '998933333333', '998944444444']
    }
    
    # DataFrame yaratish
    df = pd.DataFrame(data)
    
    # Fayl yo\'lini belgilash
    media_dir = '/home/riva/mini_hemis/media'
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    
    file_path = os.path.join(media_dir, 'sample_students.xlsx')
    
    # Excel faylini saqlash
    df.to_excel(file_path, index=False, engine='openpyxl')
    
    print(f"Namuna Excel fayli yaratildi: {file_path}")
    print(f"Jami {len(df)} ta talaba ma\'lumoti qo\'shildi")
    
    return file_path

if __name__ == "__main__":
    create_sample_excel()
