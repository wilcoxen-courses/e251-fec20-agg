#! /bin/python3

import pandas as pd

#  Display all columns

pd.set_option('display.max_columns',None)

#
#  Read the data
#

sample = pd.read_csv('sample.zip',dtype=str)

#%%
#
#  Rename a variable
#

sample = sample.rename( {'TRANSACTION_PGI':'PGI'}, axis='columns')

#
#  Convert a variable to numeric form
#

sample['dollars'] = sample['TRANSACTION_AMT'].astype(float)

#
#  Convert a string to a Pandas datetime object
#

ymd = pd.to_datetime( sample['TRANSACTION_DT'], format="%m%d%Y")
print( ymd )

#  Now pull the year out of the datetime and put it in the dataframe

sample['year'] = ymd.dt.year

#
#  What have we got now?
#

print( sample )

#%%
#
#  Pickling the dataframe
#

sample.to_pickle('sample_pkl.zip')

#  Reload it under another name as a demonstration

sample2 = pd.read_pickle('sample_pkl.zip')

#%%
#
#  Selecting rows with a boolean series
#

is_ca = sample['STATE'] == 'CA'
is_tx = sample['STATE'] == 'TX'

is_either = is_ca | is_tx

subset_rows = sample[ is_either ]
print( subset_rows )

#%%
#
#  Using .unstack()
#

#  First, do some filtering and aggregation

trim = sample.query("PGI=='P2020' or PGI=='G2020'")
trim = trim.query("year >= 2019")

grouped = trim.groupby(['PGI','year'])
tot_amt = grouped['dollars'].sum()

print( tot_amt )

#  Unstacking PGI

tot_wide = tot_amt.unstack('PGI')
tot_wide['total'] = tot_wide['P2020'] + tot_wide['G2020']

print( tot_wide )

#  Unstacking year

tot_wide = tot_amt.unstack('year')
tot_wide['total'] = tot_wide[2019] + tot_wide[2020]

print( tot_wide )

#%%
#
#  Views vs copies
#

keepvars = ['NAME', 'dollars']

subset_view = sample[ keepvars ]
subset_copy = sample[ keepvars ].copy()

#  Now suppose want to tidy up names on subsets.

#     Approach 1: changing data in a view generates a warning

fixname = subset_view['NAME'].str.title()

subset_view['NAME'] = fixname

#     Approach 2: preferred approach is to make a copy first

fixname = subset_copy['NAME'].str.title()

subset_copy['NAME'] = fixname

