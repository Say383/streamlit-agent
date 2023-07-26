import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langsmith import Client
import streamlit as st

st.set_page_config(page_title="LangChain: Chat with search", page_icon="🦜")
st.title("🦜 LangChain: Chat with search")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
langsmith_api_key = st.sidebar.text_input("LangSmith API Key", type="password")
if "messages" not in st.session_state or st.sidebar.button("Reset conversation history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if langsmith_api_key:
    ls_client = Client(api_url="https://api.smith.langchain.com", api_key=langsmith_api_key)


def render_message(msg):
    st.write(msg["content"])
    if "run_id" in msg and langsmith_api_key:
        run_id = msg["run_id"]
        up, down, url = st.columns([1, 1, 12])
        if up.button("👍", key=f"{run_id}_up"):
            ls_client.create_feedback(run_id, "thumbs_up", score=True)
        if down.button("👎", key=f"{run_id}_down"):
            ls_client.create_feedback(run_id, "thumbs_down", score=True)
        url.markdown(f"""[View run in LangSmith]({msg["run_url"]})""")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        render_message(msg)

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search_agent = initialize_agent(
        tools=[DuckDuckGoSearchRun(name="Search")],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent(st.session_state.messages, callbacks=[st_cb], include_run_info=True)
        response_msg = {"role": "assistant", "content": response["output"]}
        if langsmith_api_key:
            response_msg["run_id"] = response["__run"].run_id
            response_msg["run_url"] = ls_client.read_run(response_msg["run_id"]).url
        st.session_state.messages.append(response_msg)
        render_message(response_msg)
