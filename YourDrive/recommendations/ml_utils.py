import numpy as np
import pandas as pd
import os
import pickle
from django.conf import settings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


def prepare_car_dataset():
    from cars.models import Car, Brand
    cars = Car.objects.select_related('brand').all()
    if not cars:
        return None, None

    data = []
    for car in cars:
        data.append({
            'car_id': car.id,
            'brand': car.brand.name,
            'name': car.name,
            'price': float(car.price),
            'fuel_type': car.fuel_type,
            'transmission': car.transmission,
            'seats': car.seats,
            'mileage': float(car.mileage),
            'engine_cc': float(car.engine_cc) if car.engine_cc else 0,
            'horsepower': car.horsepower if car.horsepower else 0,
            'is_available': int(car.is_available),
        })

    df = pd.DataFrame(data)
    return df, cars


def encode_features(df):
    le_dict = {}
    df_encoded = df.copy()

    label_cols = ['brand', 'name', 'fuel_type', 'transmission']
    for col in label_cols:
        le = LabelEncoder()
        df_encoded[col + '_enc'] = le.fit_transform(df_encoded[col].astype(str))
        le_dict[col] = le

    return df_encoded, le_dict


def train_recommendation_model():
    df, cars_queryset = prepare_car_dataset()
    if df is None:
        return None, None, None, None

    df_encoded, le_dict = encode_features(df)

    feature_cols = ['brand_enc', 'price', 'fuel_type_enc', 'transmission_enc',
                    'seats', 'mileage', 'engine_cc', 'horsepower']
    X = df_encoded[feature_cols].values
    y = df_encoded['car_id'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train multiple models
    models = {
        'logistic_regression': LogisticRegression(max_iter=1000, random_state=42),
        'decision_tree': DecisionTreeClassifier(random_state=42),
        'knn': KNeighborsClassifier(n_neighbors=3),
    }

    trained_models = {}
    accuracies = {}

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        trained_models[name] = model
        accuracies[name] = acc

    # Save models
    model_dir = settings.BASE_DIR / 'ml_models'
    model_dir.mkdir(exist_ok=True)

    with open(model_dir / 'scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open(model_dir / 'label_encoders.pkl', 'wb') as f:
        pickle.dump(le_dict, f)
    with open(model_dir / 'models.pkl', 'wb') as f:
        pickle.dump(trained_models, f)
    with open(model_dir / 'dataset.pkl', 'wb') as f:
        pickle.dump(df, f)
    with open(model_dir / 'accuracies.pkl', 'wb') as f:
        pickle.dump(accuracies, f)

    return trained_models, scaler, le_dict, df


def load_trained_models():
    model_dir = settings.BASE_DIR / 'ml_models'
    try:
        with open(model_dir / 'models.pkl', 'rb') as f:
            models = pickle.load(f)
        with open(model_dir / 'scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open(model_dir / 'label_encoders.pkl', 'rb') as f:
            le_dict = pickle.load(f)
        with open(model_dir / 'dataset.pkl', 'rb') as f:
            df = pickle.load(f)
        with open(model_dir / 'accuracies.pkl', 'rb') as f:
            accuracies = pickle.load(f)
        return models, scaler, le_dict, df, accuracies
    except FileNotFoundError:
        return None, None, None, None, None


def recommend_cars(user_budget=None, preferred_brand=None, preferred_fuel=None,
                   preferred_transmission=None, n_recommendations=5, algorithm='decision_tree'):
    models, scaler, le_dict, df, accuracies = load_trained_models()
    if models is None:
        result = train_recommendation_model()
        if result[0] is None:
            return [], {}
        models, scaler, le_dict, df = result[:4]

    model = models.get(algorithm, models.get('decision_tree'))

    # Filter candidates
    candidates = df.copy()
    if user_budget:
        candidates = candidates[candidates['price'] <= float(user_budget)]
    if preferred_brand:
        candidates = candidates[candidates['brand'].str.contains(preferred_brand, case=False, na=False)]
    if preferred_fuel:
        candidates = candidates[candidates['fuel_type'] == preferred_fuel]
    if preferred_transmission:
        candidates = candidates[candidates['transmission'] == preferred_transmission]

    if candidates.empty:
        candidates = df.copy()

    # Encode candidates
    for col in ['brand', 'name', 'fuel_type', 'transmission']:
        le = le_dict[col]
        known_classes = set(le.classes_)
        candidates[col + '_enc'] = candidates[col].apply(
            lambda x: le.transform([x])[0] if x in known_classes else -1
        )

    feature_cols = ['brand_enc', 'price', 'fuel_type_enc', 'transmission_enc',
                    'seats', 'mileage', 'engine_cc', 'horsepower']
    X_candidates = candidates[feature_cols].values
    X_candidates_scaled = scaler.transform(X_candidates)

    predictions = model.predict(X_candidates_scaled)
    probabilities = model.predict_proba(X_candidates_scaled).max(axis=1)

    candidates = candidates.copy()
    candidates['predicted'] = predictions
    candidates['confidence'] = probabilities
    candidates = candidates.sort_values('confidence', ascending=False)

    top_recommendations = candidates.head(n_recommendations)

    results = []
    for _, row in top_recommendations.iterrows():
        results.append({
            'car_id': int(row['car_id']),
            'name': row['name'],
            'brand': row['brand'],
            'price': row['price'],
            'fuel_type': row['fuel_type'],
            'transmission': row['transmission'],
            'confidence': round(float(row['confidence']), 4),
        })

    return results, accuracies


def generate_accuracy_chart(accuracies):
    if not accuracies:
        return None

    fig, ax = plt.subplots(figsize=(8, 5))
    models_list = list(accuracies.keys())
    acc_values = [accuracies[m] * 100 for m in models_list]
    colors = ['#3498db', '#2ecc71', '#e74c3c']

    bars = ax.bar(models_list, acc_values, color=colors[:len(models_list)])
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('ML Model Accuracy Comparison')
    ax.set_ylim(0, 100)

    for bar, val in zip(bars, acc_values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f'{val:.1f}%', ha='center', va='bottom')

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str


def generate_booking_trends(bookings_data):
    if not bookings_data:
        return None

    df = pd.DataFrame(bookings_data)
    fig, ax = plt.subplots(figsize=(10, 5))

    if 'date' in df.columns:
        trend = df.groupby('date').size()
        trend.plot(kind='line', marker='o', ax=ax, color='#3498db')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Bookings')
        ax.set_title('Booking Trends Over Time')
        ax.grid(True, alpha=0.3)

    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str
