import sqlite3
import time
import socket
from datetime import datetime

import requests


DB_PATH = "/data/incidents.db"


SERVICES = {
    "API Server": {
        "type": "http",
        "target": "http://it-lab-api:5000/health"
    },
    "Web Server": {
        "type": "http",
        "target": "http://it-lab-web/"
    },
    "PostgreSQL": {
        "type": "tcp",
        "host": "it-lab-database",
        "port": 5432
    }
}


def initialize_database():

    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            status TEXT NOT NULL,
            severity TEXT NOT NULL,
            detected_at TEXT NOT NULL,
            resolved_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def create_incident(service):

    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        INSERT INTO incidents (
            service,
            status,
            severity,
            detected_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        service,
        "OPEN",
        "CRITICAL",
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()

    print(
        f"INCIDENT CREATED | {service}",
        flush=True
    )


def resolve_incident(service):

    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        UPDATE incidents
        SET status = 'RESOLVED',
            resolved_at = ?
        WHERE service = ?
        AND status = 'OPEN'
    """, (
        datetime.now().isoformat(),
        service
    ))

    connection.commit()
    connection.close()

    print(
        f"INCIDENT RESOLVED | {service}",
        flush=True
    )


def check_service(service, config):

    try:

        start = time.time()

        if config["type"] == "http":

            response = requests.get(
                config["target"],
                timeout=5
            )

            response_time = round(
                (time.time() - start) * 1000,
                2
            )

            healthy = response.status_code == 200

            if healthy:

                print(
                    f"[{datetime.now()}] "
                    f"{service} HEALTHY | "
                    f"Status: {response.status_code} | "
                    f"Response: {response_time} ms",
                    flush=True
                )

            else:

                print(
                    f"[{datetime.now()}] "
                    f"{service} UNHEALTHY | "
                    f"Status: {response.status_code}",
                    flush=True
                )

            return healthy

        elif config["type"] == "tcp":

            connection = socket.create_connection(
                (
                    config["host"],
                    config["port"]
                ),
                timeout=5
            )

            connection.close()

            response_time = round(
                (time.time() - start) * 1000,
                2
            )

            print(
                f"[{datetime.now()}] "
                f"{service} HEALTHY | "
                f"TCP {config['port']} | "
                f"Response: {response_time} ms",
                flush=True
            )

            return True

    except Exception as error:

        print(
            f"[{datetime.now()}] "
            f"{service} DOWN | "
            f"Error: {error}",
            flush=True
        )

        return False


initialize_database()


previous_status = {}


while True:

    for service, config in SERVICES.items():

        healthy = check_service(
            service,
            config
        )

        if healthy:

            if previous_status.get(service) == "DOWN":

                resolve_incident(service)

            previous_status[service] = "UP"

        else:

            if previous_status.get(service) != "DOWN":

                create_incident(service)

            previous_status[service] = "DOWN"

    time.sleep(10)