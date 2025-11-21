"""
Рекурсивне копіювання та сортування файлів за розширеннями.

Використання з аргументами:
    python main.py source_dir dest_dir

- source_dir  – шлях до вихідної директорії
- dest_dir    – шлях до директорії призначення (необов'язково, за замовчуванням "dist")

Якщо source_dir не передано, буде використана поточна директорія, з якої запускається скрипт.
"""

import argparse
import shutil
from pathlib import Path
from typing import Optional


def parse_args() -> argparse.Namespace:
    """Парсимо аргументи командного рядка з підтримкою fallback."""
    parser = argparse.ArgumentParser(
        description=(
            "Рекурсивно копіює файли з вихідної директорії в директорію призначення, "
            "сортуючи їх за розширеннями."
        )
    )

    # source тепер НЕ обов'язковий (nargs="?"), за замовчуванням None
    parser.add_argument(
        "source",
        type=str,
        nargs="?",
        default=None,
        help="Шлях до вихідної директорії (якщо не вказано, використовується поточна директорія).",
    )

    parser.add_argument(
        "destination",
        type=str,
        nargs="?",
        default="dist",
        help='Шлях до директорії призначення (за замовчуванням: "dist").',
    )

    return parser.parse_args()


def ensure_directory(path: Path) -> None:
    """
    Гарантуємо, що директорія існує.

    Якщо директорії немає — створюємо її (з усіма батьківськими).
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"[ПОМИЛКА] Не вдалося створити директорію {path}: {error}")


def get_extension_folder(file_path: Path, destination_root: Path) -> Path:
    """
    Визначаємо піддиректорію за розширенням файлу.

    Якщо розширення немає — використовуємо папку 'no_extension'.
    """
    extension: Optional[str] = file_path.suffix.lower()
    if extension.startswith("."):
        extension = extension[1:]

    if not extension:
        extension = "no_extension"

    return destination_root / extension


def copy_file_to_destination(file_path: Path, destination_root: Path) -> None:
    """
    Копіюємо один файл у відповідну піддиректорію за його розширенням.
    """
    try:
        extension_folder: Path = get_extension_folder(file_path, destination_root)
        ensure_directory(extension_folder)

        destination_file: Path = extension_folder / file_path.name
        shutil.copy2(file_path, destination_file)
        print(f"[OK] Скопійовано: {file_path} -> {destination_file}")
    except (OSError, shutil.Error) as error:
        print(f"[ПОМИЛКА] Не вдалося скопіювати файл {file_path}: {error}")


def recursive_copy(source_dir: Path, destination_root: Path) -> None:
    """
    Рекурсивно обходить директорію source_dir і копіює всі файли
    у директорію призначення, розкладаючи їх за розширеннями.
    """
    try:
        for item in source_dir.iterdir():
            if item.is_dir():
                # Рекурсивно опрацьовуємо вкладену директорію
                recursive_copy(item, destination_root)
            elif item.is_file():
                copy_file_to_destination(item, destination_root)
    except PermissionError as error:
        print(f"[ПОМИЛКА ДОСТУПУ] Немає доступу до {source_dir}: {error}")
    except OSError as error:
        print(f"[ПОМИЛКА] Під час читання {source_dir} сталася помилка: {error}")


def main() -> None:
    """Точка входу в програму."""
    args = parse_args()

    # 🔁 Fallback: якщо source не передано — використовуємо поточну директорію
    if args.source is None:
        source_dir = Path.cwd()
        print(
            "[INFO] Шлях до вихідної директорії не передано. "
            f"Використовую поточну директорію: {source_dir}"
        )
    else:
        source_dir = Path(args.source).resolve()

    destination_root = Path(args.destination).resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"[ПОМИЛКА] Вихідна директорія не існує або не є директорією: {source_dir}")
        return

    ensure_directory(destination_root)
    print(f"Вихідна директорія: {source_dir}")
    print(f"Директорія призначення: {destination_root}")

    recursive_copy(source_dir, destination_root)
    print("✅ Готово! Всі файли скопійовано та розсортовано за розширеннями.")


if __name__ == "__main__":
    main()
