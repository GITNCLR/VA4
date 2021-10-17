import streamlit as st

st.set_page_config(
        page_title='VA 4',
        layout='wide',
        initial_sidebar_state="expanded"
    )

CURRENT_THEME = "blue"
IS_DARK_THEME = True
EXPANDER_TEXT = """
    This is a custom theme. You can enable it by copying the following code
    to `.streamlit/config.toml`:
    ```python
    [theme]
    primaryColor = "#E694FF"
    backgroundColor = "#00172B"
    secondaryBackgroundColor = "#0083B8"
    textColor = "#C6CDD4"
    font = "sans-serif"
    ```
    """

# Mainsss
if __name__ == "__main__":
    import components.base as base
    base.main()



