from langchain.agents import AgentType, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain import OpenAI
from langchain.schema import AIMessage
from langchain.tools import DuckDuckGoSearchRun
import streamlit as st
from streamlit_memory import StreamlitMemory

st.set_page_config(page_title="LangChain: Chat with search", page_icon="🦜")
st.title("🦜 LangChain: Chat with search")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

memory = StreamlitMemory(return_messages=True, input_key="input", output_key="output")
if len(memory.messages) == 0 or st.sidebar.button("Reset chat history"):
    memory.reset_messages([AIMessage(content="How can I help you?")])

for msg in memory.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.chat_message("human").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search_agent = initialize_agent(
        tools=[DuckDuckGoSearchRun(name="Search")],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )
    with st.chat_message("ai"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent(prompt, callbacks=[st_cb])
        st.write(response)
