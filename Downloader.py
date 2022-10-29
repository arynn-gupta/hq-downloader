import streamlit as st
from humanfriendly import format_timespan, format_size
import requests, validators, time, os
from lib.utils import styling, generate_random_id

def add_columns():
    st.session_state['input_fields'].append("")

def remove_columns():
    if len(st.session_state['input_fields']) > 1:
        st.session_state['input_fields'].pop()

def update_value(i, key):
    st.session_state['input_fields'][i] = st.session_state[key]

def main():
    styling()
    
    st.title("HQ Downloader")
    st.subheader("File URL")

    if 'input_fields' not in st.session_state:
        st.session_state['input_fields'] = []
        add_columns()

    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    for i in range(0, len(st.session_state['input_fields'])):
        key=generate_random_id()
        st.text_input(f"Link {i+1}", value=st.session_state['input_fields'][i], on_change=update_value, args=(i, key), key=key)

    col1, col2, col3, col4 = st.columns(4)
    submitted = col1.button("Start Download")
    refresh = col2.button("Refresh")
    col3.button("Add", on_click = add_columns, disabled=submitted)
    col4.button("Remove", on_click = remove_columns, disabled=submitted)

    info = st.empty()

    if refresh:
        st.experimental_rerun()

    if submitted :
        
        for i in range(0, len(st.session_state['input_fields'])):
            file_url=st.session_state['input_fields'][i]

            if file_url == '':
                info.error(f"Link {i+1} is empty.")
                continue

            if not validators.url(file_url) :
                info.error(f"{file_url} is not a valid URL.")
                continue

            directory = "downloads"
            url = file_url

            localFilename = url.split('/')[-1]

            if localFilename in os.listdir(directory):
                info.error(f"{file_url} is already in downloads.")
                continue

            try:
                with open(directory + '/' + localFilename, 'wb') as f:
                    start = time.perf_counter()
                    r = requests.get(url, stream=True)
                    total_length = r.headers.get('content-length')
                    dl = 0
                    if total_length is None: # no content length header
                        f.write(r.content)
                    else:
                        for chunk in r.iter_content(1024):
                            dl += len(chunk)
                            f.write(chunk)
                            done = round((100 * dl / int(total_length)), 2)
                            output = f'''
                            Progress : {i+1}/{len(st.session_state['input_fields'])}
                            =======================
                            Speed : {format_size(dl//(time.perf_counter() - start))}ps \n
                            Percentage : {done}% \n
                            Time Elapsed: {format_timespan(time.perf_counter() - start)} \n
                            Downloaded : {format_size(dl)} / {format_size(int(total_length))}'''
                            info.success(output)
            except Exception as e:
                # debug
                # st.write(e)
                info.error(f"Can't Download {file_url} 🥲")
                continue
        
if __name__ == '__main__':
    main()