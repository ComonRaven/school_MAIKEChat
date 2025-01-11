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
DB_USER="root"
DB_PASSWORD="3@WaM2cEZDpu4SR*KUAQt"

# テーブル作成のSQL文
SQL="
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
USE ${DB_NAME};
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"

# MySQLコマンドを実行
echo "Creating database and users table..."
mysql -u ${DB_USER} -p${DB_PASSWORD} -e "${SQL}"

echo "Database and table created successfully!"