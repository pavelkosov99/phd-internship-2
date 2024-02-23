import os
import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from src.dataset.test_remove_labels import check_and_remove_label_column
from src.dataset.dataset import CustomTestDataset
from src.model.model import CustomMultiClassResNet
import json


def load_trained_model(model_path, n_classes):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = CustomMultiClassResNet(n_classes).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model


def load_data(csv_file):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    dataset = CustomTestDataset(csv_file=csv_file, transform=transform)
    data_loader = DataLoader(dataset, batch_size=1, shuffle=False)
    return data_loader


def generate_predictions(models, data_loader, output_file):
    predictions = {}

    with torch.no_grad():
        for i, inputs in enumerate(data_loader):
            # Ensure there's a dictionary for this image index
            if i not in predictions:
                predictions[i] = {}

            for model_name, model in models.items():
                device = next(model.parameters()).device  # Ensure inputs are on the same device as the model
                inputs = inputs.to(device)
                outputs = model(inputs)

                # Assuming each model outputs logits for classes
                # get the predicted class index
                _, predicted = torch.max(outputs, 1)

                # Store the prediction using the model's name as the key
                predictions[i][model_name] = predicted.item()

    with open(output_file, 'w') as f:
        json.dump(predictions, f, indent=4)

    print(f"Predictions saved to {output_file}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, '../../data/csv/test.csv')
    check_and_remove_label_column(csv_file)

    model_names = ["body_part", "weather_type", "edge_shape"]
    classes_mapping = {
        "body_part": 5,
        "weather_type": 3,
        "edge_shape": 2,
    }

    test_loader = load_data(csv_file)

    models = {}

    for model_name in model_names:
        n_classes = classes_mapping[model_name]

        model_path = os.path.join(current_dir, f"../../data/model/{model_name}_model.pth")
        models[model_name] = load_trained_model(model_path, n_classes)

    output = os.path.join(current_dir, '../../data/json/prop_output.json')
    generate_predictions(models, test_loader, output)


if __name__ == "__main__":
    main()
