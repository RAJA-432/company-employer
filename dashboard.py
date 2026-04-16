import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tinydb import TinyDB, Query

# Sci-Fi Theme CSS
st.markdown("""
<style>
    /* Sci-Fi Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
        color: #00ffff;
    }
    
    .stTitle {
        color: #00ffff !important;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        font-family: 'Courier New', monospace;
    }
    
    .stHeader {
        color: #ff00ff !important;
        text-shadow: 0 0 5px #ff00ff;
    }
    
    .stSubheader {
        color: #00ff00 !important;
        text-shadow: 0 0 3px #00ff00;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 5px;
        box-shadow: 0 0 5px #00ffff;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #00ffff, #ff00ff) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 5px;
        box-shadow: 0 0 10px #00ffff;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px #00ffff, 0 0 30px #ff00ff;
        transform: scale(1.05);
    }
    
    .stDataFrame {
        background-color: #1a1a1a !important;
        border: 1px solid #00ffff !important;
        border-radius: 5px;
        box-shadow: 0 0 10px #00ffff;
    }
    
    .stDataFrame table {
        color: #00ffff !important;
    }
    
    .stDataFrame th {
        background-color: #2a2a2a !important;
        color: #ff00ff !important;
        border-bottom: 1px solid #00ffff !important;
    }
    
    .stDataFrame td {
        border-bottom: 1px solid #333 !important;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a) !important;
        border: 1px solid #00ffff !important;
        border-radius: 10px;
        box-shadow: 0 0 10px #00ffff;
        color: #00ffff !important;
    }
    
    .stMetric label {
        color: #ff00ff !important;
    }
    
    .stMetric .metric-value {
        color: #00ff00 !important;
        text-shadow: 0 0 5px #00ff00;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #0a0a0a, #1a1a1a) !important;
        border-right: 2px solid #00ffff !important;
    }
    
    .stSidebar .stRadio > div {
        background-color: #1a1a1a !important;
        border: 1px solid #00ffff !important;
        border-radius: 5px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a !important;
        border-bottom: 2px solid #00ffff !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #00ffff !important;
        background-color: #2a2a2a !important;
        border-radius: 5px 5px 0 0;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #00ffff !important;
        color: #000000 !important;
        box-shadow: 0 0 10px #00ffff;
    }
    
    .stSuccess {
        background-color: #001100 !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
        border-radius: 5px;
        box-shadow: 0 0 5px #00ff00;
    }
    
    .stError {
        background-color: #110000 !important;
        color: #ff0000 !important;
        border: 1px solid #ff0000 !important;
        border-radius: 5px;
        box-shadow: 0 0 5px #ff0000;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #00ffff, #ff00ff);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        box-shadow: 0 0 10px #00ffff;
    }

    /* Form styling */
    .stForm {
        background-color: #1a1a1a !important;
        border: 1px solid #00ffff !important;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px #00ffff;
    }
    
    /* Sidebar divider styling */
    .stSidebar hr {
        border-color: #00ffff !important;
        box-shadow: 0 0 5px #00ffff;
    }
    
    /* Sidebar title styling */
    .stSidebar .stTitle, .stSidebar h1 {
        color: #00ffff !important;
        text-shadow: 0 0 10px #00ffff;
    }
    
    /* Sidebar button styling */
    .stSidebar .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #00ffff, #ff00ff) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 5px;
        box-shadow: 0 0 10px #00ffff;
        font-weight: bold;
        transition: all 0.3s ease;
        margin-top: 5px;
    }
    
    .stSidebar .stButton > button:hover {
        box-shadow: 0 0 20px #00ffff, 0 0 30px #ff00ff;
        transform: scale(1.02);
    }

    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 5px;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="🚀 Neural Network Dashboard", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple login system with database authentication
def login():
    st.title("🚀 NEURAL NETWORK ACCESS TERMINAL")

    st.markdown("### Enter Authorization Credentials")
    username = st.text_input("Employee ID (10-digit Neural Code)", placeholder="raj4320000")
    password = st.text_input("Access Key", type="password", placeholder="Enter your access key")

    if st.button("🔓 INITIALIZE CONNECTION", type="primary"):
        username = username.strip()
        password = password.strip()
        
        # First check hardcoded admin
        if username == "raj4320000" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.session_state.user_id = "raj4320000"
            st.success("🛰️ ADMIN ACCESS GRANTED - Welcome to the Neural Network!")
            st.rerun()
            return
        
        # Then check database users
        try:
            db = TinyDB('company_db.json')
            employees_table = db.table('employees')
            users = employees_table.all()
            
            # Check credentials
            for user in users:
                if user.get('employee_id') == username and user.get('password') == password:
                    st.session_state.logged_in = True
                    st.session_state.role = user.get('role', 'employee')
                    st.session_state.user_id = user.get('employee_id')
                    st.success(f"🛰️ ACCESS GRANTED - Neural Link Established for {user.get('role', 'employee').upper()}!")
                    st.rerun()
                    return
            
            st.error("❌ ACCESS DENIED - Invalid Neural Code or Access Key")
        except Exception as e:
            st.error(f"⚠️ SYSTEM ERROR - {e}")

def main_dashboard():
    role = st.session_state.get('role', 'employee')
    user_id = st.session_state.get('user_id')
    
    # Sidebar navigation
    st.sidebar.title("🗂️ NAVIGATION MATRIX")
    if role == 'admin':
        page = st.sidebar.radio("Go to", ["Dashboard", "Admin Panel"])
    else:
        page = "Dashboard"
    
    # Sidebar separator
    st.sidebar.divider()
    
    # Back and Logout buttons in sidebar
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("⬅️ BACK", use_container_width=True, key="back_btn"):
            if page == "Admin Panel":
                st.session_state.page = "Dashboard"
                st.rerun()
    
    with col2:
        if st.button("🔌 LOGOUT", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.user_id = None
            st.rerun()
    
    if page == "Dashboard":
        show_dashboard(role, user_id)
    elif page == "Admin Panel" and role == 'admin':
        show_admin_panel()

def show_dashboard(role, user_id):
    st.title(f"🚀 NEURAL NETWORK DASHBOARD - {role.upper()} INTERFACE")

    # Logout button
    if st.button("🔌 DISCONNECT", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.user_id = None
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
    if role in ['employee', 'employer', 'hr']:
        st.header("📊 NEURAL PERFORMANCE ANALYSIS")
        
        # Department performance
        dept_perf = filtered_df.groupby('department').agg({
            'salary': 'mean',
            'employee_id': 'count'
        }).rename(columns={'employee_id': 'count', 'salary': 'avg_salary'})
        
        st.subheader("🛰️ Sector Performance Metrics")
        st.dataframe(dept_perf.style.format({'avg_salary': '${:,.0f}'}))
        
        # Classification distribution
        st.subheader("🔬 Neural Unit Classification Matrix")
        class_dist = filtered_df['classification'].value_counts()
        st.bar_chart(class_dist)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🛰️ Sector Distribution Matrix")
        dept_chart = px.bar(
            filtered_df.groupby('department').size().reset_index(name='count'),
            x='department',
            y='count',
            title="Employee Count by Department"
        )
        st.plotly_chart(dept_chart, use_container_width=True)

    with col2:
        st.subheader("⚡ Resource Flow Analysis")
        salary_chart = px.histogram(
            filtered_df,
            x='salary',
            nbins=10,
            title="Salary Distribution"
        )
        st.plotly_chart(salary_chart, use_container_width=True)

    # Classification pie chart
    st.subheader("🔬 Neural Classification Spectrum")
    class_pie = px.pie(
        filtered_df.groupby('classification').size().reset_index(name='count'),
        values='count',
        names='classification',
        title="Employee Classification"
    )
    st.plotly_chart(class_pie, use_container_width=True)

    # Management functions for employer and hr
    if role in ['employer', 'hr']:
        st.header("⚙️ NEURAL UNIT MANAGEMENT")
        
        # Registration form
        st.subheader("➕ Deploy New Neural Unit")
        with st.form("register_employee"):
            new_name = st.text_input("Unit Designation")
            new_dept = st.selectbox("Sector Assignment", ["Engineering", "HR", "Finance", "Sales", "Marketing"])
            new_pos = st.text_input("Operational Role")
            new_class = st.selectbox("Energy Classification", ["Full-time", "Part-time", "Contract"])
            new_salary = st.number_input("Resource Allocation", min_value=0, value=50000)
            new_email = st.text_input("Communication Channel")
            new_manager = st.text_input("Command Hierarchy (optional)")
            new_password = st.text_input("Access Code", type="password")
            
            submitted = st.form_submit_button("🚀 DEPLOY UNIT")
            if submitted and new_name and new_password:
                # Check if user already exists
                existing = employees_table.search(Query().name == new_name)
                if existing:
                    st.error("Employee with this name already exists!")
                else:
                    # Generate new employee ID
                    existing_ids = [user.get('employee_id', 'raj4320000') for user in employees_table.all()]
                    # Extract numbers from existing IDs and find the max
                    existing_nums = []
                    for eid in existing_ids:
                        if eid.startswith('raj432') and len(eid) == 10:
                            try:
                                num = int(eid[6:])  # Get last 4 digits
                                existing_nums.append(num)
                            except:
                                pass
                    next_num = max(existing_nums) + 1 if existing_nums else 1
                    new_employee_id = f"raj432{next_num:04d}"
                    
                    new_employee = {
                        "employee_id": new_employee_id,
                        "name": new_name,
                        "department": new_dept,
                        "position": new_pos,
                        "classification": new_class,
                        "salary": new_salary,
                        "hire_date": str(pd.Timestamp.now().date()),
                        "email": new_email,
                        "manager": new_manager if new_manager else None,
                        "password": new_password,
                        "role": "employee"  # Employer/HR can only create employees
                    }
                    employees_table.insert(new_employee)
                    st.success(f"Employee {new_name} registered successfully! Employee ID: {new_employee_id}")
                    st.rerun()

    # Employee table
    st.subheader("📋 Neural Unit Registry")
    st.dataframe(filtered_df, use_container_width=True)

def show_admin_panel():
    st.title("⚡ ADMIN CONTROL MATRIX")

    # Load data
    try:
        db = TinyDB('company_db.json')
        employees_table = db.table('employees')
        data = employees_table.all()
        df = pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return

    # Admin tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 System Matrix", "➕ Deploy Unit", "🗑️ Terminate Unit", "👥 Neural Network"])

    with tab1:
        st.header("🖥️ System Matrix Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", len(df))
        with col2:
            st.metric("Active Employees", len(df[df['role'] == 'employee']))
        with col3:
            st.metric("Employers", len(df[df['role'] == 'employer']))
        with col4:
            st.metric("HR Staff", len(df[df['role'] == 'hr']))
        
        # Role distribution
        st.subheader("User Role Distribution")
        role_dist = df['role'].value_counts()
        st.bar_chart(role_dist)

    with tab2:
        st.header("🚀 Deploy New Neural Unit")
        with st.form("register_employee"):
            new_name = st.text_input("Full Name")
            new_dept = st.selectbox("Department", ["Engineering", "HR", "Finance", "Sales", "Marketing"])
            new_pos = st.text_input("Position")
            new_class = st.selectbox("Classification", ["Full-time", "Part-time", "Contract"])
            new_salary = st.number_input("Salary", min_value=0, value=50000)
            new_email = st.text_input("Email")
            new_manager = st.text_input("Manager (optional)")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["employee", "employer", "hr"])
            
            submitted = st.form_submit_button("Register Employee")
            if submitted and new_name and new_password:
                # Check if user already exists
                existing = employees_table.search(Query().name == new_name)
                if existing:
                    st.error("Employee with this name already exists!")
                else:
                    # Generate new employee ID
                    existing_ids = [user.get('employee_id', 'raj4320000') for user in employees_table.all()]
                    # Extract numbers from existing IDs and find the max
                    existing_nums = []
                    for eid in existing_ids:
                        if eid.startswith('raj432') and len(eid) == 10:
                            try:
                                num = int(eid[6:])  # Get last 4 digits
                                existing_nums.append(num)
                            except:
                                pass
                    next_num = max(existing_nums) + 1 if existing_nums else 1
                    new_employee_id = f"raj432{next_num:04d}"
                    
                    new_employee = {
                        "employee_id": new_employee_id,
                        "name": new_name,
                        "department": new_dept,
                        "position": new_pos,
                        "classification": new_class,
                        "salary": new_salary,
                        "hire_date": str(pd.Timestamp.now().date()),
                        "email": new_email,
                        "manager": new_manager if new_manager else None,
                        "password": new_password,
                        "role": new_role
                    }
                    employees_table.insert(new_employee)
                    st.success(f"Employee {new_name} registered successfully! Employee ID: {new_employee_id}")
                    st.rerun()

    with tab3:
        st.header("💥 Terminate Neural Unit")
        employee_names = df['name'].tolist()
        employee_to_delete = st.selectbox("Select employee to delete", [""] + employee_names)
        
        if employee_to_delete:
            emp_data = df[df['name'] == employee_to_delete].iloc[0]
            st.write("**Employee Details:**")
            st.json({
                "ID": emp_data['employee_id'],
                "Name": emp_data['name'],
                "Department": emp_data['department'],
                "Role": emp_data['role']
            })
            
            if st.button("Confirm Delete", type="primary"):
                emp_id = emp_data['employee_id']
                employees_table.remove(Query().employee_id == emp_id)
                st.success(f"Employee {employee_to_delete} deleted successfully!")
                st.rerun()

    with tab4:
        st.header("🌐 Neural Network Management")
        st.subheader("All Users")
        # Show all users with their details
        user_df = df[['employee_id', 'name', 'department', 'position', 'role', 'email']]
        st.dataframe(user_df, use_container_width=True)
        
        # Export users
        if st.button("Export User List"):
            csv = user_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="company_users.csv",
                mime="text/csv"
            )

# Main app logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None

if not st.session_state.logged_in:
    login()
else:
    main_dashboard()