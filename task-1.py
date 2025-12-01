import argparse
from pathlib import Path
import shutil


def parse_arguments():
    """
    Парсить аргументи командного рядка.

    Returns:
        argparse.Namespace: Об'єкт з аргументами source та destination.
    """
    parser = argparse.ArgumentParser(description="Рекурсивне копіювання та сортування файлів за розширенням.")
    parser.add_argument("source", type=Path, help="Шлях до вихідної директорії")
    parser.add_argument("destination", type=Path, nargs="?", default=Path("dist"), help="Шлях до директорії призначення (за замовчуванням 'dist')")
    return parser.parse_args()


def copy_file(file_path: Path, destination: Path):
    """
    Копіює файл у відповідну піддиректорію в директорії призначення на основі його розширення.

    Args:
        file_path (Path): Шлях до файлу, який потрібно скопіювати.
        destination (Path): Шлях до кореневої директорії призначення.
    """
    try:
        # Отримуємо розширення файлу (без крапки)
        extension = file_path.suffix[1:] if file_path.suffix else "no_extension"
        
        # Створюємо шлях до піддиректорії
        target_dir = destination / extension
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Копіюємо файл
        shutil.copy2(file_path, target_dir / file_path.name)
        print(f"Скопійовано: {file_path} -> {target_dir / file_path.name}")
        
    except Exception as e:
        print(f"Помилка при копіюванні файлу {file_path}: {e}")


def process_directory(source: Path, destination: Path):
    """
    Рекурсивно обробляє директорію, копіюючи файли.

    Args:
        source (Path): Шлях до поточної директорії для обробки.
        destination (Path): Шлях до директорії призначення.
    """
    try:
        for item in source.iterdir():
            if item.is_dir():
                process_directory(item, destination)
            elif item.is_file():
                copy_file(item, destination)
    except PermissionError:
        print(f"Відмовлено в доступі до директорії: {source}")
    except Exception as e:
        print(f"Помилка при обробці директорії {source}: {e}")


def main():
    """
    Головна функція скрипту.
    """
    args = parse_arguments()
    
    source_path = args.source
    destination_path = args.destination

    if not source_path.exists():
        print(f"Вихідна директорія не існує: {source_path}")
        return

    if not source_path.is_dir():
        print(f"Вказаний шлях не є директорією: {source_path}")
        return

    print(f"Починаємо копіювання з {source_path} до {destination_path}...")
    process_directory(source_path, destination_path)
    print("Роботу завершено.")


if __name__ == "__main__":
    main()
