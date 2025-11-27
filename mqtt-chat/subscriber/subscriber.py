import json
import paho.mqtt.client as mqtt
import mysql.connector

DB_CONF = {
    "host": "localhost",
    "user": "chatuser",       # se käyttäjä jonka loit MySQL:ään
    "password": "REPLACE_ME",  # sama salasana jonka annoimme aiemmin
    "database": "chatdb",
}

TOPIC = "chat/messages"

def save_message(payload: dict):
    conn = mysql.connector.connect(**DB_CONF)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_messages (nickname, text, client_id, ts) VALUES (%s,%s,%s,%s)",
        (
            payload.get("nickname"),
            payload.get("text"),
            payload.get("clientId"),
            payload.get("timestamp"),
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        save_message(data)
        print("Saved:", data)
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe(TOPIC)
client.loop_forever()
