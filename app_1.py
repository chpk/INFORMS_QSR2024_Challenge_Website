import streamlit as st
from database_1 import add_userdata, login_user
from streamlit.components.v1 import html
import webbrowser
import os

st. set_page_config(layout="wide")
# Initialize the users database
def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)
# Session state initialization for user login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
    
if 'choice' not in st.session_state:
    st.session_state['choice'] = "Login"


def save_uploaded_files(user_id, uploaded_files):
    # Create a directory for the user if it doesn't exist
    directory = os.path.join('submissions', user_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save each uploaded file to the directory
    for uploaded_file in uploaded_files:
        file_path = os.path.join(directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    return len(uploaded_files)

def upload_and_save_ui():
    st.header('Submit Your Code Here')
    # Let user upload multiple files
    uploaded_files = st.file_uploader("Choose files", type=['py', 'txt', 'h5'], accept_multiple_files=True)
    if uploaded_files and st.button('Upload Files'):
        result = save_uploaded_files(st.session_state['user_id'], uploaded_files)
        if result > 0:
            st.success(f"Successfully uploaded {result} files.")
        else:
            st.error("Failed to upload files.")


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
            background-color: #f0f2f6;
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
            A manufacturing designer generates feasible designs and infeasible designs of Microbial Fuel Cell Anode Structure [ref??]. The design variables, generated 3D geometry data in STL files, and the manufacturability are provided, refer to the appendix for dataset structure. Please use ALL samples to train an AI model to classify the manufacturability indicator.
            <br><br>
            There are no limitations on AI models to be used but methodological innovation is highly encouraged. Please use the 3D data from STL files to predict the binary manufacturablility response. Please also discuss your feature engineering and the modeling strategies to process the 3D data. Data can be downloaded here after user registration. Sample code and the environment information can be found in the appendix. Some 3D data pre-processing package can be found in the appendix. To reference the data source, please use. Data reuse and redistribution is not allowed without written consent
            <br><br>
            <b>Training Dataset:</b>
            <ul>
                <li>The Data can be downloaded using this link: .</li>
                <li>Please review the “numpy-stl” python package to process, access, modify, or save the .STL files. Sample codes related to “numpy-stl” can be found here.</li>
                <li>Please refer to Open3D, which is another modern library for 3D data processing. Using this library, you can render, process, modify, and save the STL data, or transform them into voxel or point-cloud representations.</li>
                <li>The stl-to-voxel python package helps you to turn STL files into voxels, images, and videos</li>
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
            This is a team-based competition. Each team should have a maximum of 4 members from academia or industry. Students’ participation is highly encouraged. Python code with required formats, the trained, serialized model object (see the detailed instructions in the appendix), and the result summary (up to 10 slides) should be submitted here [link??] online. Multiple submissions will be allowed for performance tests online, but only the last submission from the team will be used for competition. No email communications will be needed
        """, unsafe_allow_html=True)
        #st.image("image3.png", use_column_width=False)
        if st.button('Submit Your Code Here'):
            print("HI")
            upload_and_save_ui()
        
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
    This competition is partially supported by NSF project XXXX and XXXX.
    """)

def main():
    """INFORMS QSR 2024 Challenge Website"""

    # Display sign-in/sign-up pages if the user is not logged in
    if not st.session_state['logged_in']:
        st.title("Welcome to the INFORMS QSR 2024 Challenge")
        
        menu = ["Login", "SignUp"]
        st.session_state['choice'] = st.sidebar.selectbox("Menu", menu)

        if st.session_state['choice'] == "Login":
            st.subheader("Login Section")

            username = st.text_input("User Name")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                user_data = login_user(username, password)
                print(user_data)
                if user_data:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user_data["username"]
                    st.session_state['user_id'] = user_data["user_id"]  # Save the user_id in the session
                    st.success(f"Logged in as {user_data['username']} with User ID: {user_data['user_id']}")
                    st.experimental_rerun()
                else:
                    st.error("Incorrect Username/Password")

        elif st.session_state['choice'] == "SignUp":
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type='password')

            if st.button("SignUp"):
                add_userdata(new_user, new_password)
                st.success("You have successfully created an account! Please go to the Login menu to log in.")
                st.session_state['choice'] = "Login"
                st.experimental_rerun()
    
    # If the user is logged in, display the home page with competition details
    else:
        display_home_page()
        # More detailed sections from the document...
        
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.experimental_rerun()

if __name__ == '__main__':
    main()
