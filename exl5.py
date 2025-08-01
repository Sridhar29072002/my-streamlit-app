import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from openpyxl import load_workbook

# Load config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Setup authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Show login
authenticator.login(location='main')

# Use internal state instead of unpacking
if st.session_state["authentication_status"]:
    st.success(f"Welcome {st.session_state['name']} 👋")
    authenticator.logout("Logout", "sidebar")

    # Excel operations
    file_path = r'C:\Users\Sridhar\Documents\producttrail\product trail.xlsx'

    df = pd.read_excel(file_path, engine='openpyxl')
    date_columns = [col for col in df.columns if col != 'prod']
    formatted_dates = [pd.to_datetime(col).strftime('%d-%m-%Y') for col in date_columns]
    df.columns = ['prod'] + formatted_dates

    search_text = st.text_input("Search product (type part of name):").lower()
    filtered_products = df['prod'][df['prod'].str.lower().str.contains(search_text)].tolist()
    selected_product = st.selectbox("Select product:", filtered_products) if filtered_products else None

    selected_date = st.selectbox("Select date:", options=formatted_dates)
    new_qty = st.number_input("Enter new quantity:", min_value=0, step=1)

    if st.button("Update Quantity"):
        if selected_product and selected_date:
            row_idx = df[df['prod'] == selected_product].index[0]
            df.at[row_idx, selected_date] = new_qty

            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

            st.success(f"Updated '{selected_product}' on {selected_date} to quantity: {new_qty}")
        else:
            st.warning("Please select a valid product and date.")

elif st.session_state["authentication_status"] is False:
    st.error("Invalid username or password")

elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your login credentials.")
