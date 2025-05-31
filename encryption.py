from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import os
import logging


def encrypt_file(file_path, public_key_path):
    """Шифрует файл с помощью публичного ключа"""
    try:
        if not os.path.exists(file_path):
            logging.error(f"Файл не найден: {file_path}")
            return None

        # Читаем файл в бинарном режиме
        with open(file_path, "rb") as f:
            data = f.read()

        if not data:
            logging.error("Файл бэкапа пустой")
            return None

        # Загружаем публичный ключ
        with open(public_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        # Разбиваем данные на блоки для шифрования
        chunk_size = 190  # Для RSA 2048 бит
        encrypted_chunks = []

        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            encrypted_chunk = public_key.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_chunks.append(encrypted_chunk)

        # Сохраняем зашифрованные данные
        encrypted_file = f"{file_path}.enc"
        with open(encrypted_file, "wb") as f:
            for chunk in encrypted_chunks:
                f.write(chunk)

        logging.info(f"Файл успешно зашифрован: {encrypted_file}")
        return encrypted_file

    except Exception as e:
        logging.error(f"Ошибка шифрования: {str(e)}")
        return None