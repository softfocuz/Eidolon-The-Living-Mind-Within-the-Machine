import pandas as pd

df = pd.read_csv('dataset.csv')

df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True) # fix data type from str to datetime
df.drop(columns=['date'], inplace=True) # delete original date column
df['date'] = df['timestamp'].dt.date # create new date column and extract date from timestamp column

df['previous_app'] = df['previous_app'].fillna('NONE') # based on the missing value analysis[testing.ipynb], only this column contains missing values

df['session_duration_sec'] = df['session_duration_sec'].astype(int)
# ensure session_duration_sec is stored as integer

df['session_duration_min'] = df['session_duration_sec'] // 60 # add a new column with session duration converted from seconds to minutes

def part_of_day(hour):
    if hour > 17:
        return 'evening'
    elif hour > 11:
        return 'afternoon'
    elif hour > 5:
        return 'morning'
    else:
        return 'night'

df['day_part'] = df['hour_of_day'].apply(part_of_day) # add a new column indicating the part of the day based on the hour

# remove outliers using IQR method
for column in ['session_duration_sec',
               'cpu_usage_pct',
               'ram_usage_mb',
               'network_usage_mb',
               'battery_drain_pct']:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df[column + '_outlier'] = ((df[column] < Q1 - 1.5 * IQR) | (df[column] > Q3 + 1.5 * IQR)).astype(int)

'''
This calculates the chance of a user switching from one app to another. It first counts how many times each app transition
(previous_app >> app_name) appears in the dataset. Then, it calculates the total number of times the user switched away from each previous
app. Using these values, it computes the probability of each app transition by dividing the number of times the transition occurred by the
total number of transitions from that previous app. Finally, the code checks each row in the dataset, finds the probability
of that specific app transition, and saves it in a new column called previous_to_current_probability. If a transition has never been
seen before the code assigns a value of 0.0.
'''

transitions = df.groupby(['previous_app', 'app_name']).size().reset_index(name='count')
totals = transitions.groupby('previous_app')['count'].sum().reset_index(name='total')
transitions = transitions.merge(totals, on='previous_app')
transitions['trans_prob'] = transitions['count']/transitions['total']

lookup = dict(zip(zip(transitions['previous_app'], transitions['app_name']), transitions['trans_prob']))
df['previous_to_current_probability'] = df.apply(lambda r: lookup.get((r['previous_app'], r['app_name']), 0.0), axis=1)

df.to_csv('preprocessed_dataset.csv', index=False) # save preprocessed dataset
