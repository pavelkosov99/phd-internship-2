import json
import os


def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"An error occurred while loading/reading the file: {e}")


def combine_json_files(file1_content, file2_content):
    clothes_mapping = {
        0: "TshirtTop",
        1: "Trouser",
        2: "Pullover",
        3: "Dress",
        4: "Coat",
        5: "Sandal",
        6: "Shirt",
        7: "Sneaker",
        8: "Bag",
        9: "AnkleBoot"
    }

    body_part_mapping = {
        0: "WholeBody",
        1: "TopPart",
        2: "BottomPart",
        3: "Feet",
        4: "Hands"
    }

    weather_type_mapping = {
        0: "Cold",
        1: "Warm",
        2: "Any"
    }

    edge_shape_mapping = {
        0: "StraightEdge",
        1: "CurveEdge"
    }

    combined_json = {}

    for key in file1_content:
        image_number = f"Image_{key}"
        combined_json[image_number] = {
            "Clothes": clothes_mapping.get(file1_content[key], "Unknown"),
            "Properties": {
                "BodyPart": body_part_mapping.get(file2_content.get(key, {}).get("body_part", 0), "Unknown"),
                "WeatherType": weather_type_mapping.get(file2_content.get(key, {}).get("weather_type", 0), "Unknown"),
                "EdgeShape": edge_shape_mapping.get(file2_content.get(key, {}).get("edge_shape", 0), "Unknown")
            }
        }
    return combined_json


def write_json_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.path.join(current_dir, '../data/json')

    # Paths to the input JSON files and the output file
    file1_path = os.path.join(current_dir, 'global_output.json')
    file2_path = os.path.join(current_dir, 'prop_output.json')
    output_file_path = os.path.join(current_dir, 'compound_output.json')

    # Loading the input files
    file1_content = load_json(file1_path)
    file2_content = load_json(file2_path)

    # Combining the contents
    combined_content = combine_json_files(file1_content, file2_content)

    # Writing the combined content to a new file
    write_json_file(output_file_path, combined_content)

    print(f"Combined JSON file has been saved to: {output_file_path}")


if __name__ == "__main__":
    main()
