import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(excel_data):
    """Preprocess the data from the specified Excel file."""
    if excel_data is None:
        raise ValueError("No data to preprocess. Please check the data collection.")
    
    # Dropping unnecessary columns
    columns_to_drop = ['timestamp', 'CWE_Flag_Coun', 'ECE_Flag_Cnt', 'Fwd_Byts/b_Avg', 'Fwd_Pkts/b_Avg']
    df = excel_data.drop(columns=columns_to_drop, errors='ignore')

    # Specify the target variable and feature set
    target_columns = ['Label', 'Cat', 'Sub_Cat']
    
    # Selecting multiple target columns correctly
    y_train = df[target_columns]  # Multiple target columns
    X_train = df.drop(columns=target_columns, errors='ignore')  # Drop target columns for features

    # Convert categorical features to numeric
    for column in X_train.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X_train[column] = le.fit_transform(X_train[column])
    
    # Check for NaN and Infinite values
    if np.any(np.isnan(X_train)):
        print("Warning: NaN values detected. Replacing NaN with 0.")
        X_train.fillna(0, inplace=True)  # Replace NaN with 0 or handle appropriately

    if np.any(np.isinf(X_train)):
        print("Warning: Infinite values detected. Replacing infinite values with large finite number.")
        X_train.replace([np.inf, -np.inf], 1e10, inplace=True)  # Replace inf with a large number

    # Scale the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)  # Standardize the features

    # Convert back to DataFrame for easier inspection
    X_train = pd.DataFrame(X_train, columns=df.drop(columns=target_columns, errors='ignore').columns)

    return X_train, y_train