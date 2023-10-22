import streamlit as st


def main():
    pass

if __name__ == "__main__":
    if not st.session_state["authentication_status"]:
        st.warning('Please login first')
    else:
        main()