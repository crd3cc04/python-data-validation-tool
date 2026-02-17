'''
This test defines the baseline contract for the validator tool:
- It must accept a file path
- It must read a CSV
- It must validate each row
- It must return a dictionary with: "vaild_rows" and "invalid_rows"

'''
import os
import sys

print("CWD:", os.getcwd())
print("PATH:", sys.path)

from src.data_validator import validate_csv # pyright: ignore[reportMissingImports]

# This test is to confirm that valid rows are counted correctly
def test_validate_valid_rows(tmp_path):
    # Create a temporary CSV file
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,email,country\n"
        "Alice,30,a@b.com,USA\n"
        "Bob,25,b@c.com,Canada\n"
    )

    result = validate_csv(str(csv_file))

    assert result["valid_rows"] == 2
    assert result["invalid_rows"] == 0

# This test is to catch rows with missing required fields
def test_missing_required_field(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,email,country\n"
        ",30,a@b.com,USA\n"
    )

    result = validate_csv(str(csv_file))

    assert result["valid_rows"] == 0
    assert result["invalid_rows"] == 1
    assert len(result["errors"]) == 1
    assert "Missing value in 'name'" in result["errors"][0]

# This test is to catch rows with non-integer age values
def test_invalid_age_non_numeric(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,email,country\n"
        "Alice,thirty,a@b.com,USA\n"
    )

    result = validate_csv(str(csv_file))

    assert result["valid_rows"] == 0
    assert result["invalid_rows"] == 1
    assert len(result["errors"]) == 1
    assert "Invalid age 'thirty'" in result["errors"][0]

# This test is to treat negative age values as invalid
def test_negative_age(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,email,country\n"
        "Alice,-5,a@b.com,USA\n"
    )

    result = validate_csv(str(csv_file))

    assert result["valid_rows"] == 0
    assert result["invalid_rows"] == 1
    assert len(result["errors"]) == 1
    assert "Invalid age '-5'" in result["errors"][0]

# This test catches emails that are missing the "@" symbol
def test_invalid_email_format(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,email,country\n"
        "Alice,30,aliceexample.com,USA\n"
    )

    result = validate_csv(str(csv_file))

    assert result["valid_rows"] == 0
    assert result["invalid_rows"] == 1
    assert len(result["errors"]) == 1
    assert "Invalid email 'aliceexample.com'" in result["errors"][0]

# This test can handle a realistic mix of valid and invalid rows
def test_mixed_valid_and_invalid_rows(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,email,country\n" 
        "Alice,30,a@b.com,USA\n"        # Valid
        ",25,b@c.com,Canada\n"          # missing name
        "Charlie,-5,c@d.com,UK\n"       # invalid age
        "David,,dexample.com,France\n"  # invalid email
    )

    result = validate_csv(str(csv_file))

    assert result["valid_rows"] == 1
    assert result["invalid_rows"] == 3
    assert len(result["errors"]) == 3

    # Check specific error messages
    assert "Missing value in 'name'" in result["errors"][0]
    assert "Invalid age '-5'" in result["errors"][1]
    assert "Invalid email 'dexample.com'" in result["errors"][2]

# This test handles an empty CSV file instead of crashing or miscounting
def test_empty_file(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("")  

    result = validate_csv(str(csv_file))

    assert result["valid_rows"] == 0
    assert result["invalid_rows"] == 0
    assert len(result["errors"]) == 1
    assert "File is empty" in result["errors"][0]