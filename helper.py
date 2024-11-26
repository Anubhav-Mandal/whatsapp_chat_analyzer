from urlextract import URLExtract
extract = URLExtract()
def fetch_status(selected_user, df):
    if selected_user == 'Overall':
        # 1. Fetch the number of messages
        num_messages = df.shape[0]
        # 2. Number of words
        words = []
        for message in df['messages']:
            words.extend(message.split())
            media_messages = df[df['messages'] =='<Media omitted>\n'].shape[0]

        links = []
        for message in df['messages']:
            links.extend(extract.find_urls(message))
        return num_messages,len(words),media_messages,len(links)# Total number of rows (all messages)
    else:
        # Filter rows for the selected user
        new_df = df[df['user'] == selected_user]
        new_messages = new_df.shape[0]
        words = []
        for message in new_df['messages']:
            words.extend(message.split())
            media_messages = new_df[new_df['messages'] =='<Media omitted>\n'].shape[0]

        links = []
        for message in new_df['messages']:
            links.extend(extract.find_urls(message))
        return new_messages,len(words),media_messages,len(links)


def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    return x
