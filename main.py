import streamlit as st

st.set_page_config(
        page_title='VA 4',
        layout='wide',
        initial_sidebar_state="expanded",
        menu_items={
                    'Get Help': None,
                    'Report a bug': None,
                    'About': None
        }
    )

# Mainsss
if __name__ == "__main__":
    import components.base as base
    base.main()

