import os
import shutil
import logging


def ensure_directory_exists(path):
    """Создает директорию, если она не существует"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Не удалось создать директорию {path}: {str(e)}")
        return False


def move_to_storage(source_file, target_dir):
    """Перемещает файл в хранилище"""
    try:
        if not os.path.exists(source_file):
            logging.error(f"Исходный файл не существует: {source_file}")
            return False

        target_path = os.path.join(target_dir, os.path.basename(source_file))
        shutil.move(source_file, target_path)
        logging.info(f"Файл перемещен в хранилище: {target_path}")
        return True
    except Exception as e:
        logging.error(f"Ошибка перемещения файла: {str(e)}")
        return False