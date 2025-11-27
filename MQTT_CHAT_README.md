# MQTT Chat for LEMP Stack

This directory contains all components for a working MQTT-based chat running inside a LEMP + Docker environment.

## Components

### 1. mqtt-chat/
Contains:
- Docker Compose configuration
- Mosquitto MQTT broker config
- subscriber.py (Python script that stores messages in MySQL)

### 2. chat-frontend/
Contains:
- index.html (chat UI)
- history.php (returns last 100 messages from MySQL)

### 3. nginx_mqtt_chat.conf
Example Nginx configuration for:
- exposing http://SERVER-IP/chat
- forwarding WebSocket traffic from /mqtt to Mosquitto port 9001

## Live Functionality
- Web UI served at: `http://<server>/chat`
- Messages published to topic: `chat/messages`
- subscriber.py stores all messages to MySQL table: `chat_messages`

## IMPORTANT
Replace passwords in subscriber.py before deployment. Do NOT store real credentials in GitHub.
