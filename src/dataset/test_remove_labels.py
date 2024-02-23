import csv
import os


def check_and_remove_label_column(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Read the first row which contains headers

        if headers:  # If headers are present
            if 'label' in headers:  # If the 'label' column is present
                print("CSV file has a 'label' column. Removing it...")
                label_index = headers.index('label')  # Get the index of the 'label' column
                data = [row for row in reader]  # Read the rest of the data

                # Remove the 'label' column from both headers and data
                headers.pop(label_index)
                for row in data:
                    row.pop(label_index)

                # Write the modified data back to the CSV file
                with open(csv_file, 'w', newline='') as output_file:
                    writer = csv.writer(output_file)
                    writer.writerow(headers)
                    writer.writerows(data)
                print("Modified data saved to the same file.")
            else:
                print("CSV file does not have a 'label' column. No changes made.")
        else:
            print("CSV file does not have labels. No changes made.")


# def main():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#
#     input_csv_file = os.path.join(current_dir, '../../data/csv/test.csv')
#
#     check_and_remove_label_column(input_csv_file)
#
#
# if __name__ == "__main__":
#     main()