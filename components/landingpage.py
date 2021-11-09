import streamlit as st
#import components.filename1
#import components.filename2


def main():



    st.markdown("***")
    col1, col2, col3 = st.columns([4, 1,1])
    with col1: st.title("VA 4 dashboard")
    with col2:
        st.image("assets/amsterdam.png", width=200)
    with col3:
        st.image("assets/denhaag.png", width=200)
    st.markdown("***")
    col1, col2 = st.columns([2, 1])
    with col2:
        st.image("assets/bomen.jpg")


    with col1:
        #st.title("VA 4 dashboard")
        #st.markdown("***")
        st.markdown("*Welkom bij het VA4 Dashboard van Team 1*")
        st.header("Test")
        st.subheader("test")
        st.markdown("*Referenties: https://github.com/GITNCLR/VA4 *")
        st.markdown("*italic*")

    st.markdown("***")
    #components.filename1.main()
    #components.filename2.main()

