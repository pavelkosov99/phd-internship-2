import os

import torch
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split

from src.model.model import CustomResNet
from src.dataset.dataset import CustomDataset


def load_data(csv_file, validation_split=0.1):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    dataset = CustomDataset(csv_file=csv_file, transform=transform)
    dataset_size = len(dataset)
    val_size = int(dataset_size * validation_split)
    train_size = dataset_size - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
    return train_loader, val_loader


def custom_loss(outputs, labels):
    loss_fn = torch.nn.BCELoss()

    # Adjust labels to have the same size as outputs
    labels = labels.float().unsqueeze(1)
    return loss_fn(outputs, labels)


def train_model(model, train_loader, val_loader, optimizer, epochs, model_save_path, patience, training_type):
    early_stopping_counter = 0
    best_val_loss = float('inf')
    device = next(model.parameters()).device

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = custom_loss(outputs, labels.float())
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_train_loss = total_loss / len(train_loader)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = custom_loss(outputs, labels.float())
                val_loss += loss.item()
        avg_val_loss = val_loss / len(val_loader)

        print(
            f"{training_type} Training - Epoch [{epoch + 1}/{epochs}], Training Loss: {avg_train_loss}, Validation "
            f"Loss: {avg_val_loss}"
        )

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            early_stopping_counter = 0
            torch.save(model.state_dict(), model_save_path)
        else:
            early_stopping_counter += 1
            if early_stopping_counter >= patience:
                print(f"Early stopping triggered after {patience} epochs with no improvement")
                break


def main():
    epochs = 50
    patience = 10

    current_dir = os.path.dirname(os.path.abspath(__file__))
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Data and model setup
    data_props = {
        "body_part": ["whole_body", "top_part", "bottom_part", "feet", "hands"],
        "weather_type": ["cold", "warm", "any"],
        "edge_shape": ["straight_edge", "curve_edge"]
    }

    models = {}
    optimizers = {}

    for prop, sub_props in data_props.items():
        for sub_prop in sub_props:
            csv_file = os.path.join(current_dir, f"../../data/csv/sub_props/{prop}/{sub_prop}.csv")
            train_loader, val_loader = load_data(csv_file)

            model_save_path = os.path.join(current_dir, f"../../data/model/{prop}/{sub_prop}_model.pth")

            models[sub_prop] = CustomResNet().to(device)
            optimizers[sub_prop] = optim.Adam(models[sub_prop].parameters(), lr=0.001)

            train_model(models[sub_prop], train_loader, val_loader, optimizers[sub_prop], epochs, model_save_path,
                        patience, sub_prop)


if __name__ == "__main__":
    main()
