from pathlib import Path

import pandas as pd
from sklearn.externals import joblib
from scipy.sparse import vstack, hstack

from ml_editor.data_processing import add_v1_features

FEATURE_ARR = [
    "action_verb_full",
    "question_mark_full",
    "text_len",
    "language_question",
]

model_path = Path("../models/model_1.pkl")
vectorizer_path = Path("../models/vectorizer_1.pkl")
VECTORIZER = joblib.load(vectorizer_path)
MODEL = joblib.load(model_path)


def get_model_probabilities_for_input_texts(text_array):
    global FEATURE_ARR, VECTORIZER, MODEL
    vectors = VECTORIZER.transform(text_array)
    text_ser = pd.DataFrame(text_array, columns=["full_text"])
    text_ser = add_v1_features(text_ser)
    vec_features = vstack(vectors)
    num_features = text_ser[FEATURE_ARR].astype(float)
    features = hstack([vec_features, num_features])
    return MODEL.predict_proba(features)