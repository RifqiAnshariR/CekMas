import cv2
import easyocr
from rapidfuzz import fuzz, process
import numpy as np

DICTIONARY_NAME = "./data/ocr/nama.txt"
DICTIONARY_NUMBER = "./data/ocr/angka.txt"
DICTIONARY_GENDER = "./data/ocr/jenis_kelamin.txt"
ALLOW_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
TARGET_ENTITY = {3: "NIK", 5: "NAMA", 9: "JENIS KELAMIN"}

def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Gagal decode bytes ke image.")

    _, width = img.shape[:2]
    cropped = img[:, :int(width * 0.7)]
    adjusted = cv2.convertScaleAbs(cropped, alpha=0.5, beta=50)
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    background = cv2.medianBlur(gray, 51)
    diff = cv2.absdiff(gray, background)
    _, binary = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return binary

def load_dictionary(path):
    with open(path, encoding='utf-8') as f:
        return [line.strip().upper() for line in f]

def correct_text(text, dictionary):
    result, _, _ = process.extractOne(text.upper(), dictionary, scorer=fuzz.ratio)
    return result

def correct_text_per_character(text, dictionary):
    return ''.join(correct_text(ch, dictionary) for ch in text)

def correct_text_per_word(text, dictionary):
    return ' '.join(correct_text(word, dictionary) for word in text.split())

def extract_entities(image, languages=['id', 'en'], allow_list=ALLOW_LIST, target_entity=TARGET_ENTITY):
    reader = easyocr.Reader(languages)
    results = reader.readtext(
        image,
        detail=1,
        paragraph=False,
        allowlist=allow_list
    )
    extracted = {
        target_entity[i]: text.strip()
        for i, (_, text, _) in enumerate(results)
        if i in target_entity
    }
    return extracted

def extract_info(image):
    image_preprocessed = preprocess_image(image)
    extracted_entities = extract_entities(image_preprocessed)

    dict_gender = load_dictionary(DICTIONARY_GENDER)
    dict_name = load_dictionary(DICTIONARY_NAME)
    dict_number = load_dictionary(DICTIONARY_NUMBER)

    nik_corrected = correct_text_per_character(extracted_entities['NIK'], dict_number)
    nama_corrected = correct_text_per_word(extracted_entities['NAMA'], dict_name)
    gender_corrected = correct_text(extracted_entities['JENIS KELAMIN'], dict_gender)

    return (nik_corrected, nama_corrected, gender_corrected)
