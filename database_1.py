from pymongo import MongoClient
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MongoDB connection string
CONNECTION_STRING = st.secrets['mongoURI']

client = MongoClient(CONNECTION_STRING)
db = client.user_database  # Name your database
users_collection = db.users  # Name your collection
#print(db, users_collection)

# Function to create a user collection, not typically necessary in MongoDB as collections are created on the fly
def create_collection():
    if "users" not in db.list_collection_names():
        db.create_collection("users")

# Function to add a new user with a unique hex string ID
def add_userdata(new_user, new_password, new_user_name, new_email, new_affiliation, new_user_role):
    user_id = uuid.uuid4().hex  # Generates a random unique hexadecimal ID
    user_data = {"user_id": user_id, "username": new_user, "password": new_password, "name":new_user_name, "email":new_email, "affiliation":new_affiliation, "role":new_user_role}
    result = users_collection.insert_one(user_data)
    return result.inserted_id

# Function for user login
def login_user(username, password):
    """
    Retrieves a user from the database based on username and password.
    Returns the user document if found, None otherwise.
    """
    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return {
            "user_id": user["user_id"],  # Ensure 'user_id' is returned
            "username": user["username"],
            "password": user["password"]  # It's generally not recommended to pass password around
        }
    else:
        return None
def find_user_by_email(email):
    user = users_collection.find_one({"email": email})
    return user

def update_password(username, new_password):
    """
    Update the user's password in the database.
    """
    print(new_password)
    result = users_collection.update_one(
        {"username": username},
        {"$set": {"password": new_password}}
    )
    return result.modified_count == 1  # Returns True if the password was successfully updated

def send_password_email(email, userpassword):
    sender_email = "noreply.qsr24@gmail.com"
    receiver_email = email
    password = "fkui blhi ywxm smqx"  # SMTP server password for sender_email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Hi,
    Your password is {userpassword}. It is recommended to change your password immediately after logging in."""
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


# # Example usage of the functions
# if __name__ == "__main__":
#     create_collection()  # You can call this if you explicitly need to create a collection
#     new_user_id = add_userdata("testuser", "password123")
#     print(f"Added new user with ID: {new_user_id}")

#     logged_in_user = login_user("testuser_1", "password123")
#     if logged_in_user:
#         print("Login successful!")
#     else:
#         print("Login failed!")
# def print_all_users():
#     # Retrieve all documents in the 'users' collection
#     users = users_collection.find()
#     for user in users:
#         print(user)

# if __name__ == "__main__":
#     print_all_users()

# def delete_all_users():
#     # Delete all documents in the 'users' collection
#     result = users_collection.delete_many({})
#     print(f"Number of documents deleted: {result.deleted_count}")
    
# delete_all_users()

