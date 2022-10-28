import streamlit as st
from humanfriendly import format_timespan, format_size
import requests, validators, time, os
from lib.utils import styling

def main():
    styling()

    if not os.path.exists("downloads"):
        os.mkdir("downloads")
    
    st.title("HQ Downloader")
    with st.form("my_form"):
        file_url = st.text_input("File URL", value="")
        submitted = st.form_submit_button("Start Download")
        
        info = st.empty()

        if submitted :

            if not validators.url(file_url) :
                info.error("Please input a valid URL !")
                st.stop()

            directory = "downloads"
            url = file_url

            localFilename = url.split('/')[-1]

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
                            Speed : {format_size(dl//(time.perf_counter() - start))}ps \n
                            Percentage : {done}% \n
                            Time Elapsed: {format_timespan(time.perf_counter() - start)} \n
                            Downloaded : {format_size(dl)} / {format_size(int(total_length))}'''
                            info.success(output)
            except:
                info.error("Can't Download this File 🥲")
        
if __name__ == '__main__':
    main()