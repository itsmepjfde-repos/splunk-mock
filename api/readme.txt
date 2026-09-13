Splunk Mock API
===============
https://ishatrainingsolutions-itsmefde-splunk-mock.vercel.app/api/splunk_mock

This project provides a small FastAPI service that returns sample Splunk-like
log entries for ecommerce development and integration testing. It does not
connect to Splunk and is not a full Splunk HTTP Event Collector implementation.

Project files
-------------

- splunk_mock.py: FastAPI application and mock log endpoint.
- ../requirements.txt: Runtime dependencies.
- ../pyproject.toml: Python project metadata and the Vercel entrypoint.
- ../vercel.json: Vercel configuration. It is intentionally empty because no
	custom rewrites are needed.

API endpoint
------------

GET /api/splunk_mock

GET /api/splunk_mock/{category}

The category can also be passed to the legacy route as a query parameter:

GET /api/splunk_mock?category=payment

The service returns HTTP 200 with up to three randomly selected log entries.
With the current payload set, each category has one error entry. Each entry is
returned as a JSON string inside the logs array. Supported categories
are auth, catalog, cart, order, payment, inventory, shipping, and notification.
Aliases include products, product, orders, payments, stock, delivery, and
notifications. Unknown categories use the generic-ecommerce-service fallback.

The no-argument legacy endpoint also uses the generic fallback.

Example response:

The example is abbreviated; an actual response contains three entries.

{
	"status": "Success",
	"originator": "mock-splunk-server",
	"requested_category": "payment",
	"service_category": "payment",
	"logs": [
		"{\"level\": \"ERROR\", \"service\": \"payment-service\", \"message\": \"Connection timeout to payment gateway\", \"status_code\": 504, \"timestamp\": \"2026-09-12 12:00:00 UTC\"}"
	]
}

Run locally on Windows
----------------------

From the repository root:

		.\menv\Scripts\python.exe -m uvicorn api.splunk_mock:app --host 127.0.0.1 --port 8000

In a second PowerShell window, call the endpoint:

		Invoke-RestMethod http://127.0.0.1:8000/api/splunk_mock | ConvertTo-Json -Depth 5
		Invoke-RestMethod http://127.0.0.1:8000/api/splunk_mock/payment | ConvertTo-Json -Depth 5

Stop the server with Ctrl+C.

Deploy to Vercel
----------------

1. Commit and push the project to GitHub.
2. Import the GitHub repository in Vercel.
3. Keep the project root set to the repository root.
4. Deploy. Vercel reads the FastAPI entrypoint from pyproject.toml:

			 api.splunk_mock:app

After deployment, call:

		https://YOUR-PROJECT.vercel.app/api/splunk_mock

The menv directory should remain local and must not be committed. It is
excluded by the repository .gitignore file.
