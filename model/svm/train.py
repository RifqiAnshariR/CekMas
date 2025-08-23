import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib

DATASET_SENTIMENT = "../data/svm/dataset_sentiment.csv"
DATASET_CATEGORY = "../data/svm/dataset_category.csv"
SENTIMENT_MODEL = "./model/model_sentiment.pkl"
CATEGORY_MODEL = "./model/model_category.pkl"

def train_model(data_path, text_col, label_col, test_size, random_state):
    df = pd.read_csv(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        df[text_col], df[label_col], test_size=test_size, random_state=random_state
    )
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("svm", LinearSVC())
    ])
    pipeline.fit(X_train, y_train)
    return pipeline, X_test, y_test

def export_model(model, path):
    joblib.dump(model, path)
    print(f"Model disimpan di {path}")

def load_model(path):
    if os.path.exists(path):
        return joblib.load(path)
    else:
        return None

def main():
    # Sentiment
    sentimen_clf, _, _ = train_model(DATASET_SENTIMENT, "teks", "sentiment", 0.2, 42)
    export_model(sentimen_clf, SENTIMENT_MODEL)

    # Category
    kategori_clf, _, _ = train_model(DATASET_CATEGORY, "teks", "category", 0.2, 42)
    export_model(kategori_clf, CATEGORY_MODEL)

if __name__ == "__main__":
    main()
