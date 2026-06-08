import pandas as pd

#2.Create a DataFrame from a dictionary.

a = {
    'car': ['BMW', 'Audi', 'Mercedes'],
    'model': [2009, 2010, 2011]
}

df = pd.DataFrame(a)
print(df)