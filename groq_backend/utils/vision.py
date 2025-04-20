from PIL import Image
import torch
import clip

# Move model to correct device
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def describe_image(file):
    image = Image.open(file).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)  # Move image to device

    # Tokenize and move text to device
    text_inputs = torch.cat([
        clip.tokenize("a photo of a cat"),
        clip.tokenize("a scenic view"),
        clip.tokenize("a person talking"),
        clip.tokenize("a diagram"),
        clip.tokenize("an AI assistant"),
    ]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_inputs)
        similarity = (image_features @ text_features.T).squeeze(0)
        best_caption_idx = similarity.argmax().item()

    return ["cat", "scenic view", "person", "diagram", "AI assistant"][best_caption_idx]
