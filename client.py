import requests
import uuid

ENDPOINT_URL = "http://127.0.0.1:8000/xapi/statements/"

xapi_statement = {
    "actor": {
        "mbox": "mailto:test@example.com",
        "name": "Test User",
        "objectType": "Agent"
    },
    "verb": {
        "id": "http://adlnet.gov/expapi/verbs/completed",
        "display": {"en-US": "completed"}
    },
    "object": {
        "id": "http://example.com/activity",
        "definition": {
            "name": {"en-US": "Test Activity"},
            "description": {"en-US": "Description of the test activity."},
            "type": "http://adlnet.gov/expapi/activities/course"
        },
        "objectType": "Activity"
    },
    "id": str(uuid.uuid4())
}

response = requests.post(ENDPOINT_URL, json=xapi_statement)

if response.status_code == 200:
    print("xAPI statement sent successfully!")
    print(response.json())
else:
    print(f"Failed to send xAPI statement. Status: {response.status_code}")
    try:
        error_data = response.json()
        print(f"Error message: {error_data.get('detail', 'Unknown error')}")
    except:
        print(response.text)
