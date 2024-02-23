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
    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(current_dir,'../../data/csv/train.csv')

    bodypart_file_path = os.path.join(current_dir,'../../data/csv/props/body_part.csv')
    bodypart_mappings = {0: 1,
                         1: 2,
                         2: 1,
                         3: 0,
                         4: 3,
                         5: 1,
                         6: 1,
                         7: 3,
                         8: 4,
                         9: 3}
    modify_labels(file_path, bodypart_file_path, bodypart_mappings)

    weathertype_file_path = os.path.join(current_dir,'../../data/csv/props/weather_type.csv')
    weathertype_mappings = {0: 1,
                            1: 2,
                            2: 0,
                            3: 2,
                            4: 1,
                            5: 0,
                            6: 2,
                            7: 2,
                            8: 2,
                            9: 0}
    modify_labels(file_path, weathertype_file_path, weathertype_mappings)

    edgeshape_file_path = os.path.join(current_dir,'../../data/csv/props/edge_shape.csv')
    edgeshape_mappings = {0: 1,
                          1: 0,
                          2: 1,
                          3: 0,
                          4: 1,
                          5: 1,
                          6: 1,
                          7: 1,
                          8: 0,
                          9: 0}
    modify_labels(file_path, edgeshape_file_path, edgeshape_mappings)


if __name__ == '__main__':
    main()
