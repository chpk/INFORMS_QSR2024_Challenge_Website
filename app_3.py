import streamlit as st
from database_1 import add_userdata, login_user, find_user_by_email, send_password_email, update_password
from streamlit.components.v1 import html
import webbrowser
import os
import pandas as pd


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
        code_file_train = st.file_uploader("Upload your model training code file (.py)", type=['py'], key="traincode")
        code_file_test = st.file_uploader("Upload your model testing code file (.py)", type=['py'], key="testcode")
        requirements_file = st.file_uploader("Upload your requirements file (.txt)", type=['txt'], key="requirements")
        weights_file = st.file_uploader("Upload your weights file", key="weights")
        additional_data_file = st.file_uploader("Upload your results summary report & code execution (test.py) details", key="additionaldata")

        submitted = st.form_submit_button('Upload My Data')
        if submitted:
            # List of files to save
            files_to_save = [code_file_train, code_file_test, requirements_file, weights_file, additional_data_file]
            success = save_files(st.session_state.user_id, files_to_save)
            if success:
                st.balloons()
                st.toast("All files have been successfully uploaded in the new version folder!")
            else:
                st.error("Failed to upload one or more files. Please ensure all files are selected.")

    if st.button('Back to Home Page'):
        st.session_state.page = 'home'
        st.rerun()

def view_leaderboard():
    st.title("Top 10 Participants Leaderboard")

    # Read the leaderboard data from the CSV file
    leaderboard_data = pd.read_csv("leaderboard.csv")

    # Display the leaderboard table
    st.table(leaderboard_data)

    if st.button('Back to Home Page'):
        st.session_state.page = 'home'
        st.rerun()

def display_home_page():
    # Custom CSS to inject into the Streamlit page
    custom_css = """
    <style>
        .stMarkdown-container {
            font-weight: 400;
            font-size: 20px;
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
    col1_1, col2_1, col3_1 = st.columns([0.9, 1.4, 0.9])
    with col2_1:
        st.title("INFORMS QSR 2024 Challenge")
    # Introduction Section with Custom Styling
    #col1, col2 = st.columns([2, 1])
    #with col1:
    st.write("#")
    st.write("#")
    #st.write("#")
    col1_2, col2_2, col3_2 = st.columns([1, 7, 1])
    with col2_2:
        st.image("image1.png", width=1000)
    st.write("#")
    #with col2:
    st.markdown("""
    <style>
        .big-text {
            font-size: 20px;
        }
    </style>
    <div class='section-background'>
        <h1 class='big-font'>Manufacturing AI Competition</h1>
        <p class='big-text'>
            Sponsored by Virginia Tech Academy of Data Science and INFORMS Quality, Statistics, and Reliability Section
            <br><br>
            The Quality, Statistics, and Reliability (QSR) Section of the Institute for Operations Research and the Management Sciences (INFORMS) announces the Data Challenge Award to recognize excellence in data modeling techniques among the submissions to the 2024 QSR Data Challenge Competition. This award program brings prestige to the QSR Section as well as to the recipients honored.
            <br><br>
            <b>2024 INFORMS Annual Meeting</b><br>
            Date: October 20 – 23, 2024<br>
            Location: Seattle, Washington, USA
            <br><br>
            <b>Important Dates:</b>
            <ul class='big-text'>
                <li>Submission Deadline: August 19, 2024</li>
                <li>Notification of Finalists: September 2, 2024</li>
                <li>Presentations: October 20 – 23, 2024</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
    #st.button('View Flyer', on_click=open_page('./Call for Participation_HS.pdf'))
    st.markdown("---")    
    st.write("#")
    #st.write("#")
    #st.write("#")
    # Alternating Sections with Images and Text
    #col1, col2 = st.columns([1, 1])
    #with col1:
    # HTML code
    html_code = """
    <div class='section-background'>
        <h2 class='big-font'>Problem Statement</h2>
        <p class='big-text'>
            Predict the manufacturability of Microbial Fuel Cell Anode Structures using the provided dataset containing design variables, 3D geometry data in STL files, and binary manufacturability labels. The dataset consists of 1,000 designs with a 70/30 split between feasible and infeasible designs.
            <br><br>
            Develop an AI model to classify the manufacturability indicator using the entire dataset for training. Feature engineering and innovative modeling strategies to process the 3D data are highly encouraged. Sample code and environment information can be found in the <a href="https://drive.google.com/file/d/1F7YcRGvhfV8vLOIpfVNBwrirJyw1-rIr/view?usp=sharing" target='_blank'>competition flyer</a>.
            <br><br>
            <b>Dataset Details:</b>
            <ul class='big-text'>
                <li>Download the dataset using this link. Please view the terms and conditions before downloading.</li>
                <li>Refer to the <a href="https://pypi.org/project/numpy-stl/" target='_blank'>numpy-stl</a> and <a href="https://github.com/isl-org/Open3D" target='_blank'>Open3D</a> libraries for processing STL files.</li>
                <li>Consider using the <a href="https://pypi.org/project/stl-to-voxel/" target='_blank'>stl-to-voxel</a> package to convert STL files into voxels, images, or videos.</li>
            </ul>
            <span class='big-text'>Data reuse and redistribution is not allowed without written consent.</span>
        </p>
    </div>
    """

    # CSS code
    css_code = """
    <style>
        .big-text {
            font-size: 20px;
        }
    </style>
    """

    # Render the HTML and CSS code
    st.markdown(css_code + html_code, unsafe_allow_html=True)

    # Terms and Conditions
    terms_and_conditions = """
    ### Terms and Conditions

    By downloading the data files, you agree with the following terms to process the data:

    1. The data that I handled are generated from the Laboratory of Data Science and Visualization. The data are Virginia Tech's property and belong to Dr. Ran Jin's research lab.
    2. Re-distribution of the data will not be allowed with other personnel besides my manufacturing AI competition teammates. I will not use the data for other purposes such as research publications, without written approval from Dr. Ran Jin (jran5@vt.edu). Appropriate references must be included in my future publications.
    3. Disclosure period: The data should never be disclosed if no written approval is provided.
    """

    # Display the terms and conditions in an expander
    with st.expander("View Terms and Conditions"):
        st.markdown(terms_and_conditions)

    # Checkbox for agreeing to the terms and conditions
    agree_checkbox = st.checkbox("I agree to the terms and conditions")

    # Download button
    if agree_checkbox:
        st.markdown("[Download Dataset](https://virginiatech-my.sharepoint.com/:f:/g/personal/cpremithkumar_vt_edu/EkhUukjjYfBBrITV-J2DB7cB4WETZKDY6RHPNzu3jbkLbA?e=Vsi75Y)")
    else:
        st.markdown("Please agree to the terms and conditions to download the dataset.")

    if st.button('View Flyer'):
        webbrowser.open_new_tab("https://drive.google.com/file/d/1F7YcRGvhfV8vLOIpfVNBwrirJyw1-rIr/view?usp=sharing")
        
        #st.image("image3.png", use_column_width=False)
    #with col2:
    #    st.image("image2.png", use_column_width=True)
    st.markdown("---")    
    st.write("#")
    #st.write("#")
    #st.write("#")
    # Alternating Sections with Images and Text
    #col1, col2 = st.columns([1, 1])
    #with col1:
    #    st.image("image4.png", use_column_width=True)
    #with col2:
    st.markdown("""
    <style>
        .big-text {
            font-size: 20px;
        }
    </style>
    <div class='section-background'>
        <h2 class='big-font'>Submission Procedure</h2>
        <p class='big-text'>
            This is a team-based competition. Each team should have a maximum of 4 members from academia or industry. Students' participation is highly encouraged. Only <b>PYTHON</b> code with required formats, the trained and serialized model object <b>weight file</b> (see the detailed instructions in the <a href="https://drive.google.com/file/d/1F7YcRGvhfV8vLOIpfVNBwrirJyw1-rIr/view?usp=sharing" target='_blank'>competition flyer</a>), and a <b>result summary report</b> should be submitted here using the below provided button. Multiple submissions will be allowed for performance tests online, but only the last submission from the team will be used for competition. No email communications will be needed.
            <br><br>
            Please upload a Python file named <b>test.py</b> containing the inference code for your trained model. The <b>test.py</b> file should adhere to the following guidelines:
            <ol>
                <li>The code should automatically load the trained model's weight file using the relative path of the saved weight file.</li>
                <li>The code should read all the <b>.stl</b> files present in the test directory (<b>"./Test Data/"</b>) and perform inference on each file.</li>
                <li>The model should perform binary classification on the test data and generate predictions.</li>
                <li>The binary classification results should be saved in a file named <b>"Save_Predictions.csv"</b>. The format of the saved predictions should match the data frame format provided in the appendix of the competition flyer.</li>
            </ol>
            <span class='big-text'>Please ensure that your <b>test.py</b> file follows these requirements and can be executed successfully to generate the desired predictions. The organizers will use this file to evaluate your model's performance on the undisclosed test dataset.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    #st.image("image3.png", use_column_width=False)
    if st.button('Submit Your Data Here'):
        #print("HI")
        st.session_state.page = 'submit'
        st.rerun()
            
        
    st.markdown("---")    
    st.write("#")
    # Alternating Sections with Images and Text
    #col1, col2 = st.columns([1, 1])
    #with col1:
    st.markdown("""
    <style>
        .big-text {
            font-size: 20px;
        }
    </style>
    <div class='section-background'>
        <h2 class='big-font'>Evaluation Procedure</h2>
        <p class='big-text'>
        The performance of the algorithms will be automatically evaluated on an undisclosed testing dataset generated from the same design simulation engine with the same parameter settings. Three finalists will be selected based on the performance of the algorithms and will be required to present the methodology and the results in an in-person session in INFORMS annual meeting 2024. One winning team (<b>see the leaderboard for results</b>) will be selected by judges and all finalists will be recognized in the INFORMS-QSR business meeting. Finalists may be invited to participate in future activities, such as industrial engagement and research exchange, held by Virginia Tech Academy of Data Science
                </p>
    """, unsafe_allow_html=True)
    if st.button('View Leaderboard'):
        #print("HI")
        st.session_state.page = 'leaderboard'
        st.rerun()
    #st.image("image3.png", use_column_width=False)
    #with col2:
    #    st.image("image5.png", use_column_width=True)
    st.markdown("---")    
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
            st.rerun()
    elif st.session_state.page == 'submit':
        submission_page()
    elif st.session_state.page == 'leaderboard':
        view_leaderboard()
    else:
        if not st.session_state.logged_in:
            st.title("Welcome to the INFORMS QSR 2024 Challenge")
            #menu = ["  ","Login", "SignUp"]
            if st.sidebar.button("Login"):
                st.session_state.choice = "Login"
                st.rerun()
            if st.sidebar.button("SignUp"):
                st.session_state.choice = "SignUp"
                st.rerun()
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
                        st.rerun()
                    else:
                        st.error("Incorrect Username/Password")
                st.write("#")
                st.write("#") 
                st.write("#")
                if st.button("Forgot Password"):
                    st.session_state.choice = "Forgot Password"
                    print("FP")
                    st.rerun()
                if st.button("Update Password"):
                    st.session_state.choice = "Update Password"
                    st.rerun()

            elif st.session_state.choice == "SignUp":
                st.subheader("Create New Account")
                new_user_name_firstname = st.text_input("First Name")
                new_user_name_last_name = st.text_input("Last Name")
                new_email = st.text_input("E-Mail")
                new_affiliation = st.text_input("Affiliation (Company/University)")
                new_user_role = st.text_input("Role")
                new_user = st.text_input("Username")
                new_password = st.text_input("Password", type='password')
    
                if st.button("Register",type="primary"):
                    add_userdata(new_user, new_password, new_user_name_firstname + " , " + new_user_name_last_name, new_email, new_affiliation, new_user_role)
                    st.toast("You have successfully created an account! Please go to the Login menu to log in.")
                    st.session_state.choice = "Login"
                    st.session_state.page = 'login'
                    st.rerun()
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
