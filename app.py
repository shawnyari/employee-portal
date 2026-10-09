import os
from flask import Flask, jsonify, send_file
import psycopg2

app = Flask(__name__)


# Employee Portal homepage
@app.route("/")
def home():
    return send_file("index.html")


# PostgreSQL database connectivity check
@app.route("/api/health")
def health():
    try:
        connection = psycopg2.connect(
            host=os.environ["DB_HOST"],
            dbname=os.environ.get("DB_NAME", "employee_portal"),
            user=os.environ.get("DB_USER", "portal_user"),
            password=os.environ["DB_PASSWORD"],
            connect_timeout=5
        )

        cursor = connection.cursor()
        cursor.execute(
            "SELECT current_database(), current_user"
        )
        database, user = cursor.fetchone()

        cursor.close()
        connection.close()

        return jsonify(
            status="success",
            database=database,
            user=user,
            message="Employee Portal connected to PostgreSQL"
        ), 200

    except Exception:
        app.logger.exception("Database connectivity failed")
        return jsonify(
            status="error",
            message="Database connection failed"
        ), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
