import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from xgboost import XGBClassifier
import joblib
import os
import json

# Load data
df = pd.read_csv('data/student_data.csv')

FEATURES = ['attendance', 'midterm_marks', 'assignment_score', 'lab_performance',
            'mathematics', 'programming', 'dbms', 'english', 'operating_systems']

X = df[FEATURES]
y = df['performance_label']

# Encode labels
le = LabelEncoder()
le.fit(['Weak', 'Average', 'Good', 'Excellent'])
y_enc = le.transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

# Scale
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

# ── Models ──────────────────────────────────────────────
rf = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

xgb = XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.1,
                     use_label_encoder=False, eval_metric='mlogloss', random_state=42)
xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)
xgb_acc = accuracy_score(y_test, xgb_pred)

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_sc, y_train)
lr_pred = lr.predict(X_test_sc)
lr_acc = accuracy_score(y_test, lr_pred)

print(f"Random Forest Accuracy : {rf_acc:.4f}")
print(f"XGBoost Accuracy       : {xgb_acc:.4f}")
print(f"Logistic Regression    : {lr_acc:.4f}")
print("\nRandom Forest Report:")
print(classification_report(y_test, rf_pred, target_names=le.classes_))

# ── Save models ─────────────────────────────────────────
os.makedirs('models', exist_ok=True)
joblib.dump(rf, 'models/random_forest.pkl')
joblib.dump(xgb, 'models/xgboost.pkl')
joblib.dump(lr, 'models/logistic_regression.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(le, 'models/label_encoder.pkl')

# Save metrics
metrics = {
    'random_forest': round(rf_acc, 4),
    'xgboost': round(xgb_acc, 4),
    'logistic_regression': round(lr_acc, 4),
    'features': FEATURES,
    'classes': list(le.classes_)
}
with open('models/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("\nAll models saved!")