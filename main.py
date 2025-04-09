import pandas as pd
import torch
from tqdm import tqdm
from preprocessing import clean_text
from sdt_classifier import init_sdt_classifier, batch_process_sdt, classify_sdt
from sentiment_analysis import init_sentiment_classifier, get_sentiment

def batch_process_sentiment(texts, sentiment_classifier):
    sentiments = []
    for text in tqdm(texts, desc="Processing Sentiment"):
        sentiment = get_sentiment(text, sentiment_classifier)
        sentiments.append(sentiment)
    return sentiments

def main():
    # 데이터 로드 및 전처리
    df = pd.read_excel('./mobile/mobile_review.xlsx')
    df['clean_content'] = df['review'].apply(clean_text)
    
    # 리뷰 길이 필터링
    df = df[df['clean_content'].str.len() >= 10].reset_index(drop=True)
    texts = df['clean_content'].tolist()
    
    # 모델 초기화
    device_id = 0 if torch.cuda.is_available() else -1
    sdt_pipeline = init_sdt_classifier(device=device_id)
    sentiment_classifier = init_sentiment_classifier(device=device_id)
    
    # 후보 라벨 정의
    candidate_labels = [
        "customization and independent choice in the app experience",               # 자율성 (autonomy)
        "demonstrated skill and performance improvement in app use",                # 유능감 (competence)
        "social experiences in app use",                                            # 관련성 (relatedness)
        "other"                                                                     # 기타
    ]

    # SDT 분류
    sdt_results = []
    for text in tqdm(texts, desc="Processing SDT"):
        res = classify_sdt(text, sdt_pipeline, candidate_labels)
        sdt_results.append(res)
    sdt_df = pd.DataFrame(sdt_results)
    
    # 감성 분석
    sentiment_results = batch_process_sentiment(texts, sentiment_classifier)
    df['sentiment'] = sentiment_results
    
    # SDT 분류 결과 병합 후 저장
    df = pd.concat([df, sdt_df], axis=1)
    df.to_excel('SDT_mobile_review.xlsx', index=False)

if __name__ == "__main__":
    main()
