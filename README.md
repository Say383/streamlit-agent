# 🦜️🔗 LangChain 🤝 Streamlit agent examples

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/langchain-ai/streamlit-agent?quickstart=1)

This repository contains reference implementations of various LangChain agents as Streamlit apps including:

- `basic_streaming.py`: Simple streaming app with `langchain.chat_models.ChatOpenAI` ([View the app](https://langchain-streaming-example.streamlit.app/))
- `mrkl_demo.py`: An agent that replicates the [MRKL demo](https://python.langchain.com/docs/modules/agents/how_to/mrkl) ([View the app](https://langchain-mrkl.streamlit.app))
- `minimal_agent.py`: A minimal agent with search (requires setting `OPENAI_API_KEY` env to run)
- `search_and_chat.py`: A search-enabled chatbot that remembers chat history ([View the app](https://langchain-chat-search.streamlit.app/))
- `chat_with_documents.py`: Chatbot capable of answering queries by referring custom documents ([View the app](https://langchain-document-chat.streamlit.app/))
- `chat_with_sql_db.py`: Chatbot which can communicate with your database ([View the app](https://langchain-chat-sql.streamlit.app/))
- `chat_pandas_df.py`: Chatbot to ask questions about a pandas DF ([View the app](https://langchain-chat-pandas.streamlit.app/))
- `simple_feedback.py`: Add a simple LangSmith feedback integration (WIP!) ([View the app](https://langsmith-simple-feedback.streamlit.app/))

Apps feature LangChain 🤝 Streamlit integrations such as the
[Callback integration](https://python.langchain.com/docs/modules/callbacks/integrations/streamlit).

## Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```shell
# Create Python environment
$ poetry install

# Install git pre-commit hooks
$ poetry shell
$ pre-commit install
```

## Running

```shell
# Run mrkl_demo.py or another app the same way
$ streamlit run streamlit_agent/mrkl_demo.py
```

## LangSmith tracing and feedback

All the examples provided here can integrate with LangSmith automatically, as described in the [Quick Start](https://docs.smith.langchain.com/#quick-start).
Just add the following to your [`.streamlit/secrets.toml` file](https://docs.streamlit.io/library/advanced-features/secrets-management):

```toml
# .streamlit/secrets.toml

LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
LANGCHAIN_API_KEY = "<your-api-key>"
LANGCHAIN_PROJECT = "<your-project>"  # if not specified, defaults to "default"
```

You can see a simple example of gathering human feedback and linking to run information in `streamlit_agent/simple_feedback.py`.

## Contributing

We plan to add more agent and chain examples over time and improve the existing ones - PRs welcome! 🚀
