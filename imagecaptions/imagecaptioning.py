import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

# Download a pre-trained ResNet model
resnet = models.resnet50(pretrained=True)
modules = list(resnet.children())[:-1]
resnet = nn.Sequential(*modules)
resnet.eval()

# Define a simple captioning model
class CaptioningModel(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers):
        super(CaptioningModel, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)

    def forward(self, features, captions):
        captions = captions[:, :-1]
        embeds = self.embed(captions)
        inputs = torch.cat((features.unsqueeze(1), embeds), 1)
        lstm_out, _ = self.lstm(inputs)
        outputs = self.linear(lstm_out)
        return outputs

# Load your vocabulary
vocab_size = len(your_vocab)
embed_size = 256
hidden_size = 512
num_layers = 1

# Initialize your model
model = CaptioningModel(embed_size, hidden_size, vocab_size, num_layers)

# Load your trained model weights (if available)
model.load_state_dict(torch.load('your_model_weights.pth'))
model.eval()

# Define a function to preprocess images
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)
    return image

# Define a function to generate captions
def generate_caption(image_path, max_length=20):
    image = preprocess_image(image_path)
    image_features = resnet(image).squeeze(0)
    image_features = image_features.unsqueeze(0)
    caption = []

    for _ in range(max_length):
        with torch.no_grad():
            inputs = torch.LongTensor(caption).unsqueeze(0)
            outputs = model(image_features, inputs)
            predicted = outputs.argmax(2)[:, -1].item()
            caption.append(predicted)
            if predicted == your_end_token_id:
                break

    return ' '.join([your_vocab[idx] for idx in caption])

# Example usage
image_path = 'your_image.jpg'
caption = generate_caption(image_path)
print("Generated Caption:", caption)
