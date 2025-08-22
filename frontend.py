import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("FastAPI+Streamlit")

# || CREATE USER ||
st.header("Add User")
with st.form("add_user_form"):
    user_id = st.number_input("User ID:", min_value=1, step=1)
    name = st.text_input("Name:")
    contact = st.text_input("Contact No. (03xxxxxxxxx):")
    submitted = st.form_submit_button("Add User")

    if submitted:
        payload = {"id": user_id, "name": name, "contact_no": contact} # 'Payload' is the request(data) sent and received between API and frontend.
        response = requests.post(f"{BASE_URL}/add_user/", json=payload)
        if response.status_code == 200:
            st.success("User added successfully!")
            st.json(response.json())
        else:
            st.error(response.json()["detail"])
# || CREATE USER ||

# || READ USERS ||
st.header("View All Users")
if st.button("Fetch Users"):
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        users = response.json()
        if users:
            st.table(users)
        else:
            st.info("No users found.")
    else:
        st.error("Error fetching users")
# || READ USERS ||

# || GET BY ID ||
st.header("Get User by ID")
search_id = st.number_input("Enter User ID to Search", min_value=1, step=1)
if st.button("Get User"):
    response = requests.get(f"{BASE_URL}/get_by_id/{search_id}")
    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error(response.json()["detail"])
# || GET BY ID ||

# || UPDATE USER ||
st.header("Update User")
with st.form("update_user_form"):
    update_id = st.number_input("User ID to Update:", min_value=1, step=1)
    new_name = st.text_input("New Name:")
    new_contact = st.text_input("New Contact No. (03xxxxxxxxx):")
    update_btn = st.form_submit_button("Update User")

    if update_btn:
        payload = {"name": new_name, "contact_no": new_contact} # 'Payload' is the request(data) sent and received between API and frontend.
        response = requests.put(f"{BASE_URL}/modify_creds/{update_id}", json=payload)
        if response.status_code == 200:
            st.success("User updated successfully!")
            st.json(response.json())
        else:
            st.error(response.json()["detail"])
# || UPDATE USER ||

# || DELETE USER ||
st.header("Delete User")
delete_id = st.number_input("User ID to Delete", min_value=1, step=1)
if st.button("Delete User"):
    response = requests.delete(f"{BASE_URL}/delete_user/{delete_id}")
    if response.status_code == 200:
        st.success("User deleted successfully!")
        st.json(response.json())
    else:
        st.error(response.json()["detail"])
# || DELETE USER ||

# streamlit run frontend.py