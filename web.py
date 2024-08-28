import pickle
import numpy as np
import streamlit as st
import time

with open('Random Forest.pkl', 'rb') as f:
    model = pickle.load(f)

def stream_data(des):
    for word in des.split(" "):
        yield word + " "
        time.sleep(0.06)

st.markdown("<h1 style='text-align: center; color: red; text-shadow: 2px 20px 20px maroon; font-size: 60px;'>🏥 BedBridge 🏥</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: lavender;'>Fill Patient Details...</h3>", unsafe_allow_html=True)
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(90deg, #070529, black, #290505);
    background-size: 400% 400%;
    animation: gradient 8s ease infinite;
    height: 100vh;
}

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

def prepro(*x):
    x = x[0]
    x[0] = x[0]/100
    if x[1] == 'Male':
        x[1] = 1
    else:
        x[1] = 0
    c = 0
    for i in ['hypertension', 'diabetes', 'depression']:
        if i in x[2]:
            c += 1
    x[2] = c
    if x[3] == 'Mild':
        x[3] = 0
    elif x[3] == 'Moderate':
        x[3] = 1
    else:
        x[3] = 2
    if x[4] == 'Normal':
        x[4] = 2
    elif x[4] == 'ICU':
        x[4] = 1
    else:
        x[4] = 0
    if x[5]:
        x[5] = 1
    else:
        x[5] = 0
    if x[6] == 'General':
        x[6] = 1
    elif x[6] == 'Neuro':
        x[6] = 2
    else:
        x[6] = 0
    return x

with st.form('Patient Form'):
    c1, c2 = st.columns(2)

    with c1:
        typ = st.selectbox('Type of disease', ['Normal', 'ICU', 'Highly Communicable'])
        sev = st.selectbox('Condition Severity', ['Mild', 'Moderate', 'Severe'])
        gen = st.radio('Gender', ['Male', 'Female'])
        emr = st.toggle('Emergency')
    with c2:
        pre = st.multiselect('Pre Existing Conditions', ['Diabetes', 'Hypertension', 'Depression'])
        dep = st.selectbox('Department', ['General', 'Neuro', 'Cardio'])
        age = st.select_slider('Age', range(1, 100))
        sub = st.form_submit_button('Check Bed Availability')
    if sub:
        y = prepro([age, gen, pre, sev, typ, emr, dep])
        st.write_stream(stream_data(f'''## A bed will be available in `{int(model.predict(np.array([y])))}` days...'''))