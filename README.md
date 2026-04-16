# Company Employee Dashboard

This repository contains a Streamlit dashboard for managing company employee data.

## Run locally

```bash
cd "c:\Users\rajas\OneDrive\Documents\document\prompt2026"
.c:/Users/rajas/OneDrive/Documents/document/prompt2026/.venv/Scripts/python.exe -m streamlit run dashboard.py
```

## Login credentials

- Admin: `admin` / `admin123`
- Employee: `employee` / `emp123`
- Employer: `employer` / `emp123`

## Deploy to Streamlit Cloud

1. Push the repository to GitHub.
2. Go to https://share.streamlit.io and sign in.
3. Connect your GitHub account.
4. Select this repository and set `dashboard.py` as the main file.
5. Deploy.

## Notes

- The app uses `company_db.json` for TinyDB persistence.
- For production, use a real cloud database and secure authentication.
