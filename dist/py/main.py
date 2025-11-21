"""
Рекурсивне розв'язання задачі «Ханойські башти».

Програма логує кожен крок і поточний стан стрижнів у вигляді словника.
"""

from typing import Dict, List


RodsState = Dict[str, List[int]]


def print_state(message: str, state: RodsState, disk: int | None = None, from_rod: str | None = None,
                to_rod: str | None = None) -> None:
    """
    Друкуємо поточний стан стрижнів.

    :param message: текстове повідомлення (наприклад, "Початковий стан")
    :param state: словник з ключами 'A', 'B', 'C' та списками дисків
    :param disk: номер диска, який рухаємо (необов’язково)
    :param from_rod: з якого стрижня (необов’язково)
    :param to_rod: на який стрижень (необов’язково)
    """
    if disk is not None and from_rod is not None and to_rod is not None:
        print(f"Перемістити диск з {from_rod} на {to_rod}: {disk}")
    print(f"{message}: {state}")


def move_disk(state: RodsState, from_rod: str, to_rod: str) -> int:
    """
    Переміщує один диск зі стрижня from_rod на стрижень to_rod.

    Повертає номер диска, який був переміщений.
    """
    disk = state[from_rod].pop()
    state[to_rod].append(disk)
    return disk


def hanoi(n: int, state: RodsState, source: str, auxiliary: str, target: str) -> None:
    """
    Рекурсивно розв'язує задачу Ханойських башт.

    :param n: кількість дисків, які потрібно перемістити з source на target
    :param state: поточний стан стрижнів
    :param source: початковий стрижень ('A')
    :param auxiliary: допоміжний стрижень ('B')
    :param target: кінцевий стрижень ('C')
    """
    if n == 0:
        return

    # 1. Перемістити n-1 дисків на допоміжний стрижень
    hanoi(n - 1, state, source, target, auxiliary)

    # 2. Перемістити найбільший диск
    disk = move_disk(state, source, target)
    print_state("Проміжний стан", state, disk, source, target)

    # 3. Перемістити n-1 дисків з допоміжного на цільовий
    hanoi(n - 1, state, auxiliary, source, target)


def main() -> None:
    """Точка входу в програму."""
    raw = input("Введіть кількість дисків n: ")
    try:
        n = int(raw)
        if n <= 0:
            print("Кількість дисків має бути додатнім числом.")
            return
    except ValueError:
        print("Потрібно ввести ціле число.")
        return

    # Ініціалізуємо стан стрижнів
    state: RodsState = {
        "A": list(range(n, 0, -1)),  # найбільший диск має найбільший номер
        "B": [],
        "C": [],
    }

    print_state("Початковий стан", state)

    hanoi(n, state, "A", "B", "C")

    print_state("Кінцевий стан", state)


if __name__ == "__main__":
    main()
