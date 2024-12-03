import streamlit as st
from streamlit_chat import message
from langchain.schema import HumanMessage, AIMessage
from agent import agent, history

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = history  # Initialize as a list of messages
if "agent" not in st.session_state:
    st.session_state.agent = agent  # Load the agent from agent.py
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

# Streamlit UI
st.title("Luxembourg Travel Guide 🇱🇺")
st.divider()
st.subheader("Letz explore!")

# Input box for user message
user_input = st.chat_input("Ask me anything about Luxembourg...")

# Handle user input
if user_input:
    with st.spinner("The AI is thinking..."):
        
        print(st.session_state.history)
        
        # Add user message to history
        human_message = user_input
        st.session_state["user_prompt_history"].append(human_message)
        st.session_state.history.add_user_message(human_message)

        # Prepare the chat history for the agent
        try:
            agent_response = st.session_state.agent.invoke(st.session_state.history)
            # Add AI response to history
            ai_message = agent_response["messages"][-1].content
            st.session_state["chat_answers_history"].append(ai_message)
            st.session_state.history.add_ai_message(ai_message)
            if st.session_state["chat_answers_history"]:
                for generated_response, user_query in zip(
                    st.session_state["chat_answers_history"],
                    st.session_state["user_prompt_history"],
                ):
                    message(user_query, is_user=True)
                    message(generated_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")