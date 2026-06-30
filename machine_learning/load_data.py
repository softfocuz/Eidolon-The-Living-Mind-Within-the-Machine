import pandas as pd
from sklearn.preprocessing import LabelEncoder

try:
    from machine_learning.preprocessed_data import importing_preprocessed_data
except ImportError:
    from preprocessed_data import importing_preprocessed_data

(preprocessed_data) = importing_preprocessed_data()

def run_load_data():
    app_name_prev = LabelEncoder()
    day_of_week = LabelEncoder()
    day_part = LabelEncoder()
    app_category = LabelEncoder()

    detected_apps = pd.concat([preprocessed_data['app_name'], preprocessed_data['previous_app']]).unique()
    app_name_prev.fit(detected_apps)

    preprocessed_data['app_name_label'] = app_name_prev.transform(preprocessed_data['app_name'])
    preprocessed_data['previous_app_label'] = app_name_prev.transform(preprocessed_data['previous_app'])

    preprocessed_data['day_of_week_label'] = day_of_week.fit_transform(preprocessed_data['day_of_week'])
    preprocessed_data['day_part_label'] = day_part.fit_transform(preprocessed_data['day_part'])
    preprocessed_data['app_category_label'] = app_category.fit_transform(preprocessed_data['app_category'])

    return (preprocessed_data, app_name_prev, day_of_week, day_part, app_category)

