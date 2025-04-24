from flask import Flask, request, jsonify, render_template
from data_collector import collect_excel_data
from data_preprocessor import preprocess_data
from model_trainer import load_model
from intrusion_detector import detect_intrusion
import numpy as np
import os
from notifier import send_notification
Base_Dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# Load your model when the app starts
model = load_model('ids_model.pkl')

@app.route('/scan', methods=['POST'])
def scan():
    # Specify the paths to your Excel files
    excel_file_path = os.path.join(Base_Dir, 'IoT Network Intrusion Dataset', 'IoT Network Intrusion Dataset.csv')  # Update to your actual new data file path

    # Collect and preprocess data
    excel_data = collect_excel_data(excel_file_path)
    if excel_data is None:
        return jsonify({"error": "Failed to collect Excel data."}), 500

    try:
        # Log the collected Excel data
        print("Excel Data:", excel_data)

        # Preprocess the collected data
        new_data_processed, _ = preprocess_data(excel_data)
        
        # Check for issues in new_data_processed
        print("Processed Data:", new_data_processed.head())

        # Ensure the correct feature names are set
        new_data_processed.columns = model.feature_names_in_

        # Detect intrusion
        is_intrusion = detect_intrusion(model, new_data_processed)

        # Convert the result to a list if it's a NumPy array
        if isinstance(is_intrusion, np.ndarray):
            is_intrusion = is_intrusion.tolist()

        return jsonify({"intrusion_detected": is_intrusion})

    except Exception as e:
        # Log the error for debugging
        print("Error during scan:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/report', methods=['POST'])
def send_email():
    # Send an email notification
    try:
        send_notification("Potential intrusion detected in the network.")
    except Exception as e:
        # Log the error for debugging
        print("Error during email notification:", str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Notification sent successfully."})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)