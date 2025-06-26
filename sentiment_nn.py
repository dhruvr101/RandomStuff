import numpy as np
import re
from sklearn.model_selection import train_test_split

# Sample dataset
data = [
    ("I love this", 1),
    ("This was amazing", 1),
    ("I hate this", 0),
    ("What a waste", 0),
    ("Truly fun", 1),
    ("Not good", 0),
    ("Really bad", 0),
    ("So boring", 0),
    ("Absolutely loved", 1),
    ("Terrible movie", 0),
    ("Very enjoyable", 1),
    ("Not bad", 1),
    ("Could be better", 0),
    ("Really nice", 1),
    ("Awful experience", 0),
]

# Preprocessing: tokenize and lowercase
def tokenize(sentence):
    return re.findall(r"\b\w+\b", sentence.lower())

# Build vocabulary
vocab = sorted(set(word for sentence, _ in data for word in tokenize(sentence)))
word_to_index = {word: i for i, word in enumerate(vocab)}
vocab_size = len(vocab)

# Convert sentences to one-hot vectors
def vectorize(sentence):
    vec = np.zeros(vocab_size)
    for word in tokenize(sentence):
        if word in word_to_index:
            vec[word_to_index[word]] = 1
    return vec

# Prepare training data
X = np.array([vectorize(sentence) for sentence, _ in data])
y = np.array([[label] for _, label in data])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Neural net parameters
np.random.seed(0)
input_size = vocab_size
hidden_size = 8
output_size = 1

W1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
W2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

# Activation functions
def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x): return x * (1 - x)

# Training loop
lr = 0.1
epochs = 10000

for epoch in range(epochs):
    # Forward pass
    z1 = np.dot(X_train, W1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, W2) + b2
    a2 = sigmoid(z2)

    # Binary cross-entropy loss
    loss = -np.mean(y_train * np.log(a2 + 1e-8) + (1 - y_train) * np.log(1 - a2 + 1e-8))

    # Backpropagation
    dz2 = a2 - y_train
    dW2 = np.dot(a1.T, dz2)
    db2 = np.sum(dz2, axis=0, keepdims=True)

    dz1 = np.dot(dz2, W2.T) * sigmoid_derivative(a1)
    dW1 = np.dot(X_train.T, dz1)
    db1 = np.sum(dz1, axis=0, keepdims=True)

    # Update weights
    W2 -= lr * dW2
    b2 -= lr * db2
    W1 -= lr * dW1
    b1 -= lr * db1

    if epoch % 1000 == 0:
        print(f"Epoch {epoch} | Loss: {loss:.4f}")

# Predict function
def predict(X_input):
    a1 = sigmoid(np.dot(X_input, W1) + b1)
    a2 = sigmoid(np.dot(a1, W2) + b2)
    return (a2 > 0.5).astype(int)

# Evaluate accuracy
predictions = predict(X_test)
accuracy = np.mean(predictions == y_test)
print(f"\nTest Accuracy: {accuracy * 100:.2f}%")

# Try your own input
while True:
    user_input = input("\nEnter a sentence to predict sentiment (or 'exit'): ")
    if user_input.lower() == 'exit':
        break
    vec = vectorize(user_input)
    pred = predict(vec.reshape(1, -1))[0][0]
    sentiment = "Positive 😊" if pred == 1 else "Negative 😞"
    print(f"Predicted Sentiment: {sentiment}")
