#!/bin/bash

echo "sqlの初期設定を開始します。"
sudo apt update
sudo apt upgrade -y
sudo apt install apache2
sudo apt install php8.3 libapache2-mod-php8.3 php8.3-cli php8.3-common php8.3-mysql php8.3-xml php8.3-mbstring php8.3-curl php8.3-zip php8.3-gd php8.3-bcmath
sudo apt install mysql-server
php -v
echo "sqlの初期設定を完了しました。"

# MySQLの設定
DB_NAME="MAIke"
DB_USER="MAIkeUser"
DB_PASSWORD="3@WaM2cEZDpu4SR*KUAQt"

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
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"

echo "Database and table created successfully!"