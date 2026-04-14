import pandas as pd
import os
from datetime import datetime

# ---------------------------------------------
# STEP 1 — LOAD JSON FILE
# ---------------------------------------------

# Ensure the data folder exists
data_folder = "data"
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print(f"Created directory: {data_folder}")

# Find latest JSON file in data/ folder
json_files = [f for f in os.listdir(data_folder) if f.startswith("trends_") and f.endswith(".json")]

if not json_files:
    print("No JSON files found in data/ folder.")
    # Optionally, you could create a dummy file or exit here
    exit() # Exit if no files are found to prevent further errors

# Pick latest file
latest_file = sorted(json_files)[-1]
file_path = os.path.join(data_folder, latest_file)

# Load into DataFrame
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

# ---------------------------------------------
# STEP 2 — CLEAN THE DATA
# ---------------------------------------------

# 1. Remove duplicates
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# 2. Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Strip whitespace from title
df["title"] = df["title"].str.strip()

# ---------------------------------------------
# STEP 3 — SAVE AS CSV
# ---------------------------------------------

output_file = os.path.join(data_folder, "trends_clean.csv")
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# ---------------------------------------------
# SUMMARY — STORIES PER CATEGORY
# ---------------------------------------------

print("\nStories per category:")
print(df["category"].value_counts())
