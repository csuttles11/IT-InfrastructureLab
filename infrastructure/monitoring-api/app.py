from flask import Flask, jsonify
import sqlite3


app = Flask(__name__)


DB_PATH = "/data/incidents.db"


def get_database_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


@app.route("/health")
def health():

    return jsonify({
        "service": "monitoring-api",
        "status": "healthy"
    })


@app.route("/incidents")
def incidents():

    connection = get_database_connection()

    rows = connection.execute("""
        SELECT
            id,
            service,
            status,
            severity,
            detected_at,
            resolved_at
        FROM incidents
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    incidents = []

    for row in rows:

        incidents.append({
            "id": row["id"],
            "service": row["service"],
            "status": row["status"],
            "severity": row["severity"],
            "detected_at": row["detected_at"],
            "resolved_at": row["resolved_at"]
        })

    return jsonify(incidents)


@app.route("/incidents/open")
def open_incidents():

    connection = get_database_connection()

    rows = connection.execute("""
        SELECT
            id,
            service,
            status,
            severity,
            detected_at,
            resolved_at
        FROM incidents
        WHERE status = 'OPEN'
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    incidents = []

    for row in rows:

        incidents.append({
            "id": row["id"],
            "service": row["service"],
            "status": row["status"],
            "severity": row["severity"],
            "detected_at": row["detected_at"],
            "resolved_at": row["resolved_at"]
        })

    return jsonify(incidents)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )