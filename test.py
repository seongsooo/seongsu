from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                      model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli")

text = [
    "Seriously, adding your own custom music makes this the best workout game by far. On top of that, there are many options to customize and fine tune the type of workout you want for each song. Got this on sale, but the personal mp3 integration makes this more than worth the purchase at full price. Well done.",
    "I bought v1 two weeks ago and played with it for an hour or so every night. It had 9 free songs per difficulty level and brought in chords around levels 3 and 4. I quickly scored well on everything except the chords, which were just too awkward for my inexperienced hands. The AI really helped with learning the tricky songs by breaking them down into sections and slowly merging them back together with my mastery. The memorization feature is useful to learn the keys without seeing the floating 3D prompt. I never did try the sheet music aspect, but I'm not looking to learn how to read sheet music at this time. v2 dropped as a complete surprise. Next thing I knew the key mapping got even better, faster, and this improved mapping resulted in all my scores improving. The interface is more responsive and more options were available all over the place. Instead of 9 songs per level there are 20+ (didn't count but it's a noticeable increase). A new jazz song generator with tons of options, and a seemingly endless list of paid songs if you opted for a subscription. The lead dev is incredibly responsive if you have questions and actively looking to make this app the best. Definitely worth the purchase and once I learn the chords I will upgrade to the monthly subscription to play real songs!",
    "It is really good! But it is a shame that is not possible to do a workout with my wife or any friends, like fitxr!"
]

candidate_labels = [
    "customization and independent choice in the app experience",               # 자율성 (autonomy)
    "demonstrated skill and performance improvement in app use",                # 역량 (competence)
    "social experiences in app use",                                            # 관련성 (relatedness)
    "other"                                                                     # 기타
]

results = classifier(text, candidate_labels)

for idx, result in enumerate(results):
    print(f"Text {idx+1} classification results:")
    for label, score in zip(result['labels'], result['scores']):
        print(f"  {label}: {score:.4f}")
    print()
