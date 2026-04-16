import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tinydb import TinyDB, Query

# Page configuration
st.set_page_config(page_title="Company Employee Dashboard", page_icon="🏢", layout="wide")

# Simple login system with roles
def login():
    st.title("🏢 Company Employee Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Simple hardcoded credentials with roles
        users = {
            "admin": {"password": "admin123", "role": "admin"},
            "employee": {"password": "emp123", "role": "employee"},
            "employer": {"password": "emp123", "role": "employer"}
        }
        if username in users and password == users[username]["password"]:
            st.session_state.logged_in = True
            st.session_state.role = users[username]["role"]
            st.success(f"Login successful as {users[username]['role']}!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def main_dashboard():
    role = st.session_state.get('role', 'employee')
    st.title(f"🏢 Company Employee Dashboard ({role.title()})")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    # Load data from TinyDB
    try:
        db = TinyDB('company_db.json')
        employees_table = db.table('employees')
        data = employees_table.all()
        df = pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return

    # Sidebar filters
    st.sidebar.header("Filters")

    departments = st.sidebar.multiselect(
        "Select Departments",
        options=df['department'].unique(),
        default=df['department'].unique()
    )

    classifications = st.sidebar.multiselect(
        "Select Classifications",
        options=df['classification'].unique(),
        default=df['classification'].unique()
    )

    # Filter data
    filtered_df = df[
        (df['department'].isin(departments)) &
        (df['classification'].isin(classifications))
    ]

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Employees", len(filtered_df))

    with col2:
        avg_salary = filtered_df['salary'].mean()
        st.metric("Average Salary", f"${avg_salary:,.0f}")

    with col3:
        st.metric("Departments", len(filtered_df['department'].unique()))

    with col4:
        st.metric("Classifications", len(filtered_df['classification'].unique()))

    # Performance Assessment Section
    if role in ['employee', 'employer']:
        st.header("📊 Performance Assessment")
        
        # Department performance
        dept_perf = filtered_df.groupby('department').agg({
            'salary': 'mean',
            'employee_id': 'count'
        }).rename(columns={'employee_id': 'count', 'salary': 'avg_salary'})
        
        st.subheader("Department Performance")
        st.dataframe(dept_perf.style.format({'avg_salary': '${:,.0f}'}))
        
        # Classification distribution
        st.subheader("Employee Classification Distribution")
        class_dist = filtered_df['classification'].value_counts()
        st.bar_chart(class_dist)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Employees by Department")
        dept_chart = px.bar(
            filtered_df.groupby('department').size().reset_index(name='count'),
            x='department',
            y='count',
            title="Employee Count by Department"
        )
        st.plotly_chart(dept_chart, use_container_width=True)

    with col2:
        st.subheader("Salary Distribution")
        salary_chart = px.histogram(
            filtered_df,
            x='salary',
            nbins=10,
            title="Salary Distribution"
        )
        st.plotly_chart(salary_chart, use_container_width=True)

    # Classification pie chart
    st.subheader("Employee Classification Distribution")
    class_pie = px.pie(
        filtered_df.groupby('classification').size().reset_index(name='count'),
        values='count',
        names='classification',
        title="Employee Classification"
    )
    st.plotly_chart(class_pie, use_container_width=True)

    # Admin functions
    if role == 'admin':
        st.header("⚙️ Admin Functions")
        
        # Delete employee
        st.subheader("Delete Employee")
        employee_names = filtered_df['name'].tolist()
        employee_to_delete = st.selectbox("Select employee to delete", [""] + employee_names)
        
        if st.button("Delete Employee") and employee_to_delete:
            # Find and delete from database
            emp_id = filtered_df[filtered_df['name'] == employee_to_delete]['employee_id'].iloc[0]
            employees_table.remove(Query().employee_id == emp_id)
            st.success(f"Employee {employee_to_delete} deleted successfully!")
            st.rerun()

    # Employee table
    st.subheader("Employee Details")
    st.dataframe(filtered_df, use_container_width=True)

# Main app logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None

if not st.session_state.logged_in:
    login()
else:
    main_dashboard()