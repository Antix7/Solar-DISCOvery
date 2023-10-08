import pandas as pd
import io

with pd.HDFStore('dataframes.h5') as store:
    dfs_from_h5 = [store[key] for key in store.keys()]

# Sort dfs based on their size (max size first)
dfs_from_h5_sorted = sorted(dfs_from_h5, key=len, reverse=True)

# Check results
for df in dfs_from_h5_sorted:
    print(df)
    print("-" * 50)
