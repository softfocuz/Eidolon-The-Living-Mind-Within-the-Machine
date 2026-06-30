import os
import joblib

try:
    from machine_learning.features import run_features
    from machine_learning.load_data import run_load_data
    from machine_learning.train import run_train
except ImportError:
    from features import run_features
    from load_data import run_load_data
    from train import run_train

(INPUT_FEATURES, feature_matrix, predicted_next_app, anomaly) = run_features()
(preprocessed_data, app_name_prev, day_of_week, day_part, app_category) = run_load_data()
(markov_transition_table, next_app_all_results, next_app_top_model, next_app_top_model_name, next_app_top_model_type, anomaly_all_results, anomaly_all_confusion_matrices, best_anomaly_model, best_anomaly_model_name) = run_train()

def run_saving_model_script():
    os.makedirs('models', exist_ok=True)

    # save next app model
    if next_app_top_model_type == 'markov':
        joblib.dump(markov_transition_table, 'models/next_app_top_model.pkl')
        joblib.dump('markov', 'models/next_app_top_model_type.pkl')
    else:
        joblib.dump(next_app_top_model, 'models/next_app_top_model.pkl')
        joblib.dump('sklearn', 'models/next_app_top_model_type.pkl')

    # save anomaly model
    joblib.dump(best_anomaly_model, 'models/anomaly_top_model.pkl')

    # save encoders
    joblib.dump(app_name_prev, 'models/app_name_prev.pkl')
    joblib.dump(day_of_week, 'models/day_of_week.pkl')
    joblib.dump(day_part, 'models/day_part.pkl')
    joblib.dump(app_category, 'models/app_category.pkl')

    # save markov table
    joblib.dump(markov_transition_table, 'models/markov_transition_table.pkl')

    # save feature column order
    joblib.dump(INPUT_FEATURES, 'models/input_features.pkl')

run_saving_model_script()