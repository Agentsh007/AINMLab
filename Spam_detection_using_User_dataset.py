import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer


data = pd.read_csv('spam_mail.csv')               
data = data[['Category', 'Messages']]             


data['Category'] = data['Category'].map({'ham': 0, 'spam': 1})

x_train, x_test, y_train, y_test = train_test_split(
    data['Messages'], data['Category'], 
    test_size=0.3, random_state=40
)

vectorizer = CountVectorizer()
x_train = vectorizer.fit_transform(x_train)
x_test = vectorizer.transform(x_test)

model = MultinomialNB()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print("\n=== MODEL PERFORMANCE ===")
print(" Accuracy Score:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


print("\n=== TEST WITH YOUR OWN MESSAGE ===")
msg = input("Enter a message: ")

msg_vectorized = vectorizer.transform([msg])  
pred = model.predict(msg_vectorized)[0]       

print("Prediction:", "Spam" if pred == 1 else "💬 Ham")

print("\n=== TEST WITH 5 CUSTOM MESSAGES ===")
custom_data = []

for i in range(5):
    message = input(f"\nEnter message {i+1}: ")
    category = input("Enter category (ham/spam): ")
    custom_data.append({'Messages': message, 'Category': category})
custom_df = pd.DataFrame(custom_data)

X_custom = vectorizer.transform(custom_df['Messages'])
y_custom = custom_df['Category'].map({'ham': 0, 'spam': 1})

y_pred_custom = model.predict(X_custom)


print("\n=== RESULTS ON CUSTOM DATA ===")
print("Predicted labels:", y_pred_custom)
print("\n Accuracy Score:", accuracy_score(y_custom, y_pred_custom))
print("\nClassification Report:\n", classification_report(y_custom, y_pred_custom))
print("\nConfusion Matrix:\n", confusion_matrix(y_custom, y_pred_custom))
