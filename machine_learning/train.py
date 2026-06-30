import numpy as np

from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

try:
    from machine_learning.load_data import run_load_data
    from machine_learning.split import run_split
except ImportError:
    from load_data import run_load_data
    from split import run_split

(preprocessed_data, app_name_prev, day_of_week, day_part, app_category) = run_load_data()
(X_train, X_test, y_train_app, y_test_app, y_train_anomaly, y_test_anomaly) = run_split()

def run_train():
    train_rows = preprocessed_data.iloc[X_train.index]

    app_transition_counts = train_rows.groupby(
        ['previous_app', 'app_name']
    ).size().reset_index(name='switch_count')

    total_outgoing = app_transition_counts.groupby('previous_app')['switch_count'].sum().reset_index(name='total_switches')

    app_transition_counts = app_transition_counts.merge(total_outgoing, on='previous_app')

    app_transition_counts['probability_switch'] = (app_transition_counts['switch_count'] / app_transition_counts['total_switches'])

    '''
    I am choosing the Markov model first because it's designed to predict what comes next based on the current 
    state, I am using this as a starting point so that I can compare its results with other models later on, with that
    I will still choose the best model depending on its accuracy, if another model beats the 
    markov model's accuracy then I will choose that model instead
    '''

    markov_transition_table = {}
    for _, transition_row in app_transition_counts.iterrows():
        prev_app = transition_row['previous_app']
        next_app = transition_row['app_name']
        probability = transition_row['probability_switch']

        if prev_app not in markov_transition_table:
            markov_transition_table[prev_app] = {}
        markov_transition_table[prev_app][next_app] = probability

    def predict_next_app_markov(prev_app_label):
        prev_app_name = app_name_prev.inverse_transform([prev_app_label])[0]

        if prev_app_name not in markov_transition_table:
            return np.random.randint(0, len(app_name_prev.classes_))
        possible_next_apps = markov_transition_table[prev_app_name]
        predicted_next_app = max(possible_next_apps, key=possible_next_apps.get)
        return app_name_prev.transform([predicted_next_app])[0]

    test_rows = preprocessed_data.iloc[X_test.index]
    markov_predictions = test_rows['previous_app'].apply(lambda prev_app:
                                                         predict_next_app_markov(app_name_prev.transform([prev_app])[0])
                                                         )
    markov_results = {
        'accuracy': accuracy_score(y_test_app, markov_predictions),
        'precision': precision_score(y_test_app, markov_predictions, average='weighted', zero_division=0),
        'recall': recall_score(y_test_app, markov_predictions, average='weighted', zero_division=0),
        'f1': f1_score(y_test_app, markov_predictions, average='weighted', zero_division=0)
    }

    next_app_models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB()
    }
    next_app_all_results = {'Markov Chain': markov_results}

    next_app_top_model = None
    next_app_top_model_name = 'Markov Chain'
    next_app_top_model_type = 'markov'
    best_next_app_f1 = markov_results['f1']

    for model_name, model in next_app_models.items():
        model.fit(X_train, y_train_app)
        predictions = model.predict(X_test)

        results = {
            'accuracy': accuracy_score(y_test_app, predictions),
            'precision': precision_score(y_test_app, predictions, average='weighted', zero_division=0),
            'recall': recall_score(y_test_app, predictions, average='weighted', zero_division=0),
            'f1': f1_score(y_test_app, predictions, average='weighted', zero_division=0)
        }

        next_app_all_results[model_name] = results

        if results['f1'] > best_next_app_f1:
            best_next_app_f1 = results['f1']
            next_app_top_model = model
            next_app_top_model_name = model_name
            next_app_top_model_type = 'sklearn'

    # anomaly detection
    anomaly_models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB(),
        'Logistic Regression': LogisticRegression(random_state=42, class_weight='balanced',max_iter=1000)
    }

    anomaly_all_results = {}
    anomaly_all_confusion_matrices = {}

    best_anomaly_model = None
    best_anomaly_model_name = ''
    best_anomaly_recall = -1

    for model_name, model in anomaly_models.items():
        model.fit(X_train, y_train_anomaly)
        predictions = model.predict(X_test)

        results = {
            'accuracy': accuracy_score(y_test_anomaly, predictions),
            'precision': precision_score(y_test_anomaly, predictions, zero_division=0),
            'recall': recall_score(y_test_anomaly, predictions, zero_division=0),
            'f1': f1_score(y_test_anomaly, predictions, zero_division=0),
            'report': classification_report(y_test_anomaly, predictions, target_names=['Normal', 'Anomaly'], zero_division=0),
        }
        anomaly_all_results[model_name] = results
        anomaly_all_confusion_matrices[model_name] = confusion_matrix(y_test_anomaly, predictions)


        if results['recall'] > best_anomaly_recall:
            best_anomaly_recall = results['recall']
            best_anomaly_model = model
            best_anomaly_model_name = model_name

    return(markov_transition_table, next_app_all_results, next_app_top_model, next_app_top_model_name, next_app_top_model_type, anomaly_all_results, anomaly_all_confusion_matrices, best_anomaly_model, best_anomaly_model_name)




