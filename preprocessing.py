import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # URL 제거
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # 알파벳, 숫자, 공백, 쉼표, 온점만 남기고 모두 제거 (다른 구두점은 추가로 허용 가능)
    text = re.sub(r'[^a-z0-9\s,\.]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
