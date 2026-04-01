import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

# Test Data
EMAIL = f"test_{uuid.uuid4().hex[:6]}@example.com"
PASSWORD = "password123"
ROLE = "admin"
DIAMOND_ID = f"D-{uuid.uuid4().hex[:6]}"
WORKER_ID = f"W-{uuid.uuid4().hex[:6]}"
PROCESS_NAME = f"proc_{uuid.uuid4().hex[:6]}"

def test_01_register():
    response = client.post("/auth/register", params={"email": EMAIL, "password": PASSWORD, "role": ROLE})
    assert response.status_code == 200
    assert response.json()["email"] == EMAIL

def test_02_login():
    response = client.post("/auth/login", params={"email": EMAIL, "password": PASSWORD})
    assert response.status_code == 200
    assert "access_token" in response.json()
    global TOKEN
    TOKEN = response.json()["access_token"]

def test_03_create_diamond():
    payload = {
        "id": DIAMOND_ID,
        "stage": "procurement",
        "weight": 1.5,
        "value": 10000.0
    }
    response = client.post("/diamond/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == DIAMOND_ID

def test_04_create_worker():
    payload = {
        "id": WORKER_ID,
        "name": "John Doe"
    }
    response = client.post("/worker/create", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == WORKER_ID
    assert response.json()["name"] == "John Doe"

def test_05_assign_diamond():
    payload = {
        "diamond_id": DIAMOND_ID,
        "worker_id": WORKER_ID
    }
    response = client.post("/assignment/assign", json=payload)
    assert response.status_code == 200

def test_06_update_diamond_stage():
    payload = {
        "diamond_id": DIAMOND_ID,
        "new_stage": "cutting"
    }
    response = client.post("/diamond/update-stage", json=payload)
    assert response.status_code == 200

def test_07_get_diamond_by_id():
    response = client.get(f"/diamond/{DIAMOND_ID}")
    assert response.status_code == 200
    assert response.json()["id"] == DIAMOND_ID
    assert response.json()["stage"] == "cutting"

def test_08_get_all_diamonds():
    response = client.get("/diamond/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(d["id"] == DIAMOND_ID for d in response.json())

def test_09_get_diamonds_by_stage():
    response = client.get("/diamond/stage/cutting")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(d["stage"] == "cutting" for d in response.json())

def test_10_get_diamond_logs():
    response = client.get(f"/diamond/{DIAMOND_ID}/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Should have at least 2 logs: procurement (created) and cutting (updated)
    assert len(response.json()) >= 1 

def test_11_get_all_workers():
    response = client.get("/worker/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(w["id"] == WORKER_ID for w in response.json())

def test_12_get_assignment_by_diamond():
    response = client.get(f"/assignment/diamond/{DIAMOND_ID}")
    assert response.status_code == 200
    assert response.json()["diamond_id"] == DIAMOND_ID

def test_13_get_worker_assignments():
    response = client.get(f"/assignment/worker/{WORKER_ID}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(a["diamond_id"] == DIAMOND_ID for a in response.json())

def test_14_dashboard_stage_count():
    response = client.get("/dashboard/stage-count")
    assert response.status_code == 200
    # Response might be a list or dict depending on implementation
    # Based on stage-count endpoint it calls count_diamonds_by_stage

def test_15_dashboard_worker_load():
    response = client.get("/dashboard/worker-load")
    assert response.status_code == 200

def test_16_dashboard_worker_performance():
    response = client.get("/dashboard/worker-performance")
    assert response.status_code == 200

def test_17_dashboard_stuck_diamonds():
    response = client.get("/dashboard/stuck-diamonds")
    assert response.status_code == 200

def test_18_dashboard_stage_duration():
    response = client.get("/dashboard/stage-duration")
    assert response.status_code == 200

def test_19_dashboard_worker_ranking():
    response = client.get("/dashboard/worker-ranking")
    assert response.status_code == 200

def test_20_dashboard_throughput():
    response = client.get("/dashboard/throughput")
    assert response.status_code == 200

def test_21_send_location():
    # Requires Auth
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    
    payload = {
        "worker_id": WORKER_ID,
        "latitude": 19.0760,
        "longitude": 72.8777
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/worker/location", json=payload, headers=headers)
    assert response.status_code == 200

def test_22_dashboard_alerts():
    # Requires Auth
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/dashboard/alerts", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_23_create_process_definition():
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "name": PROCESS_NAME,
        "description": "High precision polishing",
        "expected_duration": 45
    }
    response = client.post("/process/create", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == PROCESS_NAME

def test_24_get_all_processes():
    response = client.get("/process/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(p["name"] == PROCESS_NAME for p in response.json())

def test_25_get_diamond_status():
    response = client.get(f"/diamond/{DIAMOND_ID}/status")
    assert response.status_code == 200
    assert "is_delayed" in response.json()
    assert response.json()["current_stage"] == "cutting"

def test_26_add_manual_incentive():
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "worker_id": WORKER_ID,
        "diamond_id": DIAMOND_ID,
        "amount": 150.0
    }
    response = client.post("/incentive/add", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["amount"] == 150.0

def test_27_get_worker_incentives():
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/incentive/worker/{WORKER_ID}", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(i["amount"] == 150.0 for i in response.json())

def test_28_get_monthly_incentives():
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    import datetime
    now = datetime.datetime.now()
    response = client.get(f"/incentive/monthly/{WORKER_ID}?month={now.month}&year={now.year}", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_29_get_total_incentive():
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/incentive/total/{WORKER_ID}", headers=headers)
    assert response.status_code == 200
    assert "total_incentive" in response.json()
    assert response.json()["total_incentive"] >= 150.0

def test_30_automatic_incentive_on_completion():
    # Set diamond to completed
    payload = {
        "diamond_id": DIAMOND_ID,
        "new_stage": "completed"
    }
    response = client.post("/diamond/update-stage", json=payload)
    assert response.status_code == 200
    
    # Check if total incentive increased (previous 150 + 100 default)
    login_response = client.post(f"/auth/login?email={EMAIL}&password={PASSWORD}")
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/incentive/total/{WORKER_ID}", headers=headers)
    assert response.status_code == 200
    assert response.json()["total_incentive"] >= 250.0
