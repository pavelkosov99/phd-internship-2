import os
import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from src.dataset.dataset import CustomTestDataset
from src.model.model import CustomResNet
from src.dataset.test_remove_labels import check_and_remove_label_column
import json


def load_trained_model(model_path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = CustomResNet().to(device)
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


def generate_predictions(model, data_loader, output_file):
    predictions = {}
    image_count = 0
    with torch.no_grad():
        for inputs in data_loader:
            output = model(inputs)
            predictions[image_count] = bool(output > 0.5)
            image_count += 1

    with open(output_file, 'w') as file:
        json.dump(predictions, file, indent=4)
    print(f"Properties saved to {output_file}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_props = {
        "body_part": ["whole_body", "top_part", "bottom_part", "feet", "hands"],
        "weather_type": ["cold", "warm", "any"],
        "edge_shape": ["straight_edge", "curve_edge"]
    }

    csv_file = os.path.join(current_dir, '../../data/csv/test.csv')
    check_and_remove_label_column(csv_file)
    data_loader = load_data(csv_file)

    for prop, sub_props in data_props.items():
        for sub_prop in sub_props:
            model_path = os.path.join(current_dir, f"../../data/model/{prop}/{sub_prop}_model.pth")
            output_file = os.path.join(current_dir, f"../../data/json/{prop}/{sub_prop}_output.json")

            model = load_trained_model(model_path)
            generate_predictions(model, data_loader, output_file)


if __name__ == "__main__":
    main()
