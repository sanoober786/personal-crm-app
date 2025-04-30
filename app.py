import streamlit as st
import json
import os
import uuid

# ---------- Helper Functions ----------

DATA_FILE = "clients.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(clients):
    with open(DATA_FILE, "w") as f:
        json.dump(clients, f, indent=4)

def add_client(client):
    clients = load_data()
    clients.append(client)
    save_data(clients)

def update_client(client_id, updated_client):
    clients = load_data()
    for idx, c in enumerate(clients):
        if c['id'] == client_id:
            clients[idx] = updated_client
            break
    save_data(clients)

def delete_client(client_id):
    clients = load_data()
    clients = [c for c in clients if c['id'] != client_id]
    save_data(clients)

# ---------- Streamlit App ----------

st.set_page_config(page_title="Mini CRM", page_icon="💌", layout="wide")
st.title(" Mini Personal CRM")

menu = st.sidebar.selectbox("Navigate", ["Home", "View Clients", "Add Client"])

# ---------- Home Page ----------

if menu == "Home":
    st.header("Welcome to your Mini CRM!")
    clients = load_data()
    st.metric("Total Clients", len(clients))
    st.success("Use the sidebar to manage your clients.")

# ---------- View Clients Page ----------

elif menu == "View Clients":
    st.header("Your Clients")
    clients = load_data()

    if not clients:
        st.info("No clients added yet.")
    else:
        for client in clients:
            with st.expander(f"{client['name']} ({client['tag']})"):
                st.write(f"**Email:** {client['email']}")
                st.write(f"**Phone:** {client['phone']}")
                st.write(f"**Notes:** {client['notes']}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{client['id']}"):
                        new_name = st.text_input("Name", client['name'], key=f"name_{client['id']}")
                        new_email = st.text_input("Email", client['email'], key=f"email_{client['id']}")
                        new_phone = st.text_input("Phone", client['phone'], key=f"phone_{client['id']}")
                        new_notes = st.text_area("Notes", client['notes'], key=f"notes_{client['id']}")
                        new_tag = st.text_input("Tag", client['tag'], key=f"tag_{client['id']}")
                        if st.button("Save Changes", key=f"save_{client['id']}"):
                            updated = {
                                "id": client['id'],
                                "name": new_name,
                                "email": new_email,
                                "phone": new_phone,
                                "notes": new_notes,
                                "tag": new_tag
                            }
                            update_client(client['id'], updated)
                            st.success("Client updated!")
                            st.experimental_rerun()
                with col2:
                    if st.button("Delete", key=f"delete_{client['id']}"):
                        delete_client(client['id'])
                        st.error("Client deleted!")
                        st.experimental_rerun()

# ---------- Add Client Page ----------

elif menu == "Add Client":
    st.header("Add a New Client")
    with st.form("add_client_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        notes = st.text_area("Notes")
        tag = st.text_input("Tag (e.g., VIP, Prospect)")
        submitted = st.form_submit_button("Add Client")

        if submitted:
            if not name or not email:
                st.error("Name and Email are required!")
            else:
                client = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "notes": notes,
                    "tag": tag
                }
                add_client(client)
                st.success("Client added successfully!")
                st.experimental_rerun()


