#!/bin/bash

# .envファイルを読み込む
source .env

# MySQLの設定
DB_NAME=${MAIKE_DB_NAME}
DB_USER=${MAIKE_DB_USER}
DB_PASSWORD=${MAIKE_DB_PASSWORD}

# MySQLサーバーを起動
sudo systemctl start mysql

# ユーザーの存在確認
USER_EXISTS=$(sudo mysql -u root -e "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '${DB_USER}' AND host = 'localhost');" -sN)

# ユーザーが存在しない場合にのみ作成
if [ "$USER_EXISTS" -eq 0 ]; then
    echo "User does not exist. Creating user ${DB_USER}..."
    sudo mysql -u root -e "
        CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
        GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
        FLUSH PRIVILEGES;
    "
else
    echo "User ${DB_USER} already exists."
fi

# データベース作成とテーブル作成
sudo mysql -u root -e "
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
USE ${DB_NAME};
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    secretWord VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS Chat_History (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    chat_number INT NOT NULL DEFAULT 1,
    send_message TEXT NOT NULL,
    response_message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS chat_number (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    chat_number INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"

echo "Database and table created successfully!"