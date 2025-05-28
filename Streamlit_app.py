# # from query_handler import handle_query
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # def main():
# #     print("💬 Medical Assistant Chat")
# #     print("Type 'exit' to quit.")
    
# #     while True:
# #         query = input("\n🔍 Your question: ")
# #         if query.lower() in ["exit", "quit"]:
# #             print("👋 Exiting. Stay healthy!")
# #             break

# #         print("🤖 Thinking...")
# #         response = handle_query(query)
# #         print("\n🧠 Answer:\n", response)

# # if __name__ == "__main__":
# #     main()
# import streamlit as st
# from query_handler import handle_query

# # Set up page
# st.set_page_config(page_title="🧠 Disease Retrieval Assistant", page_icon="🧬")

# # Title and subtitle
# st.title("🩺 Disease Retrieval Assistant")
# st.markdown("Ask me anything about disease **symptoms**, **treatments**, or **medical knowledge**.")

# # Input box
# query = st.text_input("🔍 Enter your medical query:")

# # Ask button
# if st.button("Ask"):
#     try:
#         with st.spinner("Thinking..."):
#             answer = handle_query(query)
#             st.markdown("### 💡 Answer")
#             st.success(answer)
#     except Exception as e:
#         st.error(f"Something went wrong: {e}")


import streamlit as st
from query_handler import handle_query

# --- Streamlit Page Config ---
st.set_page_config(page_title="Medical Assistant", layout="centered")
st.title("🩺 AI Medical Assistant")
st.markdown("Ask any health-related question, and get an answer powered by AI!")

# --- Input Field ---
user_query = st.text_input("❓ Ask your question here:")

# --- Process on Button Click ---
if st.button("Ask"):
    if user_query.strip():
        try:
            # Get intent and answer from the handler
            intent, answer = handle_query(user_query)

            # --- Show Results ---
            st.markdown(f"### 🔍 Detected Intent: `{intent}`")
            st.markdown("### 💬 Answer:")
            st.write(answer)

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
    else:
        st.warning("Please enter a query.")


