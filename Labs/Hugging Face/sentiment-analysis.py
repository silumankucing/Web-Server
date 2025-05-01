from transformers import pipeline

# Load a pre-trained text classification pipeline
classifier = pipeline("sentiment-analysis")

# Example text inputs
texts = [
    "I love using Hugging Face Transformers!",
    "This is the worst experience I've ever had."
]

# Perform sentiment analysis
results = classifier(texts)

# Display the results
for text, result in zip(texts, results):
    print(f"Text: {text}")
    print(f"Label: {result['label']}, Confidence: {result['score']:.4f}")