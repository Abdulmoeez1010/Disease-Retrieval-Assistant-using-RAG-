# from query_handler import handle_query
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def main():
#     print("💬 Medical Assistant Chat")
#     print("Type 'exit' to quit.")
    
#     while True:
#         query = input("\n🔍 Your question: ")
#         if query.lower() in ["exit", "quit"]:
#             print("👋 Exiting. Stay healthy!")
#             break

#         print("🤖 Thinking...")
#         response = handle_query(query)
#         print("\n🧠 Answer:\n", response)

# if __name__ == "__main__":
#     main()
import streamlit as st
from query_handler import handle_query

# Set up page
st.set_page_config(page_title="🧠 Disease Retrieval Assistant", page_icon="🧬")

# Title and subtitle
st.title("🩺 Disease Retrieval Assistant")
st.markdown("Ask me anything about disease **symptoms**, **treatments**, or **medical knowledge**.")

# Input box
query = st.text_input("🔍 Enter your medical query:")

# Ask button
if st.button("Ask"):
    try:
        with st.spinner("Thinking..."):
            answer = handle_query(query)
            st.markdown("### 💡 Answer")
            st.success(answer)
    except Exception as e:
        st.error(f"Something went wrong: {e}")




