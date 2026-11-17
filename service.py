"""Правила проверки сложности паролей и генерация."""
import secrets
import string

from models import PasswordResult


class PasswordService:
    def __init__(self, repository):
        self.repository = repository
        self.symbols = "!@#$%^&*()-_=+?"
        self.common_parts = ["password", "qwerty", "123456", "abcdef", "admin", "letmein", "пароль"]

    def _analyze(self, password):
        if not password or password.isspace():
            raise ValueError("Введите непустой пароль, состоящий не только из пробелов.")

        lower = any(char in string.ascii_lowercase for char in password)
        upper = any(char in string.ascii_uppercase for char in password)
        digit = any(char in string.digits for char in password)
        symbol = any(char in string.punctuation for char in password)
        groups = sum([lower, upper, digit, symbol])
        common = any(part in password.lower() for part in self.common_parts)
        repeated = any(password[i] == password[i + 1] == password[i + 2]
                       for i in range(len(password) - 2))

        tips = []
        if len(password) < 6:
            tips.append("Увеличьте длину до 6 символов или больше.")
        if not upper:
            tips.append("Добавьте хотя бы одну заглавную латинскую букву.")
        if not digit:
            tips.append("Добавьте хотя бы одну цифру.")
        if not symbol:
            tips.append("Добавьте хотя бы один спецсимвол, например !, # или ?.")
        if common:
            tips.append("Уберите распространённые слова и последовательности.")
        if repeated:
            tips.append("Избегайте трёх одинаковых символов подряд.")

        if not tips:
            level = "надёжный"
        elif len(password) >= 8 and groups >= 2 and not common and not repeated:
            level = "средний"
        else:
            level = "слабый"
        return PasswordResult(len(password), groups, level, tips)

    def check(self, password):
        result = self._analyze(password)
        return self.repository.add(result)

    def generate(self, length):
        if length < 6 or length > 16:
            raise ValueError("Для генерации укажите длину от 6 до 16.")
        alphabet = string.ascii_letters + string.digits + self.symbols
        while True:
            # Сначала добавляем обязательные символы.
            characters = [secrets.choice(string.ascii_uppercase),
                          secrets.choice(string.digits),
                          secrets.choice(self.symbols)]
            for _ in range(length - 3):
                characters.append(secrets.choice(alphabet))
            # Перемешиваем, чтобы обязательные символы стояли в разных местах.
            secrets.SystemRandom().shuffle(characters)
            password = "".join(characters)
            result = self._analyze(password)
            if result.level == "надёжный":
                return password
