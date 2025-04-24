import psutil  # For network traffic
import logging
import pandas as pd  # For handling Excel files

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import os

Base_Dir = os.path.dirname(os.path.abspath(__file__))
def collect_network_traffic():
    """Collect network traffic data."""
    try:
        traffic_data = psutil.net_if_stats()
        logging.info("AI IDS model has collected network traffic data successfully.")
        return traffic_data
    except Exception as e:
        logging.error(f"Error collecting network traffic: {e}")
        return None

def collect_excel_data(excel_file_path):
    """Read data from an Excel file."""
    try:
        data = pd.read_csv(excel_file_path)
        logging.info("AI IDS also collected Excel data successfully.")
        return data
    except FileNotFoundError:
        logging.error(f"Excel file not found: {excel_file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        return None

# You can add a test call here if you want to run this module independently
if __name__ == "__main__":
    excel_file_path = os.path.join(Base_Dir, 'IoT Network Intrusion Dataset', 'IoT Network Intrusion Dataset.csv')
    print("Constructed File Path:", excel_file_path) 
    excel_data = collect_excel_data(excel_file_path)
    if excel_data is not None:
        print(excel_data.head())  # Print the first few rows of the collected data