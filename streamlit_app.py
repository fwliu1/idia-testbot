import streamlit as st
import google.generativeai as genai

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'context' not in st.session_state:
    st.session_state.context = ""

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_gemini_response(model, question, user_type, context):
    user_type_prompts = {
        "Kid": "You are talking to a child. Use simple language and explanations suitable for children. Keep responses brief and engaging.",
        "Adult": "You are conversing with an adult. Provide detailed and comprehensive responses.",
        "Senior": "You are speaking with a senior citizen. Be respectful, patient, and use clear language. Consider potential health or technology-related concerns in your responses."
    }
    
    full_prompt = f"""
    {context}

    You are an AI assistant for CTEC. Always be helpful, friendly, and informative. 
    {user_type_prompts.get(user_type, '')}
    
    If asked about information not provided in the context, politely state that you don't have that specific information 
    and offer to help with general inquiries or direct them to contact the center's staff for the most up-to-date information.

    Human: {question}
    AI Assistant:
    """
    response = model.generate_content(full_prompt)
    return response.text

# Streamlit app
st.title("IDIA Chatbot Assistant")

# Sidebar for context input (for demo purposes, normally this would be pre-set)
#st.sidebar.title("Set Envision Center Information")
context_input = """
IDIA (formerly Digital Equity Institute) is a nonprofit dedicated to improving the quality of life for people around the globe through digital inclusion.
Our mission is bold but simple: to eliminate the digital divide – the gap between those who have affordable access, skills, and support to effectively engage online and those who do not. We are co-creating communities in which every individual, regardless of their background, can thrive in the digital age. 

What IDIA Does:
* IDIA co-creates programs, workshops and tools, like our Community Technology Hives, designed to enhance digital skills for all ages and life contexts.
* Partners with other organizations through local and global initiatives to create human-centric, future-focused, accessible digital programs.
* IDIA informs and champions programs that promote digital inclusivity and equity. We work tirelessly to ensure that digital rights and access are recognized and prioritized.

The Staff at the HIVE:
*Erin Carr-Jordan, Ph.D. President & CEO
*Annissa Furr, Ph.D. Head of Learning and Research
* Dominic Papa Chief Government Relations Officer
*Stephanie Pierotti Head of Community Activation
*Tori Blusiewicz Administrative Coordinator
*Luis Morfin Digital Navigator Manager
*Josh Thompson, Ph.D. Program Manager
* Digital Navigators work in the HIVES.

Summary of the Digital Navigators job:
*Our Digital Navigators are here to make technology more approachable and understandable for all community members. They serve as mentors, guides, and facilitators in the journey towards  achieving digital confidence. Our goal is to ensure experiences for digital empowerment are accessible to all.
*Personalized Support
*Youth and Adult Education
*Classes and Workshops
*Collaborative Learning
*Community Voice

These are the HIVES
* The Hive at Aeroterra, Inside Aeroterra Community Center in Edison-Eastlake
-1725 E McKinley Street, Phoenix, Arizona 85006
HOURS OF OPERATION for the HIVE at Aeroterra
Mondays + Wednesday + Thursday 12pm-6pm
Tuesday + Friday 10am-4pm
Second Saturday of each month 10am-2pm

* The Hive at CTEC
Inside Emmett McLoughlin Community Training and Education Center
1150 S. 7th Avenue, Phoenix, Arizona 85007
HOURS OF OPERATION for the HIVE at CTEC
Mondays + Wednesday + Thursday 12pm-6pm
Tuesday + Friday 10am-4pm
First Saturday of each month 10am-2pm

* The Hive at Guadalupe South Mountain
Inside South Mountain Community College’s Guadalupe Center
9233 S Avenida del Yaqui, Guadalupe, Arizona 85283 
HOURS OF OPERATION for the HIVE at Guadalupe
Mondays + Wednesday + Thursday 12pm-6pm
Tuesday + Friday 10am-4pm
Third Saturday of each month 10am-2pm

* The Hive at EnVision Center
1310 E Apache Blvd, Tempe, Arizona 85281
HOURS OF OPERATION for the HIVE at EnVision Center
Mondays + Wednesday + Thursday 12pm-6pm
Tuesday + Friday 10am-4pm
Fourth Saturday of each month 10am-2pm

* The Hive at Chandler San Marcos
Next to San Marcos Elementary School
451 W Frye Rd, Chandler AZ 85225



"""

#if st.sidebar.button("Update Center Information"):
st.session_state.context = context_input
#    st.sidebar.success("Envision Center information updated!")

# API key input
api_key = st.secrets["APIKEY"]
#st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    # Initialize the model
    model = initialize_gemini(api_key)

    # User type selection
    st.subheader("Select Your User Type:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Kid"):
            st.session_state.user_type = "Kid"
    with col2:
        if st.button("Adult"):
            st.session_state.user_type = "Adult"
    with col3:
        if st.button("Senior"):
            st.session_state.user_type = "Senior"

    # Display selected user type
    if st.session_state.user_type:
        st.write(f"Selected User Type: {st.session_state.user_type}")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("How can I help you learn more about IDIA?"):
        if st.session_state.user_type:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get and display Gemini response
            response = get_gemini_response(model, prompt, st.session_state.user_type, st.session_state.context)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.warning("Please select a user type before asking questions.")

else:
    st.warning("Please enter your Gemini API Key to start.")

# Instructions
st.sidebar.title("How to Use")
st.sidebar.markdown("""
1. Select your user type (Kid, Adult, or Senior).
2. Ask questions about IDIA in the chat interface: About hours, programs, etc!
3. The AI will provide information based on your user type and details.

Quick Links:
* Website: https://theidia.org/

""")