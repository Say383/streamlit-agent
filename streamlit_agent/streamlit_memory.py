from typing import Optional, List
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain.schema import BaseMessage


class StreamlitMemory(ConversationBufferMemory):
    "Memory for Streamlit"
    key: str = "messages"

    def __init__(
        self,
        output_key: Optional[str] = None,
        input_key: Optional[str] = None,
        return_messages: bool = False,
        human_prefix: str = "Human",
        ai_prefix: str = "AI",
        memory_key: str = "chat_history",
        key: str = "messages",
    ):
        if key not in st.session_state:
            st.session_state[key] = ChatMessageHistory()

        super().__init__(
            chat_memory=st.session_state[key],
            output_key=output_key,
            input_key=input_key,
            return_messages=return_messages,
            human_prefix=human_prefix,
            ai_prefix=ai_prefix,
            memory_key=memory_key,
        )

    @property
    def messages(self) -> List[BaseMessage]:
        return self.chat_memory.messages

    def reset_messages(self, msgs: List[BaseMessage]) -> None:
        self.clear()
        for msg in msgs:
            self.chat_memory.add_message(msg)
