import joblib

def load_model(path):
    return joblib.load(path)

def main():
    # Sentiment
    sentimen_clf = load_model("./model/model_sentiment.pkl")

    # Category
    kategori_clf = load_model("./model/model_category.pkl")

    input_pengaduan = "Saya Rifqi. Waduh ada banyak sampah pak"

    pred_sentimen = sentimen_clf.predict([input_pengaduan])[0]
    pred_kategori = kategori_clf.predict([input_pengaduan])[0]

    print("Sentimen     :", pred_sentimen)
    print("Kategori     :", pred_kategori)

if __name__ == "__main__":
    main()