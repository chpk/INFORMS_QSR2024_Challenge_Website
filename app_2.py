import streamlit as st
from database_1 import add_userdata, login_user, find_user_by_email, send_password_email, update_password
from streamlit.components.v1 import html
import webbrowser
import os
import base64


st. set_page_config(layout="wide")
# Initialize the users database
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)
# Session state initialization for user login status

def change_password():
    st.subheader("Change Password")
    username = st.text_input("Username", key="username_reset")
    old_password = st.text_input("Old Password", type="password", key="old_password")
    new_password = st.text_input("New Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
    
    if st.button("Update Password"):
        user_data = login_user(username, old_password)
        if user_data and new_password == confirm_password:
            if update_password(username, new_password):
                st.success("Your password has been updated successfully.")
            else:
                st.error("Failed to update password.")
        elif not user_data:
            st.error("Incorrect username or old password.")
        else:
            st.error("New passwords do not match.")
            
def save_files(user_id, files):
    if all(files):
        base_directory = os.path.join('submissions', user_id)
        version = 1

        # Check existing versions and determine the new version number
        while os.path.exists(os.path.join(base_directory, f'V{version}')):
            version += 1

        # Create a new version directory if it doesn't exist
        directory = os.path.join(base_directory, f'V{version}')
        os.makedirs(directory, exist_ok=True)

        # Save all uploaded files to the new version directory
        successes = []
        for uploaded_file in files:
            file_path = os.path.join(directory, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            successes.append(True)

        return all(successes)
    return False

def submission_page():
    st.header('Submit Your Files')
    with st.form("file_upload_form"):
        code_file = st.file_uploader("Upload your code file (.py)", type=['py'], key="code")
        requirements_file = st.file_uploader("Upload your requirements file (.txt)", type=['txt'], key="requirements")
        weights_file = st.file_uploader("Upload your weights file", key="weights")
        additional_data_file = st.file_uploader("Upload your results summary report", key="additionaldata")

        submitted = st.form_submit_button('Upload My Data')
        if submitted:
            # List of files to save
            files_to_save = [code_file, requirements_file, weights_file, additional_data_file]
            success = save_files(st.session_state.user_id, files_to_save)
            if success:
                st.balloons()
                st.toast("All files have been successfully uploaded in the new version folder!")
            else:
                st.error("Failed to upload one or more files. Please ensure all files are selected.")

    if st.button('Back to Home Page'):
        st.session_state.page = 'home'
        st.experimental_rerun()


def display_home_page():
    # Custom CSS to inject into the Streamlit page
    custom_css = """
    <style>
        .stMarkdown-container {
            font-weight: 400;
            font-size: 16px;
            line-height: 1.5;
        }
        .reportview-container .markdown-text-container {
            font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        }
        .big-font {
            font-size:35px !important;
            font-weight: 500;
        }
        .image-caption {
            font-style: italic;
            font-size: 14px;
            text-align: center;
        }
        .section-background {
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0px;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    st.title("INFORMS QSR 2024 Challenge")

    # Introduction Section with Custom Styling
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image("image1.png", use_column_width=True)
    with col2:
        st.markdown("""
        <div class='section-background'>
            <h1 class='big-font'>Manufacturing AI Competition</h2>
            Sponsored by Virginia Tech Academy of Data Science and INFORMS Quality, Statistics, and Reliability Section
            <br><br>
            The Quality, Statistics, and Reliability (QSR) Section of the Institute for Operations Research and the Management Sciences (INFORMS) announces the Data Challenge Award to recognize excellence in data modeling techniques among the submissions to the 2024 QSR Data Challenge Competition. This award program brings prestige to the QSR Section as well as to the recipients honored. 
            <br><br>
            <b>2024 INFORMS Annual Meeting</b><br>
            Date: October 20 – 23, 2024<br>
            Location: Seattle, Washington, USA
            <br><br>
            <b>Important Dates:</b>
            <ul>
                <li>Submission Deadline: August 19, 2024</li>
                <li>Notification of Finalists: September 2, 2024</li>
                <li>Presentations: October 20 – 23, 2024</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    #st.button('View Flyer', on_click=open_page('./Call for Participation_HS.pdf'))
    st.write("#")
    st.write("#")
    st.write("#")
    # Alternating Sections with Images and Text
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class='section-background'>
            <h2 class='big-font'>Problem Statement</h2>
            A manufacturing designer generates feasible designs and infeasible designs of Microbial Fuel Cell Anode Structure. The design variables, generated 3D geometry data in STL files, and the design-manufacturability/feasibility are provided, refer to the <a href="https://drive.google.com/file/d/1F7YcRGvhfV8vLOIpfVNBwrirJyw1-rIr/view?usp=sharing" target='_blank'>competition flyer</a> for dataset structure. Please use ALL samples to train your AI model to classify the manufacturability indicator.
            <br><br>
            There are no limitations on AI models to be used but methodological innovation is highly encouraged. Please use the 3D data from STL files to predict the binary manufacturablility response. Please also discuss your feature engineering and the modeling strategies to process the 3D data. Sample code and the environment information can be found in the <a href="https://drive.google.com/file/d/1F7YcRGvhfV8vLOIpfVNBwrirJyw1-rIr/view?usp=sharing" target='_blank'>competition flyer</a>. Some 3D data pre-processing package can be found in the competetion flyer. To reference the data source, please use. Data reuse and redistribution is not allowed without written consent
            <br><br>
            <b>Training Dataset:</b>
            <ul>
                <li>The Data can be downloaded using this <a href="https://virginiatech-my.sharepoint.com/:f:/g/personal/cpremithkumar_vt_edu/EkhUukjjYfBBrITV-J2DB7cB4WETZKDY6RHPNzu3jbkLbA?e=Vsi75Y" target='_blank'>link</a> .</li>
                <li>Please review the <a href="https://pypi.org/project/numpy-stl/" target='_blank'> numpy-stl python package</a> to process, access, modify, or save the .STL files. Sample codes related to `numpy-stl` can be found here.</li>
                <li>Please refer to <a href="https://github.com/isl-org/Open3D" target='_blank'> Open3D</a>, which is another modern library for 3D data processing. Using this library, you can render, process, modify, and save the STL data, or transform them into voxel or point-cloud representations.</li>
                <li>The <a href="https://pypi.org/project/stl-to-voxel/" target='_blank'> stl-to-voxel python package</a> helps you to turn STL files into voxels, images, and videos</li>
            </ul>
            <b>Dataset Details and Structure:</b>
            <ul>
                <li>A total of 1,000 designs with 70% feasible ones and 30% infeasible ones. Design variables and generated 3D geometry data in .STL format are provided. Folder and file structure of the dataset can be found in the Challenge Flyer here</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button('View Flyer'):
            webbrowser.open_new_tab("https://drive.google.com/file/d/1F7YcRGvhfV8vLOIpfVNBwrirJyw1-rIr/view?usp=sharing")
        
        if st.button('Download Dataset'):
            webbrowser.open_new_tab("https://virginiatech-my.sharepoint.com/:f:/g/personal/cpremithkumar_vt_edu/EkhUukjjYfBBrITV-J2DB7cB4WETZKDY6RHPNzu3jbkLbA?e=Vsi75Y")
        
        #st.image("image3.png", use_column_width=False)
    with col2:
        st.image("image2.png", use_column_width=True)
        
    st.write("#")
    st.write("#")
    st.write("#")
    # Alternating Sections with Images and Text
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("image4.png", use_column_width=True)
    with col2:
        st.markdown("""
        <div class='section-background'>
            <h2 class='big-font'>Submission Procedure</h2>
            This is a team-based competition. Each team should have a maximum of 4 members from academia or industry. Students’ participation is highly encouraged. Python code with required formats, the trained, serialized model object (see the detailed instructions in the <a href="https://drive.google.com/file/d/1F7YcRGvhfV8vLOIpfVNBwrirJyw1-rIr/view?usp=sharing" target='_blank'>competition flyer</a>), and the result summary (up to 10 slides) should be submitted here using the below provided button. Multiple submissions will be allowed for performance tests online, but only the last submission from the team will be used for competition. No email communications will be needed.
        """, unsafe_allow_html=True)
        #st.image("image3.png", use_column_width=False)
        if st.button('Submit Your Data Here'):
            print("HI")
            st.session_state.page = 'submit'
            st.experimental_rerun()
            
        
    st.write("#")
    st.write("#")
    st.write("#")
    # Alternating Sections with Images and Text
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class='section-background'>
            <h2 class='big-font'>Evaluation Procedure</h2>
            The performance of the algorithms will be automatically evaluated on an undisclosed testing dataset generated from the same design simulation engine with the same parameter settings. Three finalists will be selected based on the performance of the algorithms and will be required to present the methodology and the results in an in-person session in INFORMS annual meeting 2024. One winning team will be selected by judges and all finalists will be recognized in the INFORMS-QSR business meeting. Finalists may be invited to participate in future activities, such as industrial engagement and research exchange, held by Virginia Tech Academy of Data Science
        """, unsafe_allow_html=True)
        #st.image("image3.png", use_column_width=False)
    with col2:
        st.image("image5.png", use_column_width=True)
    st.write("#")
    st.write("#")
    st.write("#")
    st.header("Organizers")
    st.markdown("""
    - Dr. Tom Woteki, Virginia Tech ([drwo@vt.edu](mailto:drwo@vt.edu))
    - Dr. Xiaoyu Chen, University at Buffalo ([xchen325@buffalo.edu](mailto:xchen325@buffalo.edu))
    - Dr. Ran Jin, Virginia Tech ([jran5@vt.edu](mailto:jran5@vt.edu))
    - Dr. Ismini Lourentzou, University of Illinois Urbana-Champaign ([lourent2@illinois.edu](mailto:lourent2@illinois.edu)) 
    - Dr. Hongyue Sun, University of Georgia ([hongyuesun@uga.edu](mailto:hongyuesun@uga.edu))
    
    **Technical Support**: Mr. Premith Chilukuri, Virginia Tech ([cpremithkumar@vt.edu](mailto:cpremithkumar@vt.edu))
    """)
    st.header("Acknowledgement")
    st.markdown("""
    This competition is partially supported by NSF project CMMI-2208864 and CMMI-2331985.
    """)
    

def display_forgot_password():
    st.subheader("Forgot Password")
    email = st.text_input("Please enter your email address:")
    if st.button("Send Password"):
        user = find_user_by_email(email)
        if user:
            # Ideally, here you would send a password reset link rather than the password itself
            send_password_email(user['email'], user['password'])
            st.toast("An email with your password has been sent.")
        else:
            st.error("No account found with that email.")


def main():
    """INFORMS QSR 2024 Challenge Website"""
    #st.set_page_config(layout="wide")
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
        
    if 'choice' not in st.session_state:
        st.session_state.choice = "Login"
    
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
        
    # Display sign-in/sign-up pages if the user is not logged in
    if st.session_state.page == 'home':
        display_home_page()
        #if st.button("Submit Your Code Here"):
            #st.session_state.page = 'submit'
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.page = 'login'
            #st.session_state.clear()
            st.experimental_rerun()
    elif st.session_state.page == 'submit':
        submission_page()
    else:
        if not st.session_state.logged_in:
            st.title("Welcome to the INFORMS QSR 2024 Challenge")
            #menu = ["  ","Login", "SignUp"]
            if st.sidebar.button("Login"):
                st.session_state.choice = "Login"
                st.experimental_rerun()
            if st.sidebar.button("SignUp"):
                st.session_state.choice = "SignUp"
                st.experimental_rerun()
            if st.session_state.choice == "Login":
                st.subheader("Login Here")
                username = st.text_input("User Name")
                password = st.text_input("Password", type='password')
                if st.button("Submit",type="primary"):
                    user_data = login_user(username, password)
                    print(user_data)
                    if user_data:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = user_data["username"]
                        st.session_state['user_id'] = user_data["user_id"]  # Save the user_id in the session
                        st.toast(f"Logged in as {user_data['username']} with User ID: {user_data['user_id']}")
                        st.session_state.page = 'home'
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect Username/Password")
                st.write("#")
                st.write("#") 
                st.write("#")
                if st.button("Forgot Password"):
                    st.session_state.choice = "Forgot Password"
                    print("FP")
                    st.experimental_rerun()
                if st.button("Update Password"):
                    st.session_state.choice = "Update Password"
                    st.experimental_rerun()

            elif st.session_state.choice == "SignUp":
                st.subheader("Create New Account")
                new_user_name = st.text_input("Full Name")
                new_email = st.text_input("E-Mail")
                new_affiliation = st.text_input("Your Affiliation (Company/University)")
                new_user_role = st.text_input("Role in the Company/University")
                new_user = st.text_input("Username")
                new_password = st.text_input("Password", type='password')
    
                if st.button("Register",type="primary"):
                    add_userdata(new_user, new_password, new_user_name, new_email, new_affiliation, new_user_role)
                    st.toast("You have successfully created an account! Please go to the Login menu to log in.")
                    st.session_state.choice = "Login"
                    st.session_state.page = 'login'
                    st.experimental_rerun()
            elif st.session_state.choice == "Forgot Password":
                display_forgot_password()
            elif st.session_state.choice == "Update Password":
                change_password()
            
if __name__ == '__main__':
    main()

# [9:54 AM] Jin, Ran
# CMMI-2331985
# [9:56 AM] Jin, Ran
# CMMI-2208864