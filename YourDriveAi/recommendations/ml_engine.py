import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from cars.models import Car, Brand

class CarRecommender:
    def __init__(self):
        self.car_data = None
        self.feature_matrix = None
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.knn = NearestNeighbors(n_neighbors=5, metric='cosine')

    def load_car_data(self):
        cars = Car.objects.filter(is_available=True).select_related('brand')
        if not cars:
            return None
        data = []
        for c in cars:
            features = f"{c.brand.name} {c.name} {c.fuel_type} {c.transmission} {c.description}"
            data.append({
                'id': c.id,
                'brand': c.brand.name,
                'name': c.name,
                'price': float(c.price),
                'fuel_type': c.fuel_type,
                'transmission': c.transmission,
                'mileage': float(c.mileage),
                'seating': c.seating_capacity,
                'features': features.lower(),
            })
        self.car_data = pd.DataFrame(data)
        return self.car_data

    def build_feature_matrix(self):
        if self.car_data is None or self.car_data.empty:
            return None
        tfidf_matrix = self.tfidf.fit_transform(self.car_data['features'])
        numeric_features = self.car_data[['price', 'mileage', 'seating']].fillna(0)
        scaler = StandardScaler()
        numeric_scaled = scaler.fit_transform(numeric_features)
        self.feature_matrix = np.hstack([tfidf_matrix.toarray(), numeric_scaled])
        self.knn.fit(self.feature_matrix)
        return self.feature_matrix

    def content_based_recommend(self, user_preferences, n=6):
        self.load_car_data()
        if self.car_data is None or self.car_data.empty:
            return []

        query_features = self._build_query_features(user_preferences)
        candidates = self.car_data.copy()

        if user_preferences.get('min_price'):
            candidates = candidates[candidates['price'] >= float(user_preferences['min_price'])]
        if user_preferences.get('max_price'):
            candidates = candidates[candidates['price'] <= float(user_preferences['max_price'])]
        if user_preferences.get('fuel_type'):
            candidates = candidates[candidates['fuel_type'].str.lower() == user_preferences['fuel_type'].lower()]
        if user_preferences.get('transmission'):
            candidates = candidates[candidates['transmission'].str.lower() == user_preferences['transmission'].lower()]
        if user_preferences.get('min_seating'):
            candidates = candidates[candidates['seating'] >= int(user_preferences['min_seating'])]

        if candidates.empty:
            candidates = self.car_data

        self.build_feature_matrix()
        if query_features is not None:
            distances, indices = self.knn.kneighbors(query_features, n_neighbors=min(n, len(self.feature_matrix)))
            recommended_ids = self.car_data.iloc[indices[0]]['id'].tolist()
        else:
            recommended_ids = candidates.head(n)['id'].tolist()

        return list(Car.objects.filter(id__in=recommended_ids).select_related('brand'))

    def _build_query_features(self, preferences):
        if self.car_data is None or self.car_data.empty:
            return None
        query_text = ' '.join([
            preferences.get('brand', ''),
            preferences.get('fuel_type', ''),
            preferences.get('transmission', ''),
        ]).lower().strip()

        if not query_text:
            return None

        query_tfidf = self.tfidf.transform([query_text])
        query_numeric = np.array([[
            float(preferences.get('max_price', 0) or 0),
            float(preferences.get('max_mileage', 0) or 0),
            float(preferences.get('min_seating', 0) or 0),
        ]])
        scaler = StandardScaler()
        scaler.fit(self.car_data[['price', 'mileage', 'seating']].fillna(0))
        query_numeric_scaled = scaler.transform(query_numeric)
        return np.hstack([query_tfidf.toarray(), query_numeric_scaled])


class BookingPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.is_trained = False

    def prepare_training_data(self):
        from bookings.models import Booking
        bookings = Booking.objects.select_related('user', 'car__brand').all()
        if len(bookings) < 10:
            return None, None

        data = []
        for b in bookings:
            data.append({
                'user_bookings': Booking.objects.filter(user=b.user).count(),
                'car_price': float(b.car.price),
                'car_mileage': float(b.car.mileage),
                'fuel_type': b.car.fuel_type,
                'transmission': b.car.transmission,
                'seating': b.car.seating_capacity,
                'is_weekend': 1 if b.booking_date.weekday() >= 5 else 0,
                'status': 1 if b.status in ['Approved', 'Completed'] else 0,
            })

        df = pd.DataFrame(data)
        for col in ['fuel_type', 'transmission']:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.label_encoders[col] = le

        X = df.drop('status', axis=1)
        y = df['status']
        return X, y

    def train(self):
        X, y = self.prepare_training_data()
        if X is None or len(X) < 10:
            return False
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        return True

    def predict_probability(self, booking_data):
        if not self.is_trained:
            self.train()
        if not self.is_trained:
            return 0.5, 'Medium'

        df = pd.DataFrame([booking_data])
        for col in ['fuel_type', 'transmission']:
            if col in df and col in self.label_encoders:
                val = df[col].iloc[0]
                if val in self.label_encoders[col].classes_:
                    df[col] = self.label_encoders[col].transform([val])[0]
                else:
                    df[col] = -1

        feature_cols = ['user_bookings', 'car_price', 'car_mileage', 'fuel_type', 'transmission', 'seating', 'is_weekend']
        for col in feature_cols:
            if col not in df:
                df[col] = 0

        X = self.scaler.transform(df[feature_cols])
        prob = self.model.predict_proba(X)[0][1]

        if prob >= 0.7:
            category = 'High Potential'
        elif prob >= 0.4:
            category = 'Medium'
        else:
            category = 'Low'

        return round(prob, 3), category


recommender = CarRecommender()
predictor = BookingPredictor()
