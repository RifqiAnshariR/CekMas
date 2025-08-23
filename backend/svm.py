import joblib

MODEL_SENTIMENT = "../model/svm/model/model_sentiment.pkl"
MODEL_CATEGORY = "../model/svm/model/model_category.pkl"

def load_model(path):
    return joblib.load(path)

def sentiment_classification(text):
    sentimen_clf = load_model(MODEL_SENTIMENT)
    return sentimen_clf.predict([text])[0]

def category_classification(text):
    kategori_clf = load_model(MODEL_CATEGORY)
    return kategori_clf.predict([text])[0]
