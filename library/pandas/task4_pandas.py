#Select a single column.

import pandas as pd

data = {'name': ['harshil','bhavy','meet','viral',],
        'age': [25,63,75,82],
        'location':['nikol','hirawadi','india colony','sbr']}
        
df = pd.DataFrame(data)
print(df['name'])
print(df['age'])
