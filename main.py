import pandas as pd
from data_collector import collect_excel_data, collect_network_traffic
from data_preprocessor import preprocess_data
from model_trainer import train_model, save_model
from intrusion_detector import detect_intrusion
from notifier import send_notification
from report_generator import generate_report
import os

Base_Dir = os.path.dirname(os.path.abspath(__file__))
def main():
    # Specify the paths to your Excel files
    """
    Main entry point for the AI IDS application.

    This function collects data from the IoT Network Intrusion Dataset Excel file, preprocesses the data, trains a machine learning model, saves the trained model, and detects potential intrusions in new data.

    Data collection involves reading the Excel file and collecting network traffic data.
    Data preprocessing involves converting categorical features to numeric values, dropping unnecessary columns, scaling the features, and splitting the data into training and testing sets.
    Model training involves training a machine learning model on the preprocessed data.
    Model saving involves saving the trained model to a file.
    Intrusion detection involves loading the saved model, preprocessing new data, and using the model to detect potential intrusions in the new data.

    If an error occurs during data collection, preprocessing, model training, or intrusion detection, this function will print an error message and exit.

    :return: None
    """
    excel_file_path = os.path.join(Base_Dir, 'IoT Network Intrusion Dataset', 'IoT Network Intrusion Dataset.csv')
    print("Constructed File Path:", excel_file_path) 
    new_data_file_path = os.path.join(Base_Dir, 'IoT Network Intrusion Dataset', 'IoT Network Intrusion Dataset.csv')
   

    # Collect Data
    network_data = collect_network_traffic()
    print("")
    excel_data = collect_excel_data(excel_file_path)

    
    if excel_data is None:
        print("Failed to collect Excel data.")
        return  # Exit if data collection fails

    # Preprocess Data
    try:
        X, y = preprocess_data(excel_data)
        print("Features (X):")
        print(X.head())  # Print features
        print("Target Columns (y):")
        print(y.head())  # Print target columns
    except ValueError as ve:
        print(f"Error during preprocessing: {ve}")
        return  # Exit if preprocessing fails

    # Train Model
    try:
        model = train_model(X, y)  # Assuming train_model accepts X and y
        save_model(model, 'ids_model.pkl')  # Save the trained model
        print("Model trained and saved successfully.")
    except Exception as e:
        print(f"Error during model training: {e}")
        return  # Exit if training fails

    # Load new data for intrusion detection
    try:
        new_data = collect_excel_data(new_data_file_path)

        # Check if new data collection was successful
        if new_data is None or new_data.empty:
            print("No new data available for intrusion detection.")
            return  # Exit if new data is not available

        # Preprocess the new data
        new_data_processed, _ = preprocess_data(new_data)  # Unpack the tuple, discard the target

        # Ensure the DataFrame has the correct feature names
        new_data_processed.columns = X.columns  # Match feature names used during training

        # Detect intrusion
        is_intrusion = detect_intrusion(model, new_data_processed)
        print("Intrusion Detected:", is_intrusion)

    except Exception as e:
        print(f"Error during intrusion detection: {e}")

if __name__ == "__main__":
    main()