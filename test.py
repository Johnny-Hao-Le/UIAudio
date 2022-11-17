from minio import Minio
import pytz
from dateutil import parser
import streamlit as st
import pandas as pd


minio_client = Minio("minio-api.app.rdhasaki.com",
                     "eeFdtztKdxpi84EP", "femoa1ZSPGdWMXyTOom7goqYAE5KoJxs")






loc = []
lstlocation = minio_client.list_objects("hasaki-audio")
for location in lstlocation:
    loc.append(location.object_name.split('/')[0])
with st.sidebar:
    loc_choose = st.selectbox(
        "Chọn khu vực", loc
    )

    day = st.date_input("Chọn ngày")
    day = day.strftime("%Y/%m/%d")

    thecomputer = []
    lstcomputer = minio_client.list_objects("hasaki-audio",f"/{loc_choose}/{day}/")
    for com in lstcomputer:
        thecomputer.append(com.object_name.split('/')[4].split('/')[0])


    thecomputer = st.selectbox(
        "Chọn thiết bị",
        thecomputer
    )



def get_time(t):
    VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
    time_modified = parser.parse(t)
    return str(time_modified.astimezone(VN_TZ)).split('.')[0]

lst_mp3_name = []
lst_mp3_modified = []
lst_mp3_size = []

mp3s = minio_client.list_objects(
    "hasaki-audio", f"/{loc_choose}/{day}/{thecomputer}/")
for mp3 in mp3s:
    lst_mp3_name.append(mp3.object_name.split("/")[-1])
    lst_mp3_modified.append(get_time(str(mp3.last_modified)))
    lst_mp3_size.append(str(round(int(mp3.size)/1048576, 1))+"MB")

total = list(zip(lst_mp3_name, lst_mp3_modified, lst_mp3_size))
fields = ["name", "last_modified", "size"]
dicts_mp3 = []
for t in total:
    d = {}
    for i in range(3):
        d[fields[i]] = t[i]
    dicts_mp3.append(d)


# df = pd.DataFrame(dicts_mp3)
# st.table(df)

for x in dicts_mp3:
    name_mp3= x['name']
    name_lastmodified= x['last_modified']
    name_size= x['size']
    df = pd.DataFrame([name_mp3,name_lastmodified,name_size],index=['name', 'last_modified', 'size'])
    df = df.T
    st.table(df)
    play_mp3 = minio_client.get_object(
    "hasaki-audio", f"/{loc_choose}/{day}/{thecomputer}/{name_mp3}")
    audio_bytes = play_mp3.read()
    st.audio(audio_bytes, format='audio/mpeg')
   
    













