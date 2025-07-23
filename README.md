# 🤖 Gemini AI Agent Chat

Simple chat bot using Google Gemini API via LangChain with Streamlit interface.

## 📋 Features

- 💬 Interactive chat with Gemini AI
- 🎛️ Model selection (gemini-2.0-flash, gemini-1.5-flash)
- 🔧 Configurable system prompts
- 📊 Token usage display
- 🔐 Automatic API key loading from .env

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup API Key

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run Application

```bash
streamlit run app.py
```

Open your browser at http://localhost:8501

## 📁 Project Structure

```
├── app.py              # Main Streamlit application
├── gemini_agent.py     # Gemini API wrapper class
├── requirements.txt    # Python dependencies
├── .env               # API keys (not in git)
└── README.md          # Documentation
```

## 💡 Usage

1. Enter your API key (if not in .env)
2. Select Gemini model
3. Optionally: add system prompt
4. Start chatting with AI
5. Token usage information is displayed under each bot response

## 🔧 Technologies

- **LangChain** - Gemini API integration
- **Streamlit** - Web interface
- **Google Gemini** - Language model
- **Python-dotenv** - Environment variable management
