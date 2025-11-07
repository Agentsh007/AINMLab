import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ----------------------------
# 1. Load the dataset
data = pd.read_csv("spam_mail.csv", encoding="latin-1")
data = data[['Category', 'Messages']]  # Keep only necessary columns
data.columns = ['label', 'message']  # Rename for clarity

# ----------------------------
# 2. Split into training and test sets (70% train, 30% test)
X = data['message']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ----------------------------
# 3. Convert text into numerical features
vectorizer = CountVectorizer()
X_train_features = vectorizer.fit_transform(X_train)
X_test_features = vectorizer.transform(X_test)

# ----------------------------
# 4. Train the model
model = MultinomialNB()
model.fit(X_train_features, y_train)

# ----------------------------
# 5. Evaluate the model on test data
y_pred = model.predict(X_test_features)

accuracy = accuracy_score(y_test, y_pred) * 100
print(f"\nModel Accuracy: {accuracy:.2f}%")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=["Actual Ham", "Actual Spam"], columns=["Pred Ham", "Pred Spam"])
print("\nConfusion Matrix:\n", cm_df)

# ----------------------------
# 6. Take user input and test manually
print("\n --- Test Your Own Message --- ")
user_input = input("Enter a message : ").strip()
# Transform user input using same vectorizer
user_input_features = vectorizer.transform([user_input])
# Predict
prediction = model.predict(user_input_features)[0]
prob = model.predict_proba(user_input_features)[0]

print(f"\nPrediction: {prediction.upper()}")
print(f"Probability -> Ham: {prob[0]:.2f}, Spam: {prob[1]:.2f}")
print("-" * 40)
