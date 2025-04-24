import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from data_collector import collect_excel_data
import os 
Base_Dir = os.path.dirname(os.path.abspath(__file__))

def detect_intrusion(model, new_data):
    """Detect intrusion using the trained model."""
    prediction = model.predict(new_data)
    return prediction

def preprocess_new_data(new_data):
    """Preprocess new data for intrusion detection."""
    # Ensure new_data is a DataFrame for processing
    if isinstance(new_data, (list, np.ndarray)):
        new_data_df = pd.DataFrame(new_data)
    else:
        new_data_df = new_data.copy()

    # Load label encoders used during training
    label_encoders = joblib.load('label_encoders.pkl')

    # Apply the same preprocessing steps as in training
    for column in new_data_df.select_dtypes(include=['object']).columns:
        if column in label_encoders:
            new_data_df[column] = label_encoders[column].transform(new_data_df[column])
        else:
            print(f"Warning: {column} not found in label encoders. Check your data.")

    # Check for NaN and infinite values
    new_data_df.fillna(0, inplace=True)
    new_data_df.replace([np.inf, -np.inf], 1e10, inplace=True)

    # Scale the new data using the same scaler
    scaler = joblib.load('scaler.pkl')
    new_data_scaled = scaler.transform(new_data_df)

    return new_data_scaled

if __name__ == "__main__":
    # Load the model
    model = joblib.load('ids_model.pkl')


    # Define the path to your new data file
    excel_file_path = os.path.join(Base_Dir, 'IoT Network Intrusion Dataset', 'IoT Network Intrusion Dataset.csv')  # Update to your actual new data file path
    new_data = collect_excel_data(excel_file_path)
    
    # Check if data collection was successful
    if new_data is None or new_data.empty:
        print("Failed to collect new data or no data available.")
    else:
        # Preprocess the new data
        new_data_processed = preprocess_new_data(new_data)

        # Detect intrusion
        is_intrusion = detect_intrusion(model, new_data_processed)
        print("Intrusion Detected:", is_intrusion)