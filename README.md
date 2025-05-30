# 🧾 Sales Tracker App (Kivy + Google Sheets)

This is a GUI-based Sales Tracker application built with **Python**, **Kivy**, and **Google Sheets API**. It allows small businesses or individual vendors to manage daily product sales, calculate totals, and automatically log records into Google Sheets.

---

## ✨ Features

- ✅ Modern Kivy-based graphical interface
- ✅ Google Sheets integration using `gspread`
- ✅ Product and quantity selection via buttons
- ✅ Real-time order total and full-day sales summary
- ✅ Cloud logging of each transaction
- ✅ "Open Report" button to view local summary file

---

## 📦 Requirements

- Python 3.x
- Kivy
- gspread
- google-auth

Install required packages:

```bash
pip install kivy gspread google-auth
```

---

## ⚙️ Setup Instructions

### 📁 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sales-tracker-app.git
cd sales-tracker-app
```

---

### 🔐 2. Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project
3. Enable the **Google Sheets API** and **Google Drive API**
4. Create **Service Account Credentials** and download the JSON file
5. Rename the file to:

```
daily-sales-455107-35b447e52c4c.json
```

6. Move this file into your project directory (same folder as your script)

> ⚠️ **Important**: Share your Google Sheet with the `client_email` from the JSON file.

---

### 📄 3. Prepare Google Sheet

1. Create a new Google Sheet
2. Copy the **Sheet ID** from the URL  
   Example:
   ```
   https://docs.google.com/spreadsheets/d/THIS_IS_YOUR_SHEET_ID/edit#gid=0
   ```
3. Replace the following line in your script with your actual sheet ID:

```python
SHEET_ID = "YOUR_SHEET_ID"
```

---

### ▶️ 4. Run the Application

In the project directory, run the Python file:

```bash
python your_script_name.py
```

(Replace `your_script_name.py` with your actual file name, e.g., `main.py`)

---

## 🖼️ Screenshot

*(Optional: Save a screenshot as `assets/screenshot.png` and display it here)*

```markdown
![Sales Tracker Screenshot](assets/screenshot.png)
```

---

## 🛠️ Project Structure

```plaintext
sales-tracker-app/
├── your_script_name.py
├── daily-sales-455107-35b447e52c4c.json  # <- keep this secret
├── README.md
├── LICENSE
├── .gitignore
├── assets/
│   └── screenshot.png
└── .github/
    └── workflows/
        └── python-app.yml  # (optional CI config)
```

---

## 📄 License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for more details.

---

## 🧪 Optional: GitHub Actions (CI)

To run basic Python checks on every push, add this file:

**.github/workflows/python-app.yml**
```yaml
name: Python App CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          pip install kivy gspread google-auth
      - name: Check for syntax errors
        run: python -m py_compile your_script_name.py
```

---

## 🙋 Need Help?

If you run into issues, double-check:
- Your credentials JSON file name and location
- That your Google Sheet is shared with the service account
- Sheet ID is correct
- Required libraries are installed

---

Made with ❤️ using Python and Kivy
