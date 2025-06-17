from flask import Flask, request, jsonify
import threading
import subprocess
import json
import os
from datetime import datetime
import queue
import time

app = Flask(__name__)

# Global queue for task communication
task_queue = queue.Queue()
driver_ready = threading.Event()

class RPAEngine:
    def __init__(self):
        self.scripts = {
            'lead': 'Tab1.py',
            'task': 'Tasks.py',
            'events': 'events.py',
            'opportunity': 'oppurntiy.py',
            'taskedit': 'edittasks.py',
            'eventsedit': 'editevents.py',
            'leadupdate': 'leadupdateone.py'
        }
        self.task_thread_started = False

    def run(self, rpa_name, input_data=None):
        if rpa_name not in self.scripts:
            return f"Invalid RPA name: {rpa_name}", False

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{rpa_name}_data_{timestamp}.json"
        filepath = os.path.join("rpa_logs")
        os.makedirs(filepath, exist_ok=True)

        file_full_path = os.path.join(filepath, filename)
        with open(file_full_path, 'w') as f:
            json.dump(input_data or {}, f, indent=4)

        if rpa_name == 'task':
            if not self.task_thread_started:
                # Start the continuous task processor
                threading.Thread(target=self._start_task_processor, daemon=True).start()
                self.task_thread_started = True
                return "Task RPA processor started", True
            else:
                # Add data to queue for existing processor
                task_queue.put(input_data)
                return f"Task data added to processing queue and saved to {filename}", True
        else:
            threading.Thread(target=self._execute, args=(rpa_name, input_data)).start()
            return f"{rpa_name} RPA started and data saved to {filename}", True

    def _start_task_processor(self):
        """Start the modified Tasks.py that waits for POST data"""
        try:
            # Start Tasks.py with a special flag to indicate it should wait for POST data
            subprocess.Popen(['python', 'Tasks.py', '--wait-for-post'], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
            print("Task processor started and waiting for POST requests")
        except Exception as e:
            print(f"Failed to start task processor: {e}")

    def _execute(self, name, data):
        try:
            result = subprocess.run(
                ['python', self.scripts[name], json.dumps(data)],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"{name} completed successfully.\nOutput:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"{name} failed with exit code {e.returncode}.\nError output:\n{e.stderr}")
        except Exception as e:
            print(f"{name} failed with exception: {e}")

rpa = RPAEngine()

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

    message, success = rpa.run(rpa_name, data)
    return jsonify({"message": message}), (200 if success else 400)

@app.route('/task-data', methods=['POST'])
def receive_task_data():
    """Endpoint specifically for task data"""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    try:
        data = request.get_json()
        task_queue.put(data)
        return jsonify({"message": "Task data received and queued"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("✅ RPA System Ready")
    app.run(host='0.0.0.0', port=5000, debug=True)