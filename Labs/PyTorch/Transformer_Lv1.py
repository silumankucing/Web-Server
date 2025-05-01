import torch
import torch.nn as nn
import torch.optim as optim

# Define the Transformer model
class SimpleTransformer(nn.Module):
    def __init__(self, input_dim, embed_dim, num_heads, ff_dim, num_layers, output_dim):
        super(SimpleTransformer, self).__init__()
        self.embedding = nn.Embedding(input_dim, embed_dim)
        self.positional_encoding = nn.Parameter(torch.zeros(1, 100, embed_dim))  # Max sequence length = 100
        self.transformer = nn.Transformer(
            d_model=embed_dim,
            nhead=num_heads,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            dim_feedforward=ff_dim,
            batch_first=True
        )
        self.fc = nn.Linear(embed_dim, output_dim)

    def forward(self, src, tgt):
        src = self.embedding(src) + self.positional_encoding[:, :src.size(1), :]
        tgt = self.embedding(tgt) + self.positional_encoding[:, :tgt.size(1), :]
        output = self.transformer(src, tgt)
        return self.fc(output)

# Hyperparameters
input_dim = 1000  # Vocabulary size
output_dim = 1000  # Vocabulary size
embed_dim = 64  # Embedding dimension
num_heads = 4  # Number of attention heads
ff_dim = 256  # Feedforward network dimension
num_layers = 2  # Number of encoder/decoder layers

# Model, loss function, and optimizer
model = SimpleTransformer(input_dim, embed_dim, num_heads, ff_dim, num_layers, output_dim)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Dummy data for training
src = torch.randint(0, input_dim, (32, 10))  # Batch size = 32, Sequence length = 10
tgt = torch.randint(0, output_dim, (32, 10))
tgt_input = tgt[:, :-1]  # Input to the decoder
tgt_output = tgt[:, 1:]  # Target output for loss calculation

# Training loop
epochs = 10
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    output = model(src, tgt_input)
    loss = loss_fn(output.view(-1, output_dim), tgt_output.view(-1))
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")

# Evaluation (dummy inference)
model.eval()
with torch.no_grad():
    src_test = torch.randint(0, input_dim, (1, 10))  # Single test sequence
    tgt_test = torch.randint(0, output_dim, (1, 9))  # Decoder input
    output = model(src_test, tgt_test)
    predicted = torch.argmax(output, dim=-1)
    print("Predicted sequence:", predicted)