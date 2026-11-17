"""Слой данных: результат проверки пароля."""


class PasswordResult:
    def __init__(self, length, groups, level, tips):
        self.id = None
        self.length = length
        self.groups = groups
        self.level = level
        self.tips = tips
