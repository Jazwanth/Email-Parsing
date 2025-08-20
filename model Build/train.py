import os
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# -------------------------
# Config: save in same folder as script
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, "email_model.pkl")
VECTORIZER_FILE = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load dataset
with open("emails.json", "r") as f:
    data = json.load(f)

X = [d["subject"] + " " + d["body"] for d in data]
y = [d["label"] for d in data]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
clf = MultinomialNB()
clf.fit(X_train_vec, y_train)

# Save
joblib.dump(clf, MODEL_FILE)
joblib.dump(vectorizer, VECTORIZER_FILE)

print(f"✅ Model saved as {MODEL_FILE}")
print(f"✅ Vectorizer saved as {VECTORIZER_FILE}")
