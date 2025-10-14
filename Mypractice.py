import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.naive_bayes  import MultinomialNB 
from sklearn.metrics import accuracy_score, classification_report
train_data = pd.read_csv("spam.csv")
train_data = train_data[['v1','v2']]
train_data.columns = ['label','message']

x_train_data = train_data['message']
y_train_data = train_data['label']

test_data = pd.read_csv("spam_mail.csv")
x_test_data = test_data['Masseges']
y_test_data = test_data['Category']

vectorizer = CountVectorizer()
x_train_features = vectorizer.fit_transform(x_train_data)
x_test_features = vectorizer.transform(x_test_data)

model = MultinomialNB()
model.fit(x_train_features,y_train_data)

y_pred = model.predict(x_test_features)

accuracy = accuracy_score(y_test_data, y_pred) *100
print(f"Test Accuracy on spam_mail.csv: {accuracy:.2f}%")
print(f"\n Classification Report\n ", classification_report(y_test_data,y_pred))

results = pd.DataFrame({
    "Messages":x_train_data,
    "Category":y_train_data,
    "Predicted": y_pred
})

print(results.head(10))

results.to_csv("spam_mail_results.csv",index=False)
print("Results saved")