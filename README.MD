# Database Backup with Encryption

Проект для автоматического резервного копирования SQL-баз данных с асимметричным шифрованием резервных копий.

## 📋 Требования

- Python 3.10+
- PostgreSQL (для работы с другими СУБД требуется модификация)
- Библиотеки: `cryptography`, `psycopg2-binary`, `pyyaml`

## 🛠 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-репозиторий/db_backup_project.git
   cd db_backup_project
2. Установите зависимости:
    ```bash
   pip install -r requirements.txt
   
## ⚙ Настройка

1. Отредактируйте файл config.yaml:
    ```yaml
   database:
      type: "postgresql"
      host: "localhost"
      port: "5432"
      user: "postgres"
      password: "ваш_пароль"
      name: "название_базы_данных"
    
    encryption:
      public_key_path: "keys/public_key.pem"
    
    storage:
      type: "local"  
      path: "backups/"
    
## 🚀 Использование