import os
import json


def load_json(file_name):
    """Safely load JSON data from a file."""
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"An error occurred while loading/reading the file: {e}")
        return None


def write_json_file(file_path, data):
    """Safely write data to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def combine_json_files(base_dir, properties):
    """Combine JSON files for each sub-property into a single structure."""
    combined_data = {}

    for property_name, sub_properties in properties.items():
        for sub_index, sub_property in enumerate(sub_properties):
            file_path = os.path.join(base_dir, property_name, f"{sub_property}.json")
            data = load_json(file_path)

            if data is not None:
                for img_id, presence in data.items():
                    if img_id not in combined_data:
                        combined_data[img_id] = {prop: None for prop in properties.keys()}

                    if presence == 1:
                        combined_data[img_id][property_name] = sub_index

    return combined_data


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_dir, '../data/json')

    properties = {
        "body_part": ["whole_body", "top_part", "bottom_part", "feet", "hands"],
        "weather_type": ["cold", "warm", "any"],
        "edge_shape": ["straight_edge", "curve_edge"]
    }

    # Combine JSON files according to specified properties
    combined_data = combine_json_files(base_dir, properties)

    # Define the path for the output combined JSON file
    output_file_path = os.path.join(base_dir, 'combined_sub_models_output.json')

    # Write the combined data to a JSON file
    write_json_file(output_file_path, combined_data)

    print(f"Combined JSON data saved to {output_file_path}")


if __name__ == "__main__":
    main()
