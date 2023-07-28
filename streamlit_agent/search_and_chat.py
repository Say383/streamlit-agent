from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.callbacks import StreamlitCallbackHandler
from langchain import OpenAI, LLMChain
from langchain.schema import AIMessage
from langchain.tools import DuckDuckGoSearchRun
import streamlit as st
from streamlit_memory import StreamlitMemory

st.set_page_config(page_title="LangChain: Chat with search", page_icon="🦜")
st.title("🦜 LangChain: Chat with search")

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!

{chat_history}
Question: {input}
{agent_scratchpad}"""
tools = [DuckDuckGoSearchRun(name="Search")]

prompt_tpl = ZeroShotAgent.create_prompt(
    tools=tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
memory = StreamlitMemory()

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if len(memory.messages) == 0 or st.sidebar.button("Reset chat history"):
    memory.clear()
    memory.add_message(AIMessage(content="How can I help you?"))

for msg in memory.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.chat_message("human").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = OpenAI(openai_api_key=openai_api_key, streaming=True)
    llm_chain = LLMChain(llm=llm, prompt=prompt_tpl)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
    search_agent = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory,
        handle_parsing_errors=True,
    )

    with st.chat_message("ai"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(prompt, callbacks=[st_cb])
        st.write(response)
