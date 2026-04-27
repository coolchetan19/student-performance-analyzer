import joblib
import numpy as np
import json

MODELS_DIR = 'models/'

FEATURES = ['attendance', 'midterm_marks', 'assignment_score', 'lab_performance',
            'mathematics', 'programming', 'dbms', 'english', 'operating_systems']

SUBJECT_FEATURES = ['mathematics', 'programming', 'dbms', 'english', 'operating_systems']
SUBJECT_LABELS = {
    'mathematics': 'Mathematics',
    'programming': 'Programming',
    'dbms': 'DBMS',
    'english': 'English',
    'operating_systems': 'Operating Systems'
}


def load_models():
    rf = joblib.load(MODELS_DIR + 'random_forest.pkl')
    xgb = joblib.load(MODELS_DIR + 'xgboost.pkl')
    lr = joblib.load(MODELS_DIR + 'logistic_regression.pkl')
    scaler = joblib.load(MODELS_DIR + 'scaler.pkl')
    le = joblib.load(MODELS_DIR + 'label_encoder.pkl')
    return rf, xgb, lr, scaler, le


def get_risk_level(category, attendance, consistency_score):
    if category == 'Excellent' and attendance >= 85:
        return 'High Performer 🌟'
    elif category in ['Weak'] or attendance < 60:
        return 'High Risk ⚠️'
    elif category == 'Average' or attendance < 75:
        return 'At-Risk 🔔'
    else:
        return 'Safe ✅'


def get_subject_analysis(student_data):
    strengths, weaknesses = [], []
    for feat in SUBJECT_FEATURES:
        score = student_data[feat]
        label = SUBJECT_LABELS[feat]
        if score >= 75:
            strengths.append((label, score))
        elif score < 55:
            weaknesses.append((label, score))

    strengths.sort(key=lambda x: x[1], reverse=True)
    weaknesses.sort(key=lambda x: x[1])
    return strengths, weaknesses


def get_suggestions(category, attendance, strengths, weaknesses, student_data):
    suggestions = []

    if attendance < 75:
        suggestions.append("📅 Improve attendance — aim for at least 75% to avoid academic penalties.")
    if attendance < 60:
        suggestions.append("🚨 Critical: Attendance is dangerously low. Consult your academic advisor immediately.")

    for subj, score in weaknesses:
        if score < 40:
            suggestions.append(f"📚 {subj}: Score critically low ({score}/100). Seek tutoring or extra practice sessions.")
        else:
            suggestions.append(f"📖 {subj}: Needs improvement ({score}/100). Focus on solving past papers and textbook exercises.")

    if student_data['midterm_marks'] < 50:
        suggestions.append("📝 Midterm performance is weak — revise core concepts and practice timed mock tests.")

    if student_data['assignment_score'] < 55:
        suggestions.append("✏️ Assignment scores are low — submit assignments on time and seek feedback from instructors.")

    if student_data['lab_performance'] < 55:
        suggestions.append("🔬 Lab performance needs attention — spend extra time on practical exercises and experiments.")

    if category == 'Excellent':
        suggestions.append("🏆 Excellent performance! Consider mentoring peers and participating in competitions.")
        suggestions.append("🎯 Explore advanced topics, research projects, or internships to further grow.")
    elif category == 'Good':
        suggestions.append("💪 Good work! Identify your weakest subject and focus on bringing it up to match your strengths.")

    if not suggestions:
        suggestions.append("✅ You are on track. Maintain consistency and keep up the great work!")

    return suggestions


def generate_report(student_data: dict, model_choice: str = 'random_forest') -> dict:
    rf, xgb, lr, scaler, le = load_models()

    import pandas as pd
    X = pd.DataFrame([[student_data[f] for f in FEATURES]], columns=FEATURES)

    if model_choice == 'random_forest':
        model = rf
        pred_enc = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
    elif model_choice == 'xgboost':
        model = xgb
        pred_enc = model.predict(X)[0]
        proba = model.predict_proba(X)[0]
    else:
        X_sc = scaler.transform(X)
        model = lr
        pred_enc = model.predict(X_sc)[0]
        proba = model.predict_proba(X_sc)[0]

    category = le.inverse_transform([pred_enc])[0]
    class_proba = {le.classes_[i]: round(float(p) * 100, 1) for i, p in enumerate(proba)}

    subject_scores = {SUBJECT_LABELS[f]: student_data[f] for f in SUBJECT_FEATURES}
    avg_subject = np.mean([student_data[f] for f in SUBJECT_FEATURES])

    # Consistency: std of all numeric scores
    all_scores = [student_data[f] for f in FEATURES]
    consistency_score = 100 - np.std(all_scores)

    risk_level = get_risk_level(category, student_data['attendance'], consistency_score)
    strengths, weaknesses = get_subject_analysis(student_data)
    suggestions = get_suggestions(category, student_data['attendance'], strengths, weaknesses, student_data)

    overall_score = round(
        student_data['midterm_marks'] * 0.25 +
        student_data['assignment_score'] * 0.15 +
        student_data['lab_performance'] * 0.15 +
        avg_subject * 0.30 +
        student_data['attendance'] * 0.15, 1
    )

    return {
        'category': category,
        'risk_level': risk_level,
        'overall_score': overall_score,
        'confidence': class_proba,
        'subject_scores': subject_scores,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'suggestions': suggestions,
        'consistency': round(consistency_score, 1),
        'attendance': student_data['attendance'],
        'midterm': student_data['midterm_marks'],
        'assignment': student_data['assignment_score'],
        'lab': student_data['lab_performance'],
    }
