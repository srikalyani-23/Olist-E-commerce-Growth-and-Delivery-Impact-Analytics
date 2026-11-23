import os 
import pandas as pd

folder_path = "data/raw"
files = os.listdir(folder_path)
print("Files in the folder:", len(files))
print ("\nDataset files:")

for file in files:
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        print(f"\nFile: {file}")
        print("Rows:", df.shape[0])
        print(f"Columns: {df.shape[1]}")