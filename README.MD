# Database Backup with Encryption

Проект для автоматического резервного копирования SQL-баз данных с асимметричным шифрованием резервных копий.

## 📋 Требования

- Python 3.10+
- PostgreSQL (для работы с другими СУБД требуется модификация)
- Библиотеки: `cryptography`, `psycopg2-binary`, `pyyaml`

## 🛠 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/shrimp151/db_backup_project.git
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
   
2. Выполните подключение к серверу:
   ```bash
   psql -U username -d database_name -h host -p port
   ```
   -U — имя пользователя

   -d — база данных

   -h — хост (по умолчанию localhost)

   -p — порт (по умолчанию 5432)
    
## 🚀 Использование

1. Сгенерируйте ключи шифрования:
   ```bash
   python key_manager.py
2. Запустите основной файл:
   ```bash
   python main.py
   ```
   
   Будут созданы резервные копии в формате sql, которые зашифрованы с помощью RSA-ключа и сохранены в папку backups/


## ♻ Восстановление из резервной копии:

1. Расшифруйте файл 
   ( ❗❗❗ в файле decrypt.py нужно указать путь к зашифрованному файлу)
   ```bash
   python decrypt.py 
   ```
2. Востановите БД:
   ```bash
   psql -U postgres -d ваша_база -f restored_bakup.sql
   ```
   
## 🕒 Автоматизация

1. Для Windows-планировщика создайте .bat файл:
   ```bat
      @echo off
      cd /d "путь к проекту"
      call .venv\Scripts\activate
      python main.py
   ```

## 📁 Структура проекта

   ```bash
      .
      ├── keys/                   # Ключи шифрования
      ├── backups/                # Зашифрованные резервные копии
      ├── config.yaml             # Конфигурация
      ├── main.py                 # Основной скрипт
      ├── db_backup.py            # Логика резервного копирования
      ├── encryption.py           # Шифрование/дешифровка
      ├── storage.py              # Управление хранилищем
      └── key_manager.py          # Генерация ключей
   ```

## 🔣 Работа с psql в терминале

Вот некоторые команды для работы с psql

   1. Подключение к серверу
   ```bash
      psql -U username -d database_name -h host -p port
   ```
   -U — имя пользователя

   -d — база данных

   -h — хост (по умолчанию localhost)

   -p — порт (по умолчанию 5432)

   2. Управление подключением
   
   ```bash
      \q                      Выйти из psql
      \c dbname [username]    Переключиться на другую БД
      \conninfo               Показать текущее подключение
   ```

   3. Работа с базами данных

   ```bash
      CREATE DATABASE dbname       Создать БД
      DROP DATABASE dbname	        Удалить БД
      \l	                        Список всех БД
      \l+                          Подробный список БД
   ```
   4. Работа с таблицами

   ```bash
      \dt	                          Список таблиц в текущей БД
      \dt+                           Подробный список таблиц
      \d table_name	          Описание таблицы
      \d+ table_name	          Подробное описание таблицы
      CREATE TABLE table_name (...); Создать таблицу
      DROP TABLE table_name;	  Удалить таблицу
      TRUNCATE TABLE table_name;	  Очистить таблицу (без удаления)
  ```

   5. Выполнение SQL-запросов

   ```bash
      SELECT * FROM table_name;                     Выполнить запрос
      INSERT INTO table_name VALUES (...);          Вставить данные
      UPDATE table_name SET column=value WHERE ...; Обновить данные
      DELETE FROM table_name WHERE ...;             Удалить данные
   ```

   6. Импорт/экспорт данных
   ```bash
      # Экспорт БД в SQL-файл (из командной строки)
      pg_dump -U username -d dbname -f backup.sql
      
      # Импорт из SQL-файла
      psql -U username -d dbname -f backup.sql
      
      # Экспорт таблицы в CSV
      \copy table_name TO '/path/file.csv' WITH CSV HEADER;
      
      # Импорт CSV в таблицу
      \copy table_name FROM '/path/file.csv' WITH CSV HEADER;
   ```

   7. Управление пользователями

   ```bash
      CREATE USER username WITH PASSWORD 'pass';    Создать пользователя
      DROP USER username;	                         Удалить пользователя
      \du	                                         Список пользователей
      ALTER USER username WITH PASSWORD 'newpass';	 Изменить пароль
   ```

   8. Мета-команды psql (начинаются с \)

   ```bash
      \?	        Справка по командам psql
      \h	        Справка по SQL-командам
      \timing      Включить/выключить замер времени
      \x	        Переключить вертикальный вывод
      \e	        Открыть редактор для запроса
      \i file.sql	Выполнить SQL-скрипт из файла
      \o file.txt	Перенаправить вывод в файл
   ```

## ⁉ Возможные проблемы

1. Смена кодировки в терменале
```bash
   #временное изменение
   chcp 1251
```