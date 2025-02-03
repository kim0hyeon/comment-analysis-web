import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
import pickle

# 1. 데이터 로드 및 전처리
# 데이터 파일 경로 설정
data_path = "data/ratings_train.txt"

# 데이터 로드
data = pd.read_csv(data_path, sep='\t')

# 결측값 제거
data = data.dropna()

# 중복된 리뷰 제거
data = data.drop_duplicates(subset='document')

# 데이터 분리
X = data['document'].values
y = data['label'].values

# 훈련/검증 데이터 분리
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 토큰화 및 패딩
# 토큰화 객체 생성
tokenizer = Tokenizer(num_words=20000)
tokenizer.fit_on_texts(X_train)

# 텍스트 데이터를 시퀀스로 변환
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_val_seq = tokenizer.texts_to_sequences(X_val)

# 시퀀스를 동일한 길이로 패딩
X_train_padded = pad_sequences(X_train_seq, maxlen=100)
X_val_padded = pad_sequences(X_val_seq, maxlen=100)

# 3. 모델 정의 및 학습
model = Sequential([
    Embedding(input_dim=20000, output_dim=128, input_length=100),
    LSTM(64, return_sequences=False),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

# 모델 컴파일
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 모델 학습
model.fit(X_train_padded, y_train, epochs=5, batch_size=64, validation_data=(X_val_padded, y_val))

# 4. 모델 저장
# 모델 파일과 토크나이저 파일 저장
model.save("models/sentiment_model.h5")
with open("models/tokenizer.pkl", "wb") as file:
    pickle.dump(tokenizer, file)

print("모델과 토크나이저가 성공적으로 저장되었습니다.")
