import subprocess
import os
from datetime import datetime
import logging


def create_backup(db_config):
    """Создает резервную копию PostgreSQL"""
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    backup_file = f"{db_config['name']}_backup_{timestamp}.sql"

    try:
        pg_dump_path = r"D:\IT\PostgreSQL\17\bin\pg_dump.exe"

        if not os.path.exists(pg_dump_path):
            logging.error(f"pg_dump не найден по пути: {pg_dump_path}")
            return None

        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']

        command = r'cmd /c "D:\IT\PostgreSQL\17\bin\pg_dump.exe" -h {} -p {} -U {} -d {} -f {}'.format(
            db_config['host'],
            db_config['port'],
            db_config['user'],
            db_config['name'],
            backup_file
        )

        # Запускаем без перехвата вывода
        result = subprocess.run(
            command,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='ignore'
        )

        if result.returncode != 0:
            logging.error(f"Ошибка pg_dump: {result.stderr}")
            return None

        if not os.path.exists(backup_file):
            logging.error("Файл бэкапа не был создан")
            return None

        return backup_file

    except Exception as e:
        logging.error(f"Ошибка создания бэкапа: {str(e)}")
        return None