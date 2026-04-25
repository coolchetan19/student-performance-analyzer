import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import random

np.random.seed(42)
random.seed(42)

n_students = 1000

def generate_student_data(n):
    data = []
    for i in range(n):
        # Performance tier
        tier = np.random.choice(['excellent', 'good', 'average', 'weak'], p=[0.15, 0.30, 0.35, 0.20])

        if tier == 'excellent':
            attendance = np.random.randint(85, 101)
            midterm = np.random.randint(75, 101)
            assignment = np.random.randint(80, 101)
            lab = np.random.randint(80, 101)
            math = np.random.randint(78, 101)
            programming = np.random.randint(75, 101)
            dbms = np.random.randint(78, 101)
            english = np.random.randint(75, 101)
            os_score = np.random.randint(78, 101)
        elif tier == 'good':
            attendance = np.random.randint(75, 95)
            midterm = np.random.randint(60, 85)
            assignment = np.random.randint(65, 85)
            lab = np.random.randint(65, 85)
            math = np.random.randint(60, 85)
            programming = np.random.randint(58, 82)
            dbms = np.random.randint(60, 83)
            english = np.random.randint(62, 84)
            os_score = np.random.randint(60, 83)
        elif tier == 'average':
            attendance = np.random.randint(60, 80)
            midterm = np.random.randint(45, 70)
            assignment = np.random.randint(48, 70)
            lab = np.random.randint(45, 70)
            math = np.random.randint(42, 68)
            programming = np.random.randint(40, 66)
            dbms = np.random.randint(42, 68)
            english = np.random.randint(45, 70)
            os_score = np.random.randint(42, 67)
        else:  # weak
            attendance = np.random.randint(30, 65)
            midterm = np.random.randint(20, 50)
            assignment = np.random.randint(20, 52)
            lab = np.random.randint(20, 50)
            math = np.random.randint(18, 48)
            programming = np.random.randint(15, 46)
            dbms = np.random.randint(18, 48)
            english = np.random.randint(20, 50)
            os_score = np.random.randint(18, 47)

        # Add noise
        subjects = [math, programming, dbms, english, os_score]
        avg_subject = np.mean(subjects)
        total_marks = (midterm * 0.3 + assignment * 0.2 + lab * 0.2 + avg_subject * 0.3)

        # Determine label
        if total_marks >= 80:
            label = 'Excellent'
        elif total_marks >= 65:
            label = 'Good'
        elif total_marks >= 50:
            label = 'Average'
        else:
            label = 'Weak'

        data.append({
            'student_id': f'STU{1000+i}',
            'attendance': min(100, attendance),
            'midterm_marks': min(100, midterm),
            'assignment_score': min(100, assignment),
            'lab_performance': min(100, lab),
            'mathematics': min(100, math),
            'programming': min(100, programming),
            'dbms': min(100, dbms),
            'english': min(100, english),
            'operating_systems': min(100, os_score),
            'performance_label': label
        })

    return pd.DataFrame(data)

df = generate_student_data(n_students)
df.to_csv('data/student_data.csv', index=False)
print("Dataset generated!")
print(df['performance_label'].value_counts())
print(df.describe())
