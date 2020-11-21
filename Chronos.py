
import streamlit as st
import numpy as np 
import pandas as pd

import time as t

import datetime as dt
from datetime import time
from datetime import date

st.write(
    """
    # All-in-scheduler (name tbd) 

    ### Scheduling meetings has ***never*** been this easy
    """
)

st.write("")

name = st.text_input("What should we call you?", value = "Harry Potter")

st.write("")

random = st.date_input ("Select a date:", date(2020,1,1))

st.write("")

diff = 5
start = st.slider("Select a time range: ",min_value = time(0,0), max_value= time(11,59),value = (time(5,30), time(9,45)), step = dt.timedelta(minutes=diff), format = "hh:mm")
ampm = st.radio("", options = ("AM", "PM"))

if ampm == "AM":
    start = (int(str(start[0].hour).zfill(2) + str(start[0].minute).zfill(2)),int(str(start[1].hour).zfill(2) + str(start[1].minute).zfill(2)))
else:
    start = (int(str(start[0].hour+12).zfill(2) + str(start[0].minute).zfill(2)),int(str(start[1].hour+12).zfill(2) + str(start[1].minute).zfill(2)))

#st.write(start)

st.write("")

npeople = st.number_input("How many people do you need to accommodate?", value = 25)

st.write("")

room_pref = st.selectbox("Which room would you prefer to conduct your meeting in? (Optional)", options = ("I don't have a preference", "Room 1", "Room 2", "Room 3", "Room 4", "Room 5"))

st.write("")
covid = st.checkbox("Take social distancing norms into consideration", value = True)

check = st.button("Book now!")
st.write("")
##########################################################################################################################
#BACKEND

if check:
    l=[('Room 1',50), ('Room 2', 80), ('Room 3', 30), ('Room 4', 50), ('Room 5', 100)]

    if covid:
        npeople *= 2
    meetsched={} #record dict for all meetings
    for i in l:
        meetsched[i[0]]=[]

    meetsched['Room 3'].append((500, 600, 'Palaash'))

    #There is a room preference
    if room_pref != "I don't have a preference":
        c=l[[i[0] for i in l].index(room_pref)][1]  #Capacity of preferred room
        
        if c<npeople:
            if covid:
                st.error("Sorry! Your preferred room does not have enough space to host " + str(int(npeople/2)) + " people with social distancing measures implemented properly.")
            else:
                st.error("Sorry! Your preferred room does not have enough space to host " + str(npeople) + " people.")
        else:

            if len(meetsched[room_pref]) == 0:
                st.success("Meeting succesfully scheduled in " + room_pref + " for the given time interval!")
                meetsched[room_pref].append((start[0],start[1],name))
            else:
                p =0
                
                for i in meetsched[room_pref]:
                    if (start[0]-i[0]>0 and start[0]-i[1]<0) or (start[1]-i[0]>0 and start[1]-i[1]<0):
                        p=1
                        break
                
                if p==0:
                    st.success("Meeting succesfully scheduled in " + room_pref + " for the given time interval!")
                    st.balloons()
                else :
                    st.error ("This room is occupied during the mentioned time interval.")
    
    #There is no preferred room
    else:
        available = []
        capa=[i[0] for i in l if npeople>=i[1]-20 and npeople<=i[1]] #20 ka buffer, rethink
        for j in capa:
            m=meetsched.get(j)
            p=0
            for tup in m:
                if (start[0]-tup[0]>0 and start[0]-tup[1]<0) or (start[1]-tup[0]>0 and start[1]-tup[1]<0):
                    p=1
                    break
            if p==0:
                available.append(j)
        meetsched[available[0]].append((start[0], start[1], name))
        st.success ("Meeting successfully scheduled in " + available[0] + " for the given time interval!")
        st.balloons()