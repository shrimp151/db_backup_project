from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os


def decrypt_file(encrypted_file, private_key_path, output_file):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    with open(encrypted_file, "rb") as f:
        encrypted_data = f.read()

    chunk_size = 256
    decrypted_data = b""

    for i in range(0, len(encrypted_data), chunk_size):
        chunk = encrypted_data[i:i + chunk_size]
        decrypted_chunk = private_key.decrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        decrypted_data += decrypted_chunk

    with open(output_file, "wb") as f:
        f.write(decrypted_data)


decrypt_file(
    "backups/company_backup_20250531_201559.sql.enc",
    "keys/private_key.pem",
    "restored_backup.sql"
)