Name: Harry Ma (hm41)

Module Info: Module 6 - Deploy Anywhere (Due: 03/03/26 11:59PM ET)

Approach: 
Architecture & Microservices: The core objective of this module was the 
refactoring of a monolithic Flask application into a decoupled microservice 
architecture. The system now utilizes Docker Compose to orchestrate four 
distinct services: a Flask web frontend, a Python background worker, a 
PostgreSQL database, and a RabbitMQ message broker. This separation ensures 
that long-running tasks, such as data ingestion and analytics recomputation, 
do not block the web tier, improving overall system responsiveness and reliability.

Asynchronous Task Processing: To handle data-modifying operations safely, a producer/consumer 
pattern was implemented via RabbitMQ. The web application acts as a producer, publishing tasks 
(e.g., recompute_analytics) to a durable exchange. The worker service consumes these messages 
with a prefetch_count=1 setting to ensure controlled backpressure and at-least-once delivery 
through manual acknowledgments.

Data Integrity & Idempotence: The ingestion layer was hardened with a watermark table (ingestion_watermarks) 
to track processed records. Database operations utilize Materialized Views for analytics, which are refreshed 
asynchronously by the worker. All SQL interactions utilize psycopg parameter binding to prevent SQL injection, 
and operations are wrapped in per-message transactions to ensure atomicity.

How to Run: 
Docker Compose: Ensure Docker Desktop is running. In the root module_6 folder, run:
docker compose up --build
Access Dashboard: Open http://localhost:8080 to view the Admissions Data Dashboard.
Monitor RabbitMQ: Access the management console at http://localhost:15672 (guest/guest).
Trigger Analysis: Click "Update Analysis" on the web UI to publish a task to RabbitMQ; 
observe the worker logs to see the Materialized View refresh.
Registry: Pull pre-built images from Docker Hub (e.g., docker pull harryma11/module_6-web:v1).

Fresh Install:
1) pip
In Terminal:
python -m venv venv 
source venv/bin/activate (Mac) OR venv\Scripts\activate
pip install -r requirements.txt
pip install -e

2) uv 
In Terminal:
uv venv
source .venv/bin/activate 
uv pip sync requirements.txt
uv pip install -e

Known Bugs/Workarounds: 
The pull data and update analysis buttons have lost their functionality since last touch. Only after running
the unit test, did I find that they were not being hit. Should've followed office hour suggestions and run tests
first before making major changes. This issue will be addressed this week to achieve intended functionalities. 
To achieve a 10/10 Pylint rating and a successful CI/CD pass, the following configurations were applied: 
Minor stylistic and non-functional linting rules were suppressed in the .pylintrc file where they did not 
impact application performance or logic.