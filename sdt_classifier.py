from transformers import pipeline

def init_sdt_classifier(device=-1):
    classifier = pipeline(
        "zero-shot-classification", 
        model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
        device=device,
        multi_label=False
    )
    return classifier

def classify_sdt(text, sdt_pipeline, candidate_labels):
    result = sdt_pipeline(text, candidate_labels)
    return {
        "SDT_label": result["labels"][0],
        "score": result["scores"][0]
    }

def batch_process_sdt(texts, sdt_pipeline, candidate_labels):
    results = []
    for text in texts:
        res = classify_sdt(text, sdt_pipeline, candidate_labels)
        results.append(res)
    return results
