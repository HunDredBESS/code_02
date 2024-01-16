import numpy as np
import pandas as pd
import os

Read_data_csv = pd.read_csv("../Data_ID.csv")
column_array = Read_data_csv['Face_Img'].to_numpy()
print(column_array)

# Extract base names without extension
base_names = [os.path.splitext(column_array)[0] for column_array in column_array]

# Print the result
print(base_names)

for items in base_names: 
    os.mkdir(items)