import pandas as pd
import numpy as np

print('--- Vitejte v Data Science Kurzu! ---')
df = pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C'])
print('\nUkazkova data (nahodna matice):')
print(df)
print('\nProstredi je pripraveno!')
