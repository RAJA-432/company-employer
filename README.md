# 🚀 Neural Network Dashboard

A futuristic sci-fi themed employee management system built with Streamlit and TinyDB.

## Features

- 🔐 **Neural Access Control**: Secure login with 10-digit employee ID codes
- 🖥️ **Admin Control Matrix**: Comprehensive admin panel with system monitoring
- 📊 **Performance Analytics**: Real-time neural performance analysis
- 👥 **Multi-Role System**: Employee, Employer, HR, and Admin access levels
- 🎨 **Sci-Fi UI Theme**: Immersive dark theme with neon accents

## Run locally

```bash
cd "c:\Users\rajas\OneDrive\Documents\document\prompt2026"
.c:/Users/rajas/OneDrive/Documents/document/prompt2026/.venv/Scripts/python.exe -m streamlit run dashboard.py
```

## Login credentials

Use 10-digit employee IDs as usernames:


- **Alice Johnson (Employee)**: `raj4320001` / `alice123`
- **Bob Smith (Employer)**: `raj4320002` / `bob123`
- **Carol Williams (HR)**: `raj4320003` / `carol123`
- **David Brown (Employer)**: `raj4320004` / `david123`
- **Eve Davis (Employee)**: `raj4320005` / `eve123`

New employees will be assigned sequential IDs like `raj4320006`, `raj4320007`, etc.

## Deploy to Streamlit Cloud

1. Push the repository to GitHub.
2. Go to https://share.streamlit.io and sign in.
3. Connect your GitHub account.
4. Select this repository and set `dashboard.py` as the main file.
5. Deploy.

## Notes

- The app uses `company_db.json` for TinyDB persistence.
- For production, use a real cloud database and secure authentication.
