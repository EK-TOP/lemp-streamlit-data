from flask import Flask, jsonify, request
import mysql.connector
import os
import random

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppassword123"),
        database=os.getenv("DB_NAME", "appdb"),
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/users")
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/init-db")
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """
        )

        # Example users
        cursor.execute(
            """
            INSERT INTO users (name, email) VALUES
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com')
        """
        )

        # Bets table for gambling
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                outcome VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Database initialized (users + bets)"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/gamble", methods=["POST"])
def gamble():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ensure bets table exists
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                outcome VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # 1/5 chance to win
        roll = random.randint(1, 5)
        if roll == 1:
            outcome = "win"
            message = "casino stole your money anyway, kjeh kjeh"
        else:
            outcome = "lose"
            message = "you lost. the house always wins."

        cursor.execute("INSERT INTO bets (outcome) VALUES (%s)", (outcome,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"outcome": outcome, "message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
