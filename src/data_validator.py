import csv

def validate_csv(file_path):
    errors = []
    row_number = 1
    valid = 0
    invalid = 0

    with open(file_path, "r") as file:
        content = file.read().strip()
        if not content:
            return {
                "valid_rows": 0,
                "invalid_rows": 0,
                "errors": ["File is empty"]
            }
        file.seek(0)  # Reset file pointer to the beginning after reading

        reader = csv.DictReader(file)

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row_number += 1
            row_errors = []

            # Check for missing fields
            for field, value in row.items():
                if value is None or value.strip() == "":
                    row_errors.append(f"Missing value in '{field}'")

            # Validate age field
            if "age" in row:
                try:
                    age_value = int(row["age"])
                    if age_value < 0:
                        row_errors.append(f"Invalid age '{row['age']}'")
                except ValueError:
                    row_errors.append(f"Invalid age '{row['age']}'")

            # Validate email field
            if "email" in row:
                email_value = row["email"]
                if email_value and "@" not in email_value:
                    row_errors.append(f"Invalid email '{email_value}'")        

            # Count valid/invalid rows
            if row_errors:
                invalid += 1
                errors.append(f"Row {row_number}: " + "; ".join(row_errors))
            else:
                valid += 1        

    print("\n===== Data Validation Report =====")
    if errors:
        for err in errors:
            print(err)
    else:
        print("No issues found. File is valid.")

    return {
        "valid_rows": valid,
        "invalid_rows": invalid,
        "errors": errors
    }    

if __name__ == "__main__":
    validate_csv("../sample_data/users.csv")
