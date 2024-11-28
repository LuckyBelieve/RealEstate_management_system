import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Assuming `fetch_users` and `fetch_estates` are defined in `fetch_data`
from fetch_data import fetch_users, fetch_estates

# Fetch data
users_df = fetch_users()
estates_df = fetch_estates()

# printing to see the data structure
# print(users_df.head())
# print(estates_df.head())

# # Combine the datasets
data = pd.merge(estates_df, users_df, left_on="owner", right_on="id", how="inner")
# print(data.head())

# # Check data shape
# print("Data Shape Before Cleaning:")
# print(data.shape)
#
# # Display initial info
# print("\nInitial Dataset Info:")
# print(data.info())
#
# # Display initial statistics
# print("\nInitial Summary Statistics:")
# print(data.describe(include="all"))
#
# # Check for missing values
# print("\nMissing Values Before Cleaning:")
# print(data.isnull().sum())
#
# # Fill missing numeric values with the mean
# data.fillna(data.mean(numeric_only=True), inplace=True)
#
# # Fill missing categorical values with a placeholder (e.g., "Unknown")
# data.fillna("Unknown", inplace=True)
#
# print("\nMissing Values After Cleaning:")
# print(data.isnull().sum())
#
# # Check for duplicates
# duplicates = data[data.duplicated()]
# print(f"\nNumber of duplicate rows: {len(duplicates)}")
# if len(duplicates) > 0:
#     print(duplicates)
#
# # Remove duplicates
# data = data.drop_duplicates()
# print("\nDuplicate rows removed.")
# print(f"Dataset shape after removing duplicates: {data.shape}")
#
# # Remove irrelevant columns (example: passwords, sensitive data)
# if "password" in data.columns:
#     data = data.drop(columns=["password"])
#
# # Convert date columns (example: if `created_at` exists)
# if "created_at" in data.columns:
#     data["created_at"] = pd.to_datetime(data["created_at"])
#
# # Extract features from `created_at`
# if "created_at" in data.columns:
#     data["year"] = data["created_at"].dt.year
#     data["month"] = data["created_at"].dt.month
#     data["day"] = data["created_at"].dt.day
#     data["hour"] = data["created_at"].dt.hour
#     data["minute"] = data["created_at"].dt.minute
#     data["second"] = data["created_at"].dt.second
#
# # Log-transform numeric columns (example: `rent_amount`)
# if "rent_amount" in data.columns:
#     data["log_rent_amount"] = data["rent_amount"].apply(lambda x: round(np.log(x + 1), 2))
#
# # Convert `username` to lowercase (if applicable)
# if "username" in data.columns:
#     data["username"] = data["username"].apply(lambda x: str.lower(x))
#
# # Extract email domain (example: from `email`)
# if "email" in data.columns:
#     data["email_domain"] = data["email"].apply(lambda x: x.split("@")[-1])
#
# # Time of day feature (if `created_at` exists)
# def get_time_of_day(hour):
#     if pd.isna(hour):
#         return "Unknown"
#     if 6 <= hour < 12:
#         return "Morning"
#     elif 12 <= hour < 18:
#         return "Afternoon"
#     elif 18 <= hour < 24:
#         return "Evening"
#     else:
#         return "Night"
#
# if "hour" in data.columns:
#     data["time_of_day"] = data["hour"].apply(get_time_of_day)
#     data["time_of_day_encoded"] = data["time_of_day"].map(
#         {"Morning": 1, "Afternoon": 2, "Evening": 3, "Night": 4, "Unknown": 0}
#     )
#
# # Interaction feature (example: between `owner_id` and `property_type`)
# if "owner_id" in data.columns and "property_type" in data.columns:
#     owner_property_interaction_counts = (
#         data.groupby(["owner_id", "property_type"])
#         .size()
#         .reset_index(name="owner_property_interaction_count")
#     )
#     data = data.merge(
#         owner_property_interaction_counts, on=["owner_id", "property_type"], how="left"
#     )
#
# # Check final data shape and contents
# print("\nCleaned Dataset Shape:")
# print(data.shape)
# print("\nCleaned Dataset Info:")
# print(data.info())
# print("\nFirst Few Rows of Cleaned Data:")
# print(data.head())
#
# # Split Dataset
# train_data, temp_data = train_test_split(data, test_size=0.3, random_state=42)
# eval_data, val_data = train_test_split(temp_data, test_size=0.5, random_state=42)
#
# print(f"\nTraining set: {len(train_data)} rows")
# print(f"Evaluation set: {len(eval_data)} rows")
# print(f"Validation set: {len(val_data)} rows")
