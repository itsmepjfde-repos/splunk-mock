import random
from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI()

# A list of hardcoded sample Splunk-style logs
MOCK_LOGS = [
    '{{"timestamp": "{ts}", "level": "INFO", "service": "auth-service", "message": "User login successful", "user_id": {uid}}}',
    '{{"timestamp": "{ts}", "level": "ERROR", "service": "payment-service", "message": "Connection timeout to payment gateway", "code": 504}}',
    '{{"timestamp": "{ts}", "level": "WARN", "service": "user-profile", "message": "High memory utilization detected", "cpu_percent": 88.5}}',
    '{{"timestamp": "{ts}", "level": "INFO", "service": "gateway", "message": "API request processed", "path": "/api/v1/data", "duration_ms": 42}}'
]

@app.get("/api/splunk_mock")
def get_splunk_logs():
    """Return sample Splunk-like log entries for clients under test."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Return 3 random log entries with fresh timestamps
    selected_logs = [
        log.format(ts=now, uid=random.randint(1000, 9999)) 
        for log in random.sample(MOCK_LOGS, k=3)
    ]
    
    return {
        "status": "Success",
        "originator": "mock-splunk-server",
        "logs": selected_logs
    }
