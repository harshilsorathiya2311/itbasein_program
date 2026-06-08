#2.Create a DataFrame from a dictionary.

import pandas as pd


a = {
    'car': ['BMW', 'Audi', 'Mercedes'],
    'model': [2009, 2010, 2011]
}

df = pd.DataFrame(a)
print(df)