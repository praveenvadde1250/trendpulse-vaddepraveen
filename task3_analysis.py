import pandas as pd
import numpy as np
import os

# ---------------------------------------------
# STEP 1 — LOAD AND EXPLORE
# ---------------------------------------------

file_path = "/content/trendpulse-vaddepraveen/data/trends_clean.csv"

# Load CSV
df = pd.read_csv(file_path)

# Print shape
print(f"Loaded data: {df.shape}")

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average values
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.0f}")
print(f"Average comments: {avg_comments:.0f}")

# ---------------------------------------------
# STEP 2 — NUMPY ANALYSIS
# ---------------------------------------------

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

# Mean, Median, Std
print(f"Mean score   : {np.mean(scores):.0f}")
print(f"Median score : {np.median(scores):.0f}")
print(f"Std deviation: {np.std(scores):.0f}")

# Max & Min
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Most commented story
max_comments_idx = np.argmax(comments)
top_story_title = df.iloc[max_comments_idx]["title"]
top_story_comments = comments[max_comments_idx]

print(f'\nMost commented story: "{top_story_title}" — {top_story_comments} comments')

# ---------------------------------------------
# STEP 3 — ADD NEW COLUMNS
# ---------------------------------------------

# Engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = score > average score
df["is_popular"] = df["score"] > avg_score

# ---------------------------------------------
# STEP 4 — SAVE RESULT
# ---------------------------------------------

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
