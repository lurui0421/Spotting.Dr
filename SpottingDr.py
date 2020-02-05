### Import packages
import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px


st.title('Spotting.Dr at NYC')

st.markdown("Spotting.Dr will help you know more about your doctor")


def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

### Get the data set 
data_load_state=st.text('Loading data...')
df = df = st.cache(pd.read_csv)("data_summary.csv")

data_load_state.text('Loading data...done!')

Speciality=st.sidebar.multiselect('You want to find specialties on?',df['Speciality'].unique())
Topics=st.sidebar.multiselect('You care about?',df["Dominant Topic"].unique())

# Filter dataframe
new_df=df[(df['Speciality'].isin(Speciality))&(df["Dominant Topic"].isin(Topics))]
new_df["Name"]=df["Name"]
# create figure using plotly express
fig = px.scatter(new_df, x ='Bayesian Adjusted Rating',y='Review Quality Index',color='Name')


st.plotly_chart(fig)
fig_1 = px.scatter(new_df, x='Number of Review',y=" Percentage of Positive Sentiment",color="Name")
st.plotly_chart(fig_1)


### Separate Data set 
pd.set_option('display.expand_frame_repr', False)
Names=st.sidebar.multiselect('Which Doctor do you want to check?',df['Name'].unique())
comment= df[(df["Dominant Topic"].isin(Topics))&(df['Name'].isin(Names))][["Comment"]].reset_index().drop(["index"],axis=1)
st.write(comment)






