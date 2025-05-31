from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os


def generate_keys():
    """Генерирует пару RSA ключей и сохраняет их в файлы"""
    try:
        # Создаем папку для ключей, если ее нет
        os.makedirs('keys', exist_ok=True)

        # Генерация ключей
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # Сохраняем приватный ключ
        with open("keys/private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Сохраняем публичный ключ
        with open("keys/public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        print("Ключи успешно сгенерированы в папке 'keys'")
    except Exception as e:
        print(f"Ошибка генерации ключей: {str(e)}")


if __name__ == "__main__":
    generate_keys()