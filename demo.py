#! /bin/python3
#  Spring 2020 (PJW)

import pandas as pd

pd.set_option('display.max_columns',None)

sample = pd.read_csv('sample-head.csv',dtype=str)

#  Translating a string column to float and adding it to the 
#  dataframe.

sample['dollars'] = sample['TRANSACTION_AMT'].astype(float)

print( sample )

# Pickling the dataframe

sample.to_pickle('sample.pkl')

# Reload it under another name

sample2 = pd.read_pickle('sample.pkl')

#%%

# Selecting variables (creating a slice of a DataFrame). Two slightly 
# different methods.

subset_view = sample[ ['NAME', 'dollars'] ]
print( subset_view )

subset_copy = sample[ ['NAME', 'dollars'] ].copy()
print( subset_copy )

# Selecting rows

is_il = sample['STATE'] == 'IL'
is_co = sample['STATE'] == 'CO'

is_either = is_il | is_co

subset_rows = sample[ is_either ]
print( subset_rows )

#%%

# Want to tidy up names on subsets. Obvious approach generates a warning
# and should be avoided.

fixname = subset_view['NAME'].str.title()
print( fixname )
subset_view['NAME'] = fixname

# Right way to revise a view is to use .loc[]

subset_view2 = sample[ ['NAME', 'dollars'] ]
subset_view2.loc[:,('NAME')] = fixname

# Alternately, no warning on an explicit copy:

fixname = subset_copy['NAME'].str.title()
print( fixname )
subset_copy['NAME'] = fixname

# Similar story with row slices

subset_rows['NAME'] = fixname

subset_rows.loc[:,('NAME')] = fixname
print( subset_rows )
