import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
user_list = ["Overall"]  # Default user list

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # Fetch the different users
    user_list = df['user'].unique().tolist()
    if 'group notification' in user_list:
        user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "Overall")

selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

if st.sidebar.button("Show Analysis"):
    # Fetch number of messages
    num_messages, words, media_messages, links = helper.fetch_status(selected_user, df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("Total Messages")
        st.title(num_messages)

    with col2:
        st.header("Total Words")
        st.title(words)

    with col3:
        st.header("Media Shared")
        st.title(media_messages)

    with col4:
        st.header("Links Shared")
        st.title(links)

if selected_user == 'Overall':
    st.title('Most Busy User')
    x = helper.fetch_most_busy_users(df)  # Ensure this function returns a DataFrame or Series

    # Correct subplot creation
    fig, ax = plt.subplots()
    ax.bar(x.index, x.values)

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig)  # Display the plot in Streamlit

