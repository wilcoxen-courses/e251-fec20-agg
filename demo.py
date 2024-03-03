""""
demo.py
Spring 2022 PJW

Demo file illustrating important additional function of pandas.
"""

import pandas as pd

#  Display all columns

pd.set_option('display.max_columns',None)

#
#  Read the data and list a few rows
#

sample = pd.read_csv('sample.zip',dtype=str)

print( '\nFirst rows:\n')
print( sample.head() )

#%%
#
#  Adjusting a name and the data type of one column
#

sample = sample.rename( columns={'TRANSACTION_PGI':'PGI'} )
sample['dollars'] = sample['TRANSACTION_AMT'].astype(float)

#%%
#
#  Convert a string to a Pandas datetime object and get the year
#

ymd = pd.to_datetime( sample['TRANSACTION_DT'], format="%m%d%Y")

sample['ymd'] = ymd
sample['year'] = ymd.dt.year

#
#  What have we got now?
#

print( sample[['TRANSACTION_DT','ymd','year']] )

#%%
#
#  Pickling the dataframe
#

sample.info()
sample.to_pickle('sample_pkl.zip')

#%%
#
#  Reload it under another name as a demonstration
#

sample2 = pd.read_pickle('sample_pkl.zip')
sample2.info()

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
#  Do some filtering and aggregation to set up next example
#

trim = sample.query("PGI=='P2020' or PGI=='G2020'")
trim = trim.query("year >= 2019")

grouped = trim.groupby(['PGI','year'])
tot_amt = grouped['dollars'].sum()

print( '\nContributions by PGI and year:\n' )
print( tot_amt )

#%%
#
#  Unstacking PGI
#

tot_wide = tot_amt.unstack('PGI')
tot_wide['total'] = tot_wide['P2020'] + tot_wide['G2020']

print('\nWide version by PGI, with total contributions:\n')
print( tot_wide )

#%%
#
#  Unstacking year
#

tot_wide = tot_amt.unstack('year')
tot_wide['total'] = tot_wide[2019] + tot_wide[2020]

print('\nWide version by year, with total contributions:\n')
print( tot_wide )

#%%
#
#  Views vs copies
#

keepvars = ['NAME', 'dollars']

subset_view = sample[ keepvars ]
subset_copy = sample[ keepvars ].copy()

#%%
#
#  Now suppose want to tidy up names on subsets.
#

#     Approach 1: Changing data in a view generates a warning

print('\nExpect one SettingWithCopy warning:\n')

fixname = subset_view['NAME'].str.title()

subset_view['NAME'] = fixname

#%%
#
#     Approach 2: No warning if we make a copy first
#

fixname = subset_copy['NAME'].str.title()

subset_copy['NAME'] = fixname

#%%
#
#     Approach 3: Preferred approach using copy_on_write mode. This will
#                 be the default in pandas 3. A copy operation will occur
#                 automatically when needed.
#

pd.options.mode.copy_on_write = True

fixname = subset_view['NAME'].str.title()

subset_view['NAME'] = fixname
