import streamlit as st
import os
from dotenv import load_dotenv
from gemini_agent import GeminiAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Gemini AI Agent Chat",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None


def setup_sidebar():
    """Setup sidebar with configuration options"""
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key section
        env_api_key = os.getenv('GOOGLE_API_KEY')
        api_key_placeholder = "API key loaded from .env" if env_api_key else "Enter your Gemini API key"

        api_key = st.text_input(
            "Google API Key",
            value=env_api_key or "",
            type="password",
            placeholder=api_key_placeholder,
            help="Get your API key from Google AI Studio"
        )

        # Model selection
        model_options = ["gemini-2.0-flash", "gemini-1.5-flash"]
        selected_model = st.selectbox("Select Model", model_options)

        # System prompt
        system_prompt = st.text_area(
            "System Prompt (Optional)",
            placeholder="Enter system instructions for the AI...",
            height=100
        )

        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            clear_chat()

        return api_key, selected_model, system_prompt


def clear_chat():
    """Clear chat history and reset agent"""
    st.session_state.messages = []
    if st.session_state.agent:
        st.session_state.agent.clear_history()
    st.session_state.agent = None
    st.rerun()


def initialize_agent(api_key: str, model_name: str):
    """Initialize Gemini agent if API key is provided"""
    if not api_key:
        return False

    os.environ['GOOGLE_API_KEY'] = api_key

    try:
        if st.session_state.agent is None:
            st.session_state.agent = GeminiAgent(model_name=model_name)
            st.sidebar.success("✅ Connected to Gemini API")
        return True
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")
        st.session_state.agent = None
        return False


def display_chat_messages():
    """Display all chat messages with token usage"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show token usage for assistant messages
            if message["role"] == "assistant" and message.get("usage_metadata"):
                usage = message["usage_metadata"]
                st.caption(f"📊 Tokens: {usage.get('input_tokens', 0)} input, "
                          f"{usage.get('output_tokens', 0)} output, "
                          f"{usage.get('total_tokens', 0)} total")


def handle_user_input(prompt: str, system_prompt: str):
    """Handle user input and generate AI response"""
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Apply system prompt only for first message
                is_first_message = len(st.session_state.messages) == 1
                response, usage_metadata = st.session_state.agent.send_message(
                    prompt,
                    system_prompt if (system_prompt and is_first_message) else None
                )

                st.markdown(response)

                # Show token usage
                if usage_metadata:
                    st.caption(f"📊 Tokens: {usage_metadata.get('input_tokens', 0)} input, "
                              f"{usage_metadata.get('output_tokens', 0)} output, "
                              f"{usage_metadata.get('total_tokens', 0)} total")

                # Save to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "usage_metadata": usage_metadata
                })

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})


def show_welcome_message():
    """Show welcome message when agent is not initialized"""
    st.warning("⚠️ Please enter your Google API key in the sidebar to start chatting.")
    st.info("""
    📝 **How to get your API key:**
    1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Create a new API key
    3. Copy and paste it in the sidebar
    """)


def main():
    """Main application logic"""
    st.title("🤖 Gemini AI Agent Chat")

    # Setup sidebar and get configuration
    api_key, selected_model, system_prompt = setup_sidebar()

    # Initialize agent
    agent_ready = initialize_agent(api_key, selected_model)

    if not agent_ready:
        show_welcome_message()
        return

    # Display chat interface
    display_chat_messages()

    # Handle user input
    if prompt := st.chat_input("What would you like to ask?"):
        handle_user_input(prompt, system_prompt)

    # Footer
    st.markdown("---")
    st.markdown(
        "🔗 **Links:** "
        "[Google AI Studio](https://makersuite.google.com/) | "
        "[Gemini API Docs](https://ai.google.dev/docs) | "
        "[Streamlit Docs](https://docs.streamlit.io/)"
    )


if __name__ == "__main__":
    main()
