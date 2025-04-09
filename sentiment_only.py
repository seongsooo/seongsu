import pandas as pd
import torch
from tqdm import tqdm
from sentiment_analysis import init_sentiment_classifier, get_sentiment

def main():
    # 기존 파일 불러오기
    df = pd.read_excel("SDT_vr_review.xlsx")
    texts = df["clean_content"].tolist()
    
    # 감성 분석 모델 초기화
    device = 0 if torch.cuda.is_available() else -1
    sentiment_classifier = init_sentiment_classifier(device=device)
    
    # 각 리뷰에 대해 감성 분석 실행
    sentiment = []
    sentiment_scores = []
    for text in tqdm(texts, desc="Processing Sentiment"):
        result = get_sentiment(text, sentiment_classifier)
        sentiment.append(result["label"])
        sentiment_scores.append(result["score"])
    
    # 결과를 새로운 컬럼으로 추가
    df["sentiment"] = sentiment
    df["sentiment_score"] = sentiment_scores
    
    # 파일로 저장
    df.to_excel("SDT_vr_review_sentiment.xlsx", index=False)

if __name__ == "__main__":
    main()
