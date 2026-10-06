# IT Infrastructure & Systems Administration Lab

A containerized IT infrastructure lab designed to simulate a small organization's
servers, database, monitoring system, and incident management workflow.

The project demonstrates practical infrastructure and systems administration
skills including Docker, networking, service monitoring, REST APIs, databases,
automation, troubleshooting, and incident response.

## Architecture

```text
                    IT Infrastructure Lab
                            |
                     Docker Network
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
    Nginx               Flask API           PostgreSQL
    Web Server           App Server          Database
       :80                  :5000                :5432
       |                    |                    |
       +--------------------+--------------------+
                            |
                            v
                     Monitoring Service
                            |
                 HTTP + TCP Health Checks
                            |
                            v
                     Incident Database
                        SQLite
                            ^
                            |
                            |
                    Monitoring API
                         :5000
                            |
                            v
                    REST API :5002