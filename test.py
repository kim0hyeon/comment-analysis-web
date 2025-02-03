import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# 1. 테스트 데이터 로드 및 전처리
test_data_path = "data/ratings_test.txt"
test_data = pd.read_csv(test_data_path, sep='\t').dropna().drop_duplicates(subset='document')

# 결측값 제거
test_data = test_data.dropna()

# 중복된 리뷰 제거
test_data = test_data.drop_duplicates(subset='document')

# 데이터 분리
X_test = test_data['document'].values
y_test = test_data['label'].values

# 토크나이저 로드
with open("models/tokenizer.pkl", "rb") as file:
    tokenizer = pickle.load(file)

# 텍스트 데이터를 시퀀스로 변환 및 패딩
X_test_seq = tokenizer.texts_to_sequences(X_test)
X_test_padded = pad_sequences(X_test_seq, maxlen=100)

# 2. 모델 로드
model = load_model("models/sentiment_model.h5")

# 3. 테스트 데이터로 평가
test_loss, test_accuracy = model.evaluate(X_test_padded, y_test)
print(f"테스트 데이터 손실: {test_loss:.4f}, 정확도: {test_accuracy:.4f}")