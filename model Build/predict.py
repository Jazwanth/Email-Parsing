import os
import sys
import json
import joblib

# -------------------------
# Config: load from same folder as script
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, "email_model.pkl")
VECTORIZER_FILE = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load model + vectorizer
clf = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

# Get input
if len(sys.argv) < 3:
    print("Usage: python predict.py '<subject>' '<body>'")
    sys.exit(1)

subject = sys.argv[1]
body = sys.argv[2]
text = subject + " " + body

# Predict
X_vec = vectorizer.transform([text])
prediction = clf.predict(X_vec)[0]

# Output as JSON
output = {"context": prediction}
print(json.dumps(output, indent=2))
