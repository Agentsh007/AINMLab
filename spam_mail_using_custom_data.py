import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# ----------------------------
# 1. Training dataset (manually defined)
train_data = pd.DataFrame({
    'label': ['ham', 'spam', 'ham', 'spam', 'ham'],
    'message': [
        "Hi, how are you?",
        "Congratulations! You've won a free lottery ticket.",
        "Let's meet tomorrow at the library.",
        "You have been selected for a cash prize! Click now.",
        "Are you coming to the party tonight?"
    ]
})

X_train_data = train_data['message']
y_train_data = train_data['label']

# ----------------------------
# 2. Testing dataset (manually defined)
test_data = pd.DataFrame({
    'Category': ['spam', 'ham', 'spam', 'ham'],
    'Masseges': [
        "Win a free vacation trip now!",
        "Can we talk later about the project?",
        "You have a chance to get a $500 gift card!",
        "Don't forget to bring your notebook to class."
    ]
})

X_test_data = test_data['Masseges']
y_test_data = test_data['Category']

# ----------------------------
# 3. Convert text to numerical features (Bag of Words)
vectorizer = CountVectorizer()
X_train_features = vectorizer.fit_transform(X_train_data)
X_test_features = vectorizer.transform(X_test_data)

# ----------------------------
# 4. Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train_features, y_train_data)

# ----------------------------
# 5. Predict on the test dataset
y_pred = model.predict(X_test_features)

# ----------------------------
# 6. Calculate accuracy and print report
accuracy = accuracy_score(y_test_data, y_pred) * 100
print(f"Test Accuracy: {accuracy:.2f}%")
print("\nClassification Report:\n", classification_report(y_test_data, y_pred))

# ----------------------------
# 7. Display results (Actual vs Predicted)
results = pd.DataFrame({
    "Message": X_test_data,
    "Actual": y_test_data,
    "Predicted": y_pred
})

print("\n--- Actual vs Predicted ---")
print(results)

# ----------------------------
# 8. Optionally save results
results.to_csv("spam_mail_results.csv", index=False)
print("\nResults saved to spam_mail_results.csv")
