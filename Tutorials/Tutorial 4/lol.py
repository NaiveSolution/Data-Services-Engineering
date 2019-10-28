import pandas as pd

df = pd.read_csv('Books.csv')

df = df.set_index('Identifier')

def lol(id):
    if id in df.index:
	print(f'{id} is in df')
    else:
        print(f'{id} not in df')

lol('206')
lol('216')
lol('50')
