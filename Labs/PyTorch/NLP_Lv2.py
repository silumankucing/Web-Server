import torch
import torch.nn as nn
import torch.optim as optim
from torchtext.vocab import GloVe
from torchtext.data.utils import get_tokenizer
from sklearn.model_selection import train_test_split

# Sample dataset: Texts and their corresponding labels
texts = ["I love programming", "Python is amazing", "I hate bugs", "Debugging is fun", "I dislike errors"]
labels = [1, 1, 0, 1, 0]  # 1 = Positive, 0 = Negative

# Tokenization
tokenizer = get_tokenizer("basic_english")
tokenized_texts = [tokenizer(text) for text in texts]

# Load pre-trained GloVe embeddings
glove = GloVe(name="6B", dim=50)  # 50-dimensional GloVe embeddings

# Convert tokens to embeddings
def encode_text(tokens):
    embeddings = [glove[token] for token in tokens if token in glove.stoi]
    if len(embeddings) == 0:
        return torch.zeros(50)  # Handle empty tokens
    return torch.mean(torch.stack(embeddings), dim=0)

encoded_texts = torch.stack([encode_text(tokens) for tokens in tokenized_texts])
labels = torch.tensor(labels, dtype=torch.float32)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(encoded_texts, labels, test_size=0.2, random_state=42)

# Define an LSTM-based sequence model
class LSTMClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMClassifier, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.unsqueeze(1)  # Add sequence dimension
        _, (hidden, _) = self.lstm(x)
        output = self.sigmoid(self.fc(hidden[-1]))
        return output

# Model, loss function, and optimizer
model = LSTMClassifier(input_size=50, hidden_size=128, output_size=1)
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