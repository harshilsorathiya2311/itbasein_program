import logging
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from django.db.models import Count, Q

logger = logging.getLogger(__name__)

TEXT_WEIGHT = 0.35
NUMERIC_WEIGHT = 0.40
CATEGORICAL_WEIGHT = 0.25


class CarRecommender:
    def __init__(self):
        self._car_data = None
        self._feature_matrix = None
        self._tfidf_matrix = None
        self._numeric_scaled = None
        self._categorical_encoded = None
        self._tfidf = TfidfVectorizer(stop_words='english', max_features=500)
        self._scaler = StandardScaler()
        self._knn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute')
        self._dirty = True

    def _load_and_build(self):
        from cars.models import Car
        cars = Car.objects.filter(is_available=True).select_related('brand')
        if not cars:
            self._car_data = pd.DataFrame()
            return

        records = []
        for c in cars:
            records.append({
                'id': c.id,
                'brand': c.brand.name,
                'name': c.name,
                'price': float(c.price),
                'fuel_type': c.fuel_type,
                'transmission': c.transmission,
                'mileage': float(c.mileage),
                'seating': c.seating_capacity,
                'body_type': c.body_type,
                'safety_rating': c.safety_rating,
                'engine_cc': float(c.engine_cc or 0),
                'power': float(c.power or 0),
                'text': f"{c.brand.name} {c.name} {c.fuel_type} {c.transmission} {c.body_type} {c.description}".lower(),
            })

        self._car_data = pd.DataFrame(records)
        self._build_feature_matrix()

    def _build_feature_matrix(self):
        df = self._car_data
        if df.empty:
            return

        self._tfidf_matrix = self._tfidf.fit_transform(df['text'])
        self._tfidf_matrix = self._tfidf_matrix.toarray()

        numeric = df[['price', 'mileage', 'seating', 'engine_cc', 'power']].fillna(0)
        self._numeric_scaled = self._scaler.fit_transform(numeric)

        cat_df = pd.get_dummies(df[['fuel_type', 'transmission', 'body_type']])
        self._categorical_encoded = cat_df.values

        tfidf_weighted = self._tfidf_matrix * TEXT_WEIGHT
        numeric_weighted = self._numeric_scaled * NUMERIC_WEIGHT
        cat_weighted = self._categorical_encoded * CATEGORICAL_WEIGHT

        self._feature_matrix = np.hstack([tfidf_weighted, numeric_weighted, cat_weighted])
        self._knn.fit(self._feature_matrix)
        self._dirty = False

    def recommend(self, preferences, n=5):
        from cars.models import Car
        self._load_and_build()

        if self._car_data is None or self._car_data.empty:
            logger.warning('No car data available for recommendations')
            return []

        candidates = self._filter_candidates(preferences)
        explanations = []

        if candidates.empty:
            logger.info('No exact matches, falling back to closest cars')
            candidates = self._fallback_closest(preferences)
            explanations = ['No exact match — closest available option']
        else:
            explanations = self._generate_explanations(preferences)

        if candidates.empty:
            return []

        query_vec = self._build_query_vector(preferences)
        if query_vec is not None and len(candidates) > 1:
            candidate_indices = candidates.index.tolist()
            candidate_features = self._feature_matrix[candidate_indices]
            sims = cosine_similarity(query_vec.reshape(1, -1), candidate_features)[0]
            sims = np.nan_to_num(sims, nan=0.3)
            candidates = candidates.copy()
            base = 0.3
            candidates['_score'] = base + (1 - base) * (sims - sims.min()) / max(sims.max() - sims.min(), 1e-6)
            candidates = candidates.sort_values('_score', ascending=False)
        else:
            candidates = candidates.head(n).copy()
            candidates['_score'] = 0.5

        min_possible_score = 50 if query_vec is not None else 50

        top_n = candidates.head(n)
        car_ids = top_n['id'].tolist()
        score_map = dict(zip(top_n['id'], top_n['_score']))
        cars = list(Car.objects.filter(id__in=car_ids).select_related('brand'))
        cars.sort(key=lambda c: car_ids.index(c.id))

        results = []
        for car in cars:
            raw = score_map.get(car.id, 0.5)
            pct = max(0, min(100, round(raw * 100)))
            if pct < 5 and explanations:
                pct = max(pct, 50)
            why = self._why_this_car(car, preferences, pct)
            results.append({
                'car': car,
                'score': pct,
                'score_raw': round(raw, 3),
                'explanation': why,
                'explanations': explanations,
            })

        return results

    def _filter_candidates(self, prefs):
        df = self._car_data.copy()

        min_p = prefs.get('min_price')
        max_p = prefs.get('max_price')
        brand = prefs.get('brand')
        fuel = prefs.get('fuel_type')
        trans = prefs.get('transmission')
        min_seat = prefs.get('min_seating')
        body = prefs.get('body_type')
        min_safety = prefs.get('safety_priority')
        max_mileage = prefs.get('max_mileage')

        if min_p:
            try:
                df = df[df['price'] >= float(min_p)]
            except (ValueError, TypeError):
                pass
        if max_p:
            try:
                df = df[df['price'] <= float(max_p)]
            except (ValueError, TypeError):
                pass
        if brand:
            df = df[df['brand'].str.lower() == brand.lower()]
        if fuel:
            df = df[df['fuel_type'].str.lower() == fuel.lower()]
        if trans:
            df = df[df['transmission'].str.lower() == trans.lower()]
        if min_seat:
            try:
                df = df[df['seating'] >= int(min_seat)]
            except (ValueError, TypeError):
                pass
        if body:
            df = df[df['body_type'].str.lower() == body.lower()]
        if min_safety:
            try:
                df = df[df['safety_rating'] >= int(min_safety)]
            except (ValueError, TypeError):
                pass
        if max_mileage:
            try:
                df = df[df['mileage'] <= float(max_mileage)]
            except (ValueError, TypeError):
                pass

        return df

    def _fallback_closest(self, prefs):
        df = self._car_data.copy()
        query_vec = self._build_query_vector(prefs)
        if query_vec is None:
            return df.head(5)

        sims = cosine_similarity(query_vec.reshape(1, -1), self._feature_matrix)[0]
        df = df.copy()
        df['_sim'] = sims
        df = df.sort_values('_sim', ascending=False)
        return df.head(10)

    def _build_query_vector(self, prefs):
        if self._car_data is None or self._car_data.empty:
            return None

        brand = prefs.get('brand', '')
        fuel = prefs.get('fuel_type', '')
        trans = prefs.get('transmission', '')
        body = prefs.get('body_type', '')
        query_text = f"{brand} {fuel} {trans} {body}".lower().strip()

        if query_text:
            tfidf_vec = self._tfidf.transform([query_text]).toarray()
        else:
            tfidf_vec = np.zeros((1, self._tfidf_matrix.shape[1]))

        try:
            q_price = float(prefs.get('max_price', 0) or 0)
        except (ValueError, TypeError):
            q_price = 0.0
        try:
            q_mileage = float(prefs.get('max_mileage', 0) or 0)
        except (ValueError, TypeError):
            q_mileage = 0.0
        try:
            q_seating = float(prefs.get('min_seating', 0) or 0)
        except (ValueError, TypeError):
            q_seating = 0.0

        query_num = np.array([[
            q_price,
            q_mileage,
            q_seating,
            0.0,
            0.0,
        ]])
        query_num_scaled = self._scaler.transform(query_num)

        cat_keys = ['fuel_type', 'transmission', 'body_type']
        full_cat_df = pd.get_dummies(self._car_data[cat_keys])
        query_cat = pd.DataFrame(0, index=[0], columns=full_cat_df.columns)
        for pref_key, col_prefix in [('fuel_type', 'fuel_type_'), ('transmission', 'transmission_'), ('body_type', 'body_type_')]:
            val = prefs.get(pref_key, '')
            if val:
                col = col_prefix + val
                if col in query_cat.columns:
                    query_cat[col] = 1

        query_cat = query_cat[full_cat_df.columns].fillna(0).values

        return np.hstack([
            tfidf_vec * TEXT_WEIGHT,
            query_num_scaled * NUMERIC_WEIGHT,
            query_cat * CATEGORICAL_WEIGHT,
        ])

    def _generate_explanations(self, prefs):
        reasons = []
        if prefs.get('max_price') or prefs.get('min_price'):
            reasons.append('within your budget')
        if prefs.get('brand'):
            reasons.append(f"matched brand {prefs['brand']}")
        if prefs.get('fuel_type'):
            reasons.append(f"{prefs['fuel_type']} fuel type")
        if prefs.get('transmission'):
            reasons.append(f"{prefs['transmission']} transmission")
        if prefs.get('body_type'):
            reasons.append(f"{prefs['body_type']} body type")
        if prefs.get('min_seating'):
            reasons.append(f"seats {prefs['min_seating']}+")
        return reasons if reasons else ['matches your preferences']

    def _why_this_car(self, car, prefs, score):
        parts = []
        if prefs.get('max_price'):
            try:
                if float(car.price) <= float(prefs['max_price']):
                    parts.append(f"Under ${float(prefs['max_price']):,.0f}")
            except (ValueError, TypeError):
                pass
        if prefs.get('min_price'):
            try:
                if float(car.price) >= float(prefs['min_price']):
                    parts.append(f"Above ${float(prefs['min_price']):,.0f}")
            except (ValueError, TypeError):
                pass
        if prefs.get('brand') and car.brand.name.lower() == prefs['brand'].lower():
            parts.append(f"Preferred brand: {car.brand.name}")
        if prefs.get('fuel_type') and car.fuel_type.lower() == prefs['fuel_type'].lower():
            parts.append(f"{car.fuel_type} engine")
        if prefs.get('transmission') and car.transmission.lower() == prefs['transmission'].lower():
            parts.append(f"{car.transmission} transmission")
        if prefs.get('body_type') and car.body_type.lower() == prefs['body_type'].lower():
            parts.append(f"{car.body_type} body type")
        if prefs.get('min_seating'):
            try:
                if car.seating_capacity >= int(prefs['min_seating']):
                    parts.append(f"Seats {car.seating_capacity}")
            except (ValueError, TypeError):
                pass
        if prefs.get('max_mileage'):
            try:
                if float(car.mileage) <= float(prefs['max_mileage']):
                    parts.append(f"Great mileage: {car.mileage} kmpl")
            except (ValueError, TypeError):
                pass
        if parts:
            return ' | '.join(parts[:3])
        if score >= 80:
            return 'Top match based on your preferences'
        elif score >= 60:
            return 'Strong match across multiple features'
        else:
            return 'Closest available option'


class BookingPredictor:
    def __init__(self):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder, StandardScaler
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
