import streamlit as st
from api_client import login_user, register_user

def show_login_form():
    """
    Display login form in Streamlit.
    """
    st.markdown("### Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", type="default")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if email and password:
                try:
                    login_response = login_user(email, password)
                    st.session_state["access_token"] = login_response["access_token"]
                    st.session_state["user_id"] = login_response["user_id"]
                    st.session_state["user_email"] = login_response["email"]
                    st.session_state["user_name"] = login_response["full_name"]
                    st.session_state["authenticated"] = True
                    st.success("Login successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
            else:
                st.error("Please fill in all fields")

def show_register_form():
    """
    Display registration form in Streamlit.
    """
    st.markdown("### Register")
    
    with st.form("register_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email", type="default")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if full_name and email and password and confirm_password:
                if password == confirm_password:
                    try:
                        register_response = register_user(email, password, full_name)
                        st.success("Registration successful! Please login.")
                    except Exception as e:
                        st.error(f"Registration failed: {str(e)}")
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Please fill in all fields")

def show_auth_page():
    """
    Display authentication page with login and register tabs.
    """
    st.markdown("<h1 style='text-align: center; color: navy;'>Elder Care Management System</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()

def logout():
    """
    Clear session state and logout user.
    """
    for key in ["access_token", "user_id", "user_email", "user_name", "authenticated"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Logged out successfully!")
    st.rerun() 