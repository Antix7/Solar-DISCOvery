import pandas as pd
import io
with pd.HDFStore('dataframes.h5') as store:
    dfs_from_h5 = [store[key] for key in store.keys()]

# Check if DataFrames were loaded
print(f"Number of DataFrames loaded: {len(dfs_from_h5)}")

# Check results
for df in dfs_from_h5:
    print(df)
    print("-" * 50)


