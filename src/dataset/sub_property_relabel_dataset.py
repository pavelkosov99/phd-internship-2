import os

import pandas as pd


def modify_labels(file_path, modified_file_path, mappings):
    try:
        data = pd.read_csv(file_path)
        if 'label' not in data.columns:
            raise ValueError("Column 'label' not found in the file")

        data['label'] = data['label'].replace(mappings)

        data.to_csv(modified_file_path, index=False)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Base directory for data files
    data_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/csv'))

    # Configurations for each label modification
    modifications = [
        ('sub_props/body_part/whole_body.csv', {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}),
        ('sub_props/body_part/top_part.csv', {0: 1, 1: 0, 2: 1, 3: 0, 4: 0, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0}),
        ('sub_props/body_part/bottom_part.csv', {0: 0, 1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}),
        ('sub_props/body_part/feet.csv', {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1, 8: 0, 9: 1}),
        ('sub_props/body_part/hands.csv', {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1, 9: 0}),

        ('sub_props/weather_type/cold.csv', {0: 0, 1: 0, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 0, 8: 0, 9: 1}),
        ('sub_props/weather_type/warm.csv', {0: 1, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}),
        ('sub_props/weather_type/any.csv', {0: 0, 1: 1, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 0}),

        ('sub_props/edge_shape/straight_edge.csv', {0: 0, 1: 1, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0, 8: 1, 9: 1}),
        ('sub_props/edge_shape/curve_edge.csv', {0: 1, 1: 0, 2: 1, 3: 1, 4: 0, 5: 1, 6: 1, 7: 1, 8: 0, 9: 0})
    ]

    # Main train.csv file path
    file_path = os.path.join(data_base_dir, 'train.csv')

    # Loop over each modification configuration
    for sub_path, mappings in modifications:
        modify_labels(file_path, os.path.join(data_base_dir, sub_path), mappings)


if __name__ == '__main__':
    main()
