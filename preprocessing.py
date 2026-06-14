import pandas as pd

df = pd.read_csv('dataset.csv')

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['previous_app'] = df['previous_app'].fillna('NONE') # based on the missing value analysis above[2nd cell], only this column contains missing values

df['session_duration_hms'] = pd.to_timedelta(df['session_duration_hms'])
df['session_duration_sec'] = df['session_duration_sec'].astype(int)
# convert session_duration_hms from string to timedelta and ensure session_duration_sec is stored as integer

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

transitions = df.groupby(['previous_app', 'app_name']).size().reset_index(name='count')
totals = transitions.groupby('previous_app')['count'].sum().reset_index(name='total')
transitions = transitions.merge(totals, on='previous_app')
transitions['trans_prob'] = transitions['count']/transitions['total']

lookup = dict(zip(zip(transitions['previous_app'], transitions['app_name']), transitions['trans_prob']))
df['previous to current probability'] = df.apply(lambda r: lookup.get((r['previous_app'], r['app_name']), 0.0), axis=1)
