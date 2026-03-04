import torch


def sentiment_classifier(model, tokenizer, input: list):
    inputs = tokenizer(input, return_tensors="pt", padding=True, Truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)
    
    return outputs

def parse_payload():
    # parse logic
    x = 1


def format_output(outputs, model):
    for output in outputs.logits:
        print(output)
        predicted_class_id = torch.argmax(output, dim=-1).item()
        predicted_label = model.config.id2label[predicted_class_id]
        print(f"Predicted label: {predicted_label} confidences: {torch.argmax(torch.softmax(output, dim=-1))}")