import random
import operator

class MathCaptcha:
    """Matematik captcha generator"""
    
    @staticmethod
    def generate_captcha():
        """Yangi captcha yaratish"""
        # 2 ta random son (1-10 oraliqda)
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        
        # Amallar: +, -, *
        operations = [
            ('+', operator.add, f"{num1} + {num2}"),
            ('-', operator.sub, f"{num1} - {num2}" if num1 >= num2 else f"{num2} - {num1}"),
            ('*', operator.mul, f"{num1} * {num2}")
        ]
        
        # Random amal tanlash
        op_symbol, op_func, expression = random.choice(operations)
        
        # Agar ayirma bo'lsa va num1 < num2 bo'lsa, sonlarni almashtirish
        if op_symbol == '-' and num1 < num2:
            num1, num2 = num2, num1
            
        # Javobni hisoblash
        answer = op_func(num1, num2)
        
        # Expression ni to'g'ri formatda qaytarish
        if op_symbol == '+':
            expression = f"{num1} + {num2}"
        elif op_symbol == '-':
            expression = f"{num1} - {num2}"
        else:  # *
            expression = f"{num1} × {num2}"
        
        return {
            'question': expression,
            'answer': str(answer),
            'num1': num1,
            'num2': num2,
            'operation': op_symbol
        }
    
    @staticmethod
    def verify_answer(user_answer, correct_answer):
        """Javobni tekshirish"""
        try:
            return str(user_answer).strip() == str(correct_answer).strip()
        except (ValueError, AttributeError):
            return False
