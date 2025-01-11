<?php
session_start();
$host = 'localhost';
$dbname = 'user_management';
$user = 'root';
$pass = 'your_mysql_password';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $email = $_POST['email'];
        $password = $_POST['password'];

        $stmt = $pdo->prepare("SELECT * FROM users WHERE email = :email");
        $stmt->bindParam(':email', $email);
        $stmt->execute();
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            header("Location: dashboard.php");
            exit();
        } else {
            echo "メールアドレスまたはパスワードが間違っています。";
        }
    }
} catch (PDOException $e) {
    echo "データベース接続エラー: " . $e->getMessage();
}
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ログインページ</title>
    <script src="./js/login.js" defer></script>
</head>
<body>
    <h1>ログインページです。</h1>
    <div class="logo">
        <img src="https://picsum.photos/200" />
    </div>

    <form action="home.php" method="POST">
        <label for="email">メールアドレス:</label><br>
        <input type="email" name="email" required><br>

        <label for="password">パスワード:</label><br>
        <input type="password" name="password" required><br><br>

        <button type="submit">ログイン</button>
    </form>
    <button onclick="move()">移動</button>
    <script>
        function move(){
            window.location.href = "./AI.html";
        }
    </script>
</body>
</html>