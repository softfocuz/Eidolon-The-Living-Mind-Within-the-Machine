try:
    from machine_learning.load_data import run_load_data
except ImportError:
    from load_data import run_load_data

load_data = run_load_data()

(preprocessed_data, app_name_prev, day_of_week, day_part, app_category) = run_load_data()

def run_features():
    INPUT_FEATURES = [
        'previous_app_label',
        'app_category_label',
        'hour_of_day',
        'day_of_week_label',
        'day_part_label',
        'is_weekend',
        'session_duration_min',
        'cpu_usage_pct',
        'ram_usage_mb',
        'network_usage_mb',
        'battery_drain_pct',
        'session_duration_sec_outlier',
        'cpu_usage_pct_outlier',
        'ram_usage_mb_outlier',
        'network_usage_mb_outlier',
        'battery_drain_pct_outlier',
        'previous_to_current_probability',
    ]

    predicted_next_app = preprocessed_data['app_name_label']
    anomaly = preprocessed_data['is_anomaly']
    feature_matrix = preprocessed_data[INPUT_FEATURES]

    return (INPUT_FEATURES, feature_matrix, predicted_next_app, anomaly)