import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# function to load the transcript from a YouTube URL

def train_model(csv_path="data/ragebait_dataset.csv"):
    data = pd.read_csv(csv_path)

    X = data["text"]
    y = data["label"]

    model = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("classifier", MultinomialNB())
    ])

    model.fit(X, y)
    return model

#this function predicts the label of the text and return the confidence scores for each label
def predict_text(model, text):
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    labels = model.classes_

    confidence = dict(zip(labels, probabilities))
    return prediction, confidence

#this function tests the model on a test set and returns the accuracy score
def test_model(csv_path="data/ragebait_dataset.csv"):
    data = pd.read_csv(csv_path)

    X = data["text"]
    y = data["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
#seeing the model as a pipeline ti fit it on the training data and then predict on the
#test data to get the accuracy score
    model = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("classifier", MultinomialNB())
    ])

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    return accuracy_score(y_test, predictions)