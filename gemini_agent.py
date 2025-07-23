import os
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class GeminiAgent:
    """Simple AI Agent using LangChain's ChatGoogleGenerativeAI"""

    def __init__(self, model_name: Optional[str] = None, temperature: float = 0.7):
        """Initialize the Gemini agent with API key and model configuration"""
        load_dotenv()

        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        self.model_name = model_name or 'gemini-2.0-flash'
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=temperature,
            max_retries=2,
        )
        self.chat_history: List[Dict[str, str]] = []

    def send_message(self, message: str, system_prompt: Optional[str] = None) -> Tuple[str, Dict]:
        """Send message to Gemini and return response with token usage"""
        try:
            messages = self._build_message_history(message, system_prompt)
            response = self.llm.invoke(messages)

            self._update_chat_history(message, response.content)
            return response.content, response.usage_metadata or {}

        except Exception as e:
            return f"Error: {str(e)}", {}

    def _build_message_history(self, current_message: str, system_prompt: Optional[str] = None) -> List:
        """Build the complete message history for the current conversation"""
        messages = []

        # Add system prompt only for the first message
        if system_prompt and not self.chat_history:
            messages.append(SystemMessage(content=system_prompt))

        # Add conversation history
        for msg in self.chat_history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))

        # Add current user message
        messages.append(HumanMessage(content=current_message))
        return messages

    def _update_chat_history(self, user_message: str, assistant_response: str) -> None:
        """Update the internal chat history with new messages"""
        self.chat_history.extend([
            {'role': 'user', 'content': user_message},
            {'role': 'assistant', 'content': assistant_response}
        ])

    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.chat_history.clear()

    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the current chat history"""
        return self.chat_history.copy()
