import csv

def validate_csv(file_path):
    errors = []
    row_number = 1

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row_number += 1

            # Check for missing fields
            for field, value in row.items():
                if value is None or value.strip() == "":
                    errors.append(f"Row {row_number}: Missing value in '{field}'")

            # Validate age field
            if "age" in row:
                try:
                    int(row["age"])
                except ValueError:
                    errors.append(f"Row {row_number}: Invalid age '{row['age']}'")

    print("\n===== Data Validation Report =====")
    if errors:
        for err in errors:
            print(err)
    else:
        print("No issues found. File is valid.")

if __name__ == "__main__":
    validate_csv("../sample_data/users.csv")
