import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Read data
data = pd.read_csv("spam_mail.csv", encoding="latin-1")
data = data[['Category', 'Messages']]
data.columns = ['label', 'message']
data['label'] = data['label'].map({'ham': 1, 'spam': 0})

# Train-test split
X = data['message']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Feature extraction
vectorizer = CountVectorizer()
X_train_features = vectorizer.fit_transform(X_train)
X_test_features = vectorizer.transform(X_test)

# Model training
model = MultinomialNB()
model.fit(X_train_features, y_train)

# Evaluation
y_pred = model.predict(X_test_features)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy Score: {accuracy * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(
    cm,
    index=["Actual Spam", "Actual Ham"],
    columns=["Predicted Spam", "Predicted Ham"]
)
print(f"\nConfusion Matrix:\n{cm_df}")

# ---- User Input Section ----
print("\n---- Enter Your Own Messages ----")

messages = []
while True:
    msg = input("\nEnter your message (press Enter to stop): ").strip()
    if msg == "":
        break
    messages.append(msg)

if not messages:
    print("No message entered.")
else:
    features = vectorizer.transform(messages)
    preds = model.predict(features)
    probs = model.predict_proba(features)

    for i, (m, p, pr) in enumerate(zip(messages, preds, probs), 1):
        pred_label = 'Ham' if p == 1 else 'Spam'
        print(f"\nMessage {i}: {m}")
        print(f"Prediction: {pred_label}")
        print(f"Probabilities -> Ham: {pr[1]:.2f}, Spam: {pr[0]:.2f}")
        print("-" * 42)
