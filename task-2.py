import turtle
import argparse
import os


def parse_arguments():
    """
    Парсить аргументи командного рядка.

    Returns:
        argparse.Namespace: Об'єкт з аргументом level.
    """
    parser = argparse.ArgumentParser(description="Малювання фракталу 'Сніжинка Коха'.")
    parser.add_argument("level", type=int, nargs="?", default=3, help="Рівень рекурсії (за замовчуванням 3)")
    return parser.parse_args()


def koch_curve(t, order, size):
    """
    Рекурсивно малює одну сторону сніжинки Коха (криву Коха).

    Args:
        t (turtle.Turtle): Об'єкт turtle для малювання.
        order (int): Поточний рівень рекурсії.
        size (float): Довжина сегмента.
    """
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


def draw_koch_snowflake(order, size=300):
    """
    Налаштовує середовище turtle та малює повну сніжинку Коха.

    Args:
        order (int): Рівень рекурсії.
        size (float): Розмір сніжинки (довжина сторони початкового трикутника).
    """
    # Приховуємо попередження про застарілий Tk на macOS
    os.environ['TK_SILENCE_DEPRECATION'] = '1'

    try:
        window = turtle.Screen()
        window.bgcolor("white")
        window.title(f"Сніжинка Коха (Рівень {order})")
        
        # Вимикаємо анімацію для миттєвого малювання
        window.tracer(0)

        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(-size / 2, size / 3)
        t.pendown()

        for _ in range(3):
            koch_curve(t, order, size)
            t.right(120)

        window.update()
        window.mainloop()
    except turtle.Terminator:
        pass


def main():
    """
    Головна функція скрипту.
    """
    args = parse_arguments()
    
    # Обмежимо рівень рекурсії розумними межами, щоб не зависло
    if args.level < 0:
        print("Рівень рекурсії не може бути від'ємним.")
        return
    if args.level > 6:
        print(f"Попередження: Високий рівень рекурсії ({args.level}) може зайняти багато часу.")

    print(f"Малюємо сніжинку Коха з рівнем рекурсії {args.level}...")
    try:
        draw_koch_snowflake(args.level)
    except turtle.Terminator:
        print("Вікно малювання було закрито.")
    except Exception as e:
        print(f"Виникла помилка: {e}")


if __name__ == "__main__":
    main()
