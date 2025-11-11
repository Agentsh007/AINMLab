import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

# data read
data = pd.read_csv('spam_mail.csv')
data=data[['Category','Messages']]
data.columns=['label','message']
data['label'] = data['label'].map({'ham': 1, 'spam': 0})

#train test data split
X=data['message']
y=data['label']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

#feature extract
vectorizer=CountVectorizer()
X_train_features=vectorizer.fit_transform(X_train)
X_test_features=vectorizer.transform(X_test)

#model
model=MultinomialNB()
model.fit(X_train_features,y_train)

y_pred=model.predict(X_test_features)
accracy=accuracy_score(y_test,y_pred)
print(f"\nAccuracy Score:{accracy:.2f}%")
print("\n Classification Report:\n",classification_report(y_test,y_pred))

cm=confusion_matrix(y_test,y_pred)
cm_df=pd.DataFrame(cm,index=["Actua Ham","Actual Spam"],columns=["pred ham","pred spam"])
print(f"\n Confusion Matrix:\n",cm_df)

print("----Enter Your Own Message---")
# user_input=input("\nEnter message:").strip()
# user_input_feature=vectorizer.transform([user_input])
# prediction=model.predict(user_input_feature)[0]
# prob=model.predict_proba(user_input_feature)[0]

# print(f"\n predicttion:{prediction.upper()}")
# print(f"\n prabability Ham->{prob[0]:.2f},spam->{prob[1]:.2f}")
# print("-"*42)

messages=[]
while True:
    msg=input("\n Ener your message:").strip()
    if msg=="":
     break
    messages.append(msg)

if not messages:
    print("no message.")
    
else:
    features=vectorizer.transform(messages)
    pred=model.predict(features)
    prob=model.predict_proba(features)
    for i,(m,p,pr) in enumerate(zip(messages,pred,prob),1):
        pred_label="Ham" if p == 1 else "Spam"
        print(f"\n message{i}:{m}\n prediction:{p}({pred_label})\n probabilities->{pr[0]:.2f}(ham),{pr[1]:.2f}(spam)")
    print("-"*42)