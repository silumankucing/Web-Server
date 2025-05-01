import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split

# Sample dataset: Texts and their corresponding labels
texts = ["I love programming", "Python is amazing", "I hate bugs", "Debugging is fun", "I dislike errors"]
labels = [1, 1, 0, 1, 0]  # 1 = Positive, 0 = Negative

# Vocabulary creation
vocab = set(word for text in texts for word in text.lower().split())
word_to_idx = {word: idx for idx, word in enumerate(vocab)}

# Text encoding: Convert texts to bag-of-words vectors
def encode_text(text):
    vector = torch.zeros(len(vocab))
    for word in text.lower().split():
        if word in word_to_idx:
            vector[word_to_idx[word]] += 1
    return vector

encoded_texts = torch.stack([encode_text(text) for text in texts])
labels = torch.tensor(labels, dtype=torch.float32)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(encoded_texts, labels, test_size=0.2, random_state=42)

# Define a simple feedforward neural network
class TextClassifier(nn.Module):
    def __init__(self, input_size):
        super(TextClassifier, self).__init__()
        self.fc = nn.Linear(input_size, 1)  # Output size is 1 for binary classification
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        return self.sigmoid(self.fc(x))

# Model, loss function, and optimizer
model = TextClassifier(input_size=len(vocab))
loss_fn = nn.BCELoss()  # Binary Cross-Entropy Loss
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training loop
epochs = 100
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    predictions = model(X_train).squeeze()
    loss = loss_fn(predictions, y_train)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")

# Evaluation
model.eval()
with torch.no_grad():
    test_predictions = model(X_test).squeeze()
    test_predictions = (test_predictions >= 0.5).float()  # Convert probabilities to binary predictions
    accuracy = (test_predictions == y_test).float().mean()
    print(f"Test Accuracy: {accuracy:.4f}")