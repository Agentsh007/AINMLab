import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


data = pd.read_csv("spam_mail.csv", encoding="latin-1")
data = data[['Category', 'Messages']]
data.columns = ['label', 'message']
data['label'] = data['label'].map({'ham': 0, 'spam': 1})
print(" Label Conversion Preview:")
print(data['label'].head())
X = data['message']     
y = data['label']      

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

vectorizer = CountVectorizer()

X_train_features = vectorizer.fit_transform(X_train)

X_test_features = vectorizer.transform(X_test)

model = MultinomialNB()       
model.fit(X_train_features, y_train)  

y_pred = model.predict(X_test_features)

accuracy = accuracy_score(y_test, y_pred) * 100
print(f"\n Model Accuracy: {accuracy:.2f}%")

print("\n Classification Report:\n", classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(
    cm,
    index=["Actual Ham", "Actual Spam"],
    columns=["Predicted Ham", "Predicted Spam"]
)
print("\n Confusion Matrix:\n", cm_df)

print("\n --- Test Your Own Messages (press Enter on blank line to finish) ---")

messages = []
while True:
    msg = input("Enter a message (blank to finish): ").strip()
    if msg == "":
        break
    messages.append(msg)

if not messages:
    print(" No messages entered. Exiting manual test.")
else:  
    features = vectorizer.transform(messages)
  
    preds = model.predict(features)
    probs = model.predict_proba(features)
 
    print("\n================ RESULTS ================\n")
    for i, (m, p, pr) in enumerate(zip(messages, preds, probs), 1):
        print(f"Message {i}: {m}")
        print(f"Prediction: {' SPAM' if p == 1 else ' HAM'}")
        print(f"Confidence -> Ham: {pr[0]:.4f}, Spam: {pr[1]:.4f}")
        print("-" * 40)
