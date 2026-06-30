from sklearn.model_selection import train_test_split

try:
    from machine_learning.features import  run_features
except ImportError:
    from features import  run_features

(INPUT_FEATURES, feature_matrix, predicted_next_app, anomaly) = run_features()

def run_split():
    # next app prediction
    X_train, X_test, y_train_app, y_test_app = train_test_split(
        feature_matrix,
        predicted_next_app,
        test_size=0.2,
        random_state=42
    )

    #anomaly detection
    X_train, X_test, y_train_anomaly, y_test_anomaly = train_test_split(
        feature_matrix,
        anomaly,
        test_size=0.2,
        random_state=42,
        stratify=anomaly
    )

    return (X_train, X_test, y_train_app, y_test_app, y_train_anomaly, y_test_anomaly)
