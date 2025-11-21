"""
Візуалізація фракталу «сніжинка Коха» з використанням рекурсії.

Користувач вводить рівень рекурсії з клавіатури.
"""

import turtle
from typing import Union


def draw_koch_segment(length: float, depth: int) -> None:
    """
    Малюємо один сегмент кривої Коха.

    :param length: довжина відрізка
    :param depth: рівень рекурсії
    """
    if depth == 0:
        turtle.forward(length)
        return

    length /= 3.0
    draw_koch_segment(length, depth - 1)
    turtle.left(60)
    draw_koch_segment(length, depth - 1)
    turtle.right(120)
    draw_koch_segment(length, depth - 1)
    turtle.left(60)
    draw_koch_segment(length, depth - 1)


def draw_koch_snowflake(length: float, depth: int) -> None:
    """
    Малюємо повну сніжинку Коха (3 сторони трикутника).
    """
    for _ in range(3):
        draw_koch_segment(length, depth)
        turtle.right(120)


def get_recursion_level() -> int:
    """
    Зчитуємо рівень рекурсії від користувача.

    Повертаємо ціле число >= 0.
    """
    while True:
        raw: str = input("Введіть рівень рекурсії (0–6 рекомендовано): ")
        try:
            level: int = int(raw)
            if level < 0:
                print("Рівень не може бути від’ємним. Спробуйте ще раз.")
                continue
            return level
        except ValueError:
            print("Потрібно ввести ціле число. Спробуйте ще раз.")


def main() -> None:
    """Точка входу в програму."""
    level: int = get_recursion_level()

    screen = turtle.Screen()
    screen.title(f"Сніжинка Коха (рівень {level})")
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-200, 100)
    turtle.pendown()

    draw_koch_snowflake(400, level)

    turtle.hideturtle()
    print("✅ Фрактал намальовано. Закрийте вікно, щоб завершити програму.")
    turtle.done()


if __name__ == "__main__":
    main()
