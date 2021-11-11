import streamlit as st
import inspect

def show_with_options(func, text=''):
    import components.base as base
    if (text != ''):
        st.subheader(text)
    if base.showPlots: func()
    if base.showCode: st.code(inspect.getsource(func))