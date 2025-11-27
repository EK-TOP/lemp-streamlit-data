<?php
header('Content-Type: application/json');

$host = 'localhost';
$db   = 'chatdb';
$user = 'chatuser';
$pass = 'ChatPass123'; // sama kuin MySQL-käyttäjällä

$mysqli = new mysqli($host, $user, $pass, $db);

if ($mysqli->connect_errno) {
    http_response_code(500);
    echo json_encode(['error' => 'DB connection failed']);
    exit;
}

// Haetaan 100 viimeistä viestiä id:n mukaan DESC ja käännetään järjestys ASC (vanhin ensin)
$sql = "
    SELECT nickname, text, ts
    FROM (
        SELECT nickname, text, ts
        FROM chat_messages
        ORDER BY id DESC
        LIMIT 100
    ) AS latest
    ORDER BY ts ASC
";

$result = $mysqli->query($sql);

$messages = [];

if ($result) {
    while ($row = $result->fetch_assoc()) {
        $messages[] = [
            'nickname' => $row['nickname'],
            'text'     => $row['text'],
            'ts'       => $row['ts'],
        ];
    }
    $result->free();
}

$mysqli->close();

echo json_encode($messages);
