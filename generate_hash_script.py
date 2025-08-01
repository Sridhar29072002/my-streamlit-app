import streamlit_authenticator as stauth

# List of plain-text passwords
passwords = ['1234', 'admin123']

# Initialize hasher
hasher = stauth.Hasher()

# Hash each password individually
hashed_passwords = [hasher.hash(pwd) for pwd in passwords]

# Print the hashed passwords
for pwd in hashed_passwords:
    print(pwd)





