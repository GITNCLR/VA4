import streamlit as st
st.set_page_config(
        page_title='VA 4',
        layout='wide',
        initial_sidebar_state="expanded",
        theme= "Light"
    )

# Mainsss
if __name__ == "__main__":
    import components.base as base
    base.main()



