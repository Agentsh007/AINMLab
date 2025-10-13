import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from googletrans import Translator

# ----------------------------
# 1. Load the training dataset (spam.csv)
train_data = pd.read_csv("spam.csv", encoding="latin-1")
train_data = train_data[['v1', 'v2']]  # Keep only necessary columns
train_data.columns = ['label', 'message']  # Rename columns for clarity

X_train_data = train_data['message']  # Features
y_train_data = train_data['label']    # Labels

# ----------------------------
# 2. Load the test dataset (spam_mail.csv)
# Columns: Category (ham/spam), Masseges
test_data = pd.read_csv("spam_mail.csv")
X_test_data = test_data['Masseges']  # Features for testing
y_test_data = test_data['Category']  # True labels

# ----------------------------
# 3. Convert text to numerical features (Bag of Words)
vectorizer = CountVectorizer()
X_train_features = vectorizer.fit_transform(X_train_data)  # Fit on training data
X_test_features = vectorizer.transform(X_test_data)        # Transform test data

# ----------------------------
# 4. Train the model
model = MultinomialNB()
model.fit(X_train_features, y_train_data)

# ----------------------------
# 5. Predict on the test dataset
y_pred = model.predict(X_test_features)

# ----------------------------
# 6. Calculate accuracy and print report
accuracy = accuracy_score(y_test_data, y_pred) * 100
print(f"Test Accuracy on spam_mail.csv: {accuracy:.2f}%")
print("\nClassification Report:\n", classification_report(y_test_data, y_pred))

# ----------------------------
# 7. Display results (Actual vs Predicted)
results = pd.DataFrame({
    "Message": X_test_data,
    "Actual": y_test_data,
    "Predicted": y_pred
})

print(results.head(10))  # Show first 10 rows

# ----------------------------
# 8. Optionally save results to CSV
results.to_csv("spam_mail_results.csv", index=False)
print("Results saved to spam_mail_results.csv")

