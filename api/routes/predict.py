from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

router = APIRouter(prefix="/predict", tags=["predict"])

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'machine_learning', 'models')

next_app_model = joblib.load(os.path.join(MODELS_DIR, 'next_app_top_model.pkl'))
next_app_model_type = joblib.load(os.path.join(MODELS_DIR, 'next_app_top_model_type.pkl'))
anomaly_model = joblib.load(os.path.join(MODELS_DIR, 'anomaly_top_model.pkl'))
app_encoder = joblib.load(os.path.join(MODELS_DIR, 'app_name_prev.pkl'))
day_encoder = joblib.load(os.path.join(MODELS_DIR, 'day_of_week.pkl'))
daypart_encoder = joblib.load(os.path.join(MODELS_DIR, 'day_part.pkl'))
category_encoder = joblib.load(os.path.join(MODELS_DIR, 'app_category.pkl'))
markov_table = joblib.load(os.path.join(MODELS_DIR, 'markov_transition_table.pkl'))
input_features = joblib.load(os.path.join(MODELS_DIR, 'input_features.pkl'))

class PredictRequest(BaseModel):
    previous_app: str
    app_category: str
    hour_of_day: int
    day_of_week: str
    day_part: str
    is_weekend: int
    session_duration_min: int
    cpu_usage_pct: float
    ram_usage_mb: float
    network_usage_mb: float
    battery_drain_pct: float
    session_duration_sec_outlier: int
    cpu_usage_pct_outlier: int
    ram_usage_mb_outlier: int
    network_usage_mb_outlier: int
    battery_drain_pct_outlier: int
    previous_to_current_probability: float


def get_action(probability: float) -> str:
    if probability >= 0.80:
        return 'preload'
    elif probability >= 0.50:
        return 'notify'
    else:
        return 'none'

@router.post("/")
def predict(request: PredictRequest):
    try:
        prev_app_encoded = int(app_encoder.transform([request.previous_app])[0])
        category_encoded = int(category_encoder.transform([request.app_category])[0])
        day_encoded = int(day_encoder.transform([request.day_of_week])[0])
        daypart_encoded = int(daypart_encoder.transform([request.day_part])[0])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Unknown value: {str(e)}")

    feature_values = {
        'previous_app_label': prev_app_encoded,
        'app_category_label': category_encoded,
        'hour_of_day': request.hour_of_day,
        'day_of_week_label': day_encoded,
        'day_part_label': daypart_encoded,
        'is_weekend': request.is_weekend,
        'session_duration_min': request.session_duration_min,
        'cpu_usage_pct': request.cpu_usage_pct,
        'ram_usage_mb': request.ram_usage_mb,
        'network_usage_mb': request.network_usage_mb,
        'battery_drain_pct': request.battery_drain_pct,
        'session_duration_sec_outlier': request.session_duration_sec_outlier,
        'cpu_usage_pct_outlier': request.cpu_usage_pct_outlier,
        'ram_usage_mb_outlier': request.ram_usage_mb_outlier,
        'network_usage_mb_outlier': request.network_usage_mb_outlier,
        'battery_drain_pct_outlier': request.battery_drain_pct_outlier,
        'previous_to_current_probability': request.previous_to_current_probability,
    }

    X = np.array([[feature_values[f] for f in input_features]])

    if next_app_model_type == 'markov':
        prev_app_name = request.previous_app
        if prev_app_name in markov_table:
            app_probs = markov_table[prev_app_name]
        else:
            app_probs = {app: 1/len(app_encoder.classes_) for app in app_encoder.classes_}
    else:
        # use sklearn model's predict_proba for all app probabilities
        proba = next_app_model.predict_proba(X)[0]
        app_probs = {
            app_encoder.classes_[i]: float(proba[i])
            for i in range(len(app_encoder.classes_))
        }

    # sort all apps by probability (highest first)
    sorted_predictions = sorted(
        [{'app': app, 'probability': round(prob, 4), 'action': get_action(prob)}
         for app, prob in app_probs.items()],
        key=lambda x: x['probability'],
        reverse=True
    )

    # predict anomaly
    anomaly_pred = int(anomaly_model.predict(X)[0])
    anomaly_proba = float(anomaly_model.predict_proba(X)[0][1]) if hasattr(anomaly_model, 'predict_proba') else None

    # build response
    top = sorted_predictions[0]
    return {
        'predictions': sorted_predictions,
        'top_prediction': {
            'app': top['app'],
            'probability': top['probability'],
            'action': top['action'],
        },
        'anomaly': {
            'is_anomaly': bool(anomaly_pred),
            'probability': anomaly_proba,
        }
    }