#!/usr/bin/env python

import streamlit as st

from db_scripts.upload_data import get_nearest_neighbor
from llm_logic import get_response


# Streamlit application starts here
def main():
    # Title of the application
    st.title(
        "History buffbut - an LLM Chatbot augmented with Wikipedia history knowledge"
    )

    # Input from the user
    user_query = st.text_input("Ask a question about a notable historical event:")
    if st.button("Process Query"):
        # Check if the query is not empty
        if user_query:
            # Call the function to process the query
            context = get_nearest_neighbor(user_query)
            result = get_response(user_query, context)
            # Display the result
            st.write(result)
        else:
            # Display a message if the user tries to process an empty query
            st.warning("Please enter a query to process.")


if __name__ == "__main__":
    main()
