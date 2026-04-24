# 🎓 Student Performance Analyzer

An ML-powered web application that analyzes student academic data and generates detailed performance reports with predictions, risk assessment, and personalized improvement suggestions.

---

## 🚀 Features

- **Multi-model Classification** — Random Forest, XGBoost, and Logistic Regression
- **Performance Categories** — Excellent / Good / Average / Weak
- **Risk Level Detection** — High Performer / Safe / At-Risk / High Risk
- **Subject-wise Analysis** — Identifies per-subject strengths and weaknesses
- **Personalized Suggestions** — Actionable improvement advice per student
- **Confidence Scores** — Model probability breakdown per category
- **Interactive Dashboard** — Built with Streamlit for clean, visual reports

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| ML Models | scikit-learn, XGBoost |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib |
| Language | Python 3.9+ |

---

## 📁 Project Structure

```
student-performance-analyzer/
├── app.py                      # Streamlit dashboard
├── requirements.txt
├── README.md
├── data/
│   ├── generate_data.py        # Synthetic dataset generator
│   └── student_data.csv        # Training dataset (1000 students)
├── models/
│   ├── train_models.py         # Model training pipeline
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── logistic_regression.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── metrics.json
└── utils/
    └── predictor.py            # Prediction + report engine
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/coolchetan19/student-performance-analyzer.git
cd student-performance-analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Data & Train Models
```bash
python data/generate_data.py
python models/train_models.py
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 📊 Input Features

| Feature | Description |
|---------|-------------|
| Attendance | Student attendance percentage (0–100) |
| Midterm Marks | Mid-semester exam score (0–100) |
| Assignment Score | Average assignment performance (0–100) |
| Lab Performance | Practical/lab score (0–100) |
| Mathematics | Subject score (0–100) |
| Programming | Subject score (0–100) |
| DBMS | Subject score (0–100) |
| English | Subject score (0–100) |
| Operating Systems | Subject score (0–100) |

---

## 📈 Model Performance

| Model | Accuracy |
|-------|----------|
| Random Forest | ~99.5% |
| XGBoost | ~99.5% |
| Logistic Regression | ~99.5% |

---

## ☁️ Deployment

### Streamlit Cloud
1. Push repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repo → set `app.py` as main file → Deploy

### Render
1. Create a new Web Service on [render.com](https://render.com)
2. Set build command: `pip install -r requirements.txt && python data/generate_data.py && python models/train_models.py`
3. Set start command: `streamlit run app.py --server.port $PORT`

---

## 👨‍💻 Developer

**Chetan Kumar Sambhawani**

- 🐙 GitHub: [github.com/coolchetan19](https://github.com/coolchetan19)
- 💼 LinkedIn: [linkedin.com/in/chetan-kumar-sambhawani-b1b833326](https://www.linkedin.com/in/chetan-kumar-sambhawani-b1b833326/)

---

## 📄 License

MIT License — free to use, modify, and distribute.
