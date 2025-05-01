import torch
import torch.nn as nn
import torch.optim as optim

# Sample user-item interaction matrix (ratings)
# Rows: Users, Columns: Items
ratings = torch.tensor([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
    [0, 3, 4, 0]
], dtype=torch.float32)

# Mask for known ratings (non-zero entries)
mask = ratings > 0

# Define the matrix factorization model
class MatrixFactorization(nn.Module):
    def __init__(self, num_users, num_items, num_factors):
        super(MatrixFactorization, self).__init__()
        self.user_factors = nn.Embedding(num_users, num_factors)  # User latent factors
        self.item_factors = nn.Embedding(num_items, num_factors)  # Item latent factors

    def forward(self, user, item):
        # Dot product of user and item latent factors
        return (self.user_factors(user) * self.item_factors(item)).sum(1)

# Number of users, items, and latent factors
num_users, num_items = ratings.shape
num_factors = 3

# Model, loss function, and optimizer
model = MatrixFactorization(num_users, num_items, num_factors)
loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training data
user_ids, item_ids = mask.nonzero(as_tuple=True)
target_ratings = ratings[mask]

# Training loop
epochs = 500
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    predictions = model(user_ids, item_ids)
    loss = loss_fn(predictions, target_ratings)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")

# Predict the full user-item matrix
with torch.no_grad():
    full_user_ids = torch.arange(num_users).repeat_interleave(num_items)
    full_item_ids = torch.arange(num_items).repeat(num_users)
    predicted_ratings = model(full_user_ids, full_item_ids).reshape(num_users, num_items)

print("\nOriginal Ratings:")
print(ratings)
print("\nPredicted Ratings:")
print(predicted_ratings)