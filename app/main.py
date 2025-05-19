# Use this file to run the application

import streamlit as st
from agents_worker.interface_agent.main import AllocationEngine
import asyncio
from functools import partial

# Initialize the AllocationEngine instance
if "allocation_engine" not in st.session_state:
    st.session_state.allocation_engine = AllocationEngine()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set up the Streamlit page
st.title("Database Query Assistant")
st.write("Ask me anything about the HR database. I'll help you generate SQL queries and answer your questions.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

async def process_query(prompt):
    try:
        response = await st.session_state.allocation_engine.generate_agent_response(prompt)
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Chat input
if prompt := st.chat_input("What would you like to know about the HR database?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get agent response using AllocationEngine asynchronously
    try:
        response = asyncio.run(process_query(prompt))
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        st.error(error_message)

# Add a sidebar with information about the HR database
with st.sidebar:
    st.title("HR Database Assistant")
    st.write("""
    This assistant can help you with:
    - Generating SQL queries for the HR database
    - Finding information about employees, departments, positions, and skills
    - Understanding database relationships and structure
    
    Available tables:
    - employees
    - departments
    - positions
    - employee_skills
    - skills
    
    Just ask your question in natural language!
    """)
    
    # Add a clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()