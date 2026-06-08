#3.Display the first 5 rows of a DataFrame

import pandas as pd

data = {'Name': ['harshil', 'meet', 'fenil', 'viral', 'bhavy'],
        'Age': [25, 30, 35, 40, 45],
        'City': ['Nikol', 'hirawadi', 'india colony', 'naroda', 'sbr']}

df = pd.DataFrame(data)

print(df.head(3)) 