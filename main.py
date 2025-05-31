import yaml
import os
import logging
from logging.handlers import RotatingFileHandler
from db_backup import create_backup
from encryption import encrypt_file
from storage import move_to_storage, ensure_directory_exists
import sys
import io


# Принудительная установка UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def setup_logging():
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    # Настройка файлового логгера с UTF-8
    file_handler = RotatingFileHandler(
        'backup.log',
        encoding='utf-8',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    file_handler.setFormatter(log_formatter)

    # Настройка консольного логгера
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    # Основной логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def load_config():
    try:
        with open("config.yaml", "r", encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Ошибка загрузки конфига: {str(e)}")
        return None


def main():
    setup_logging()
    config = load_config()
    if not config:
        return

    # 1. Создаем бэкап
    backup_file = create_backup(config['database'])
    if not backup_file:
        return

    # 2. Шифруем бэкап
    encrypted_file = encrypt_file(backup_file, config['encryption']['public_key_path'])
    if not encrypted_file:
        os.remove(backup_file)
        return

    # 3. Сохраняем в хранилище
    if ensure_directory_exists(config['storage']['path']):
        if not move_to_storage(encrypted_file, config['storage']['path']):
            logging.error("Не удалось сохранить в хранилище")

    # 4. Очистка
    if os.path.exists(backup_file):
        os.remove(backup_file)


if __name__ == "__main__":
    main()