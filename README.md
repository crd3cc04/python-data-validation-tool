# 🐍 Python Data Validation Tool

A robust CSV validation engine built using test-driven development (TDD).

This project validates CSV files for common data-quailty issues such as missing fields, invalid ages, malformed emails, and more. The tool was built entirely through a structured TDD workflow using oytest, ensuring reliability, clarity, and maintainability.

---

## 🚀 Features

- Detects missing required values  
- Detects invalid data types  
- Validates numeric and non-negative fields  
- Generates a clean summary report  
- Works with any CSV file
- Flags invalid email formats
- Detects empty files
- Returns structured validation results
- Handles mixed valid/invalid rows  

---

## 📁 Project Structure

```
python-data-validation-tool/
│
├── src/
│   └── data_validator.py
│
├── sample_data/
│   └── users.csv
|
├── tests/
|   └── test_validator.py
|
├── conftest.py
│
└── README.md
```

---

## ▶️ How to Run

```bash
python3 src/data_validator.py
```

---

## 🧪 Sample Output

```
===== Data Validation Report =====
Row 3: Missing value in 'email'
Row 4: Invalid age 'not_a_number'
```

---

# 🧪 Running Tests

```bash
pytest -v
```

---

## 📌 Why This Project Matters

This script demonstrates:

- Python automation  
- Data quality checks  
- Error detection  
- Real‑world IT and data engineering workflows  

A strong addition to a professional GitHub portfolio.

---

## 🔧 Future Enhancements

- JSON validation  
- Schema definition support  
- Export results to CSV  
- Colorized terminal output  
- CLI arguments for file selection

# 🛠️ Common Errors Encountered & How They Were Resolved
*A technical log of issues discovered during development and how each was fixed.*

This project was built using a test-driven development (TDD) workflow. Each error below represents a real debugging moment that strengthened the final design.

---

🔹 1. ```ModuleNotFoundError: No module named 'src.validator'```

**Cause**

Tests attempted to import:
```python
from src.validator import validate_csv
```
But the actual file was named:
```code
data_validator.py
```
**Solution**

Updated the import:
```python
from src.data_validator import validate_csv
```

🔹 2. ```TypeError: 'NoneType' objecy is not subscriptable'```

**Cause**

```validate_csv()``` printed output but returned nothing, so Python returned ```None```.

**Solution**

Added a structured return:
```python
return {
    "vaild_rows": vaild,
    "invalid_rows": invalid,
    "errors": errors
}
```

**🔹 3. Missing Required Field Not Detected** 

**Cause**

the test accidentally used a vaild row.

**Solution**

Corrected the test data:
```code
,30,a@b.com,USA
```
The validator already handled missing fields correctly.

**🔹 4. Negative Age not Flagged as Invaild** 

**Cause**

```int(-5)``` is valid Python, so the validator accepted negative ages.

**Solution**

Added a negative-age check:
```python
age_value = int(row["age"])
if age_value < 0:
    row_errors.append(f"Invalid age '{row[age]}'")
```

**🔹 5. Invalid Email Format Not Detected**

**Cause**

Email validation logic didn't exist yet.

**Solution**

Added a simple format check:
```python
if "@" not in email_value:
    row_errorsappend(f"Invalid email '{email_value}'")
```

**🔹 6. Empty File Not Recognized**

**Cause**

An empty CSV produced zero rows and zero errors.

**Solution**

Added an early-exit check:
```python
content = file.read().strip()
if not content:
     return {
         "valid_rows": 0,
         "invalid_rows": 0,
         "errors": ["File is empty"]
}
```

