from flask import Flask, jsonify
import psycopg

app = Flask(__name__)


DB_CONFIG = {
    "host": "it-lab-database",
    "port": 5432,
    "dbname": "itlab",
    "user": "itadmin",
    "password": "itlabpassword"
}


@app.route("/health")
def health():
    return jsonify({
        "service": "api-server",
        "status": "healthy"
    })


@app.route("/")
def home():
    return jsonify({
        "service": "IT Infrastructure Lab API",
        "status": "online"
    })


@app.route("/database")
def database():
    try:
        connection = psycopg.connect(**DB_CONFIG)

        cursor = connection.cursor()
        cursor.execute("SELECT version();")

        version = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({
            "database": "PostgreSQL",
            "status": "connected",
            "version": version
        })

    except Exception as error:
        return jsonify({
            "database": "PostgreSQL",
            "status": "error",
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)