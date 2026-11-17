"""Точка входа: меню и работа с пользователем."""
from repository import Repository
from service import PasswordService


def show_result(result):
    print(f"Проверка №{result.id}: {result.level}, "
          f"длина: {result.length}, групп символов: {result.groups}.")
    for tip in result.tips:
        print("-", tip)


def main():
    service = PasswordService(Repository())
    print("Проверка сложности и генерация паролей.")
    print("Оценка учебная: по длине, группам символов и нескольким простым шаблонам.")

    while True:
        print("\n1. Проверить свой пароль\n2. Сгенерировать сложный пароль\n0. Выход")
        try:
            action = input("Выберите действие: ").strip()
            if action == "0":
                break
            elif action == "1":
                password = input("Введите пароль: ")
                show_result(service.check(password))
            elif action == "2":
                length = int(input("Длина пароля(6-16): "))
                password = service.generate(length)
                print("Созданный пароль:", password)
                show_result(service.check(password))
            else:
                print("Такого пункта нет.")
        except ValueError as error:
            print("Ошибка:", error)
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            break


if __name__ == "__main__":
    main()
