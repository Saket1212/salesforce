from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/runrpa', methods=['POST'])
def trigger_from_post():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Malformed JSON"}), 400
    
    rpa_name = data.get('rpa_name')
    if not rpa_name:
        return jsonify({"error": "'rpa_name' is required in JSON body"}), 400
    
    # Debug: Print received data structure
    print(f"🔍 Received data keys: {list(data.keys())}")
    print(f"🔍 Full received data: {json.dumps(data, indent=2)}")
    
    # Save the data to a JSON file for record
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{rpa_name}_data_{timestamp}.json"
    filepath = os.path.join("rpa_logs")
    os.makedirs(filepath, exist_ok=True)
    
    file_full_path = os.path.join(filepath, filename)
    with open(file_full_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"📝 New data received for RPA: {rpa_name}")
    print(f"💾 Data saved to: {filename}")
    
    # Also check if followups_data exists
    followups_data = data.get('followups_data', [])
    if followups_data:
        print(f"✅ Found {len(followups_data)} followups_data entries")
    else:
        print("⚠️ No 'followups_data' key found in request")
        # Try to find other possible data keys
        possible_keys = ['data', 'tasks', 'leads', 'entries']
        for key in possible_keys:
            if key in data and isinstance(data[key], list):
                print(f"🔍 Found data in '{key}' key with {len(data[key])} entries")
                break
    
    return jsonify({"message": f"Data for '{rpa_name}' saved to {filename}"}), 200

@app.route('/test', methods=['POST'])
def test_endpoint():
    """Test endpoint with sample data"""
    sample_data = {
        "rpa_name": "lead",
        "followups_data": [
            {
                "task_id": "TEST123",
                "lead_email": "test@example.com",
                "subject": "Test Task Subject",
                "due_date": "19/06/2025",
                "status": "Not Started",
                "lead_url": "https://cxp--preprod.sandbox.my.site.com/CXP/s/lead/Lead/TEST123",
                "comments": "This is a test task created from Flask API"
            }
        ]
    }
    
    # Save test data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"test_data_{timestamp}.json"
    filepath = os.path.join("rpa_logs")
    os.makedirs(filepath, exist_ok=True)
    
    file_full_path = os.path.join(filepath, filename)
    with open(file_full_path, 'w') as f:
        json.dump(sample_data, f, indent=4)
    
    print(f"🧪 Test data created: {filename}")
    
    return jsonify({"message": f"Test data created: {filename}", "data": sample_data}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Flask API is healthy"}), 200

if __name__ == '__main__':
    print("🚀 Starting Flask API Server...")
    print("📡 Listening for POST requests on http://localhost:5000/runrpa")
    print("✅ JSON Processor Ready")
    app.run(host='0.0.0.0', port=5000, debug=True)
