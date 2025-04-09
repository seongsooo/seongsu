from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def init_sentiment_classifier(device=-1):
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)
    return sentiment_pipeline

def get_sentiment(text, sentiment_classifier):
    if not text or len(text) < 3:
        return {"label": "Neutral", "score": 0.0}
    
    # top_k=1 옵션으로 가장 높은 확률의 감성 라벨만 반환
    result = sentiment_classifier(text, truncation=True, max_length=512, top_k=1)
    mapping = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
    selected_label = mapping.get(result[0]["label"], result[0]["label"])
    return {"label": selected_label, "score": result[0]["score"]}
