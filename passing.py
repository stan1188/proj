import streamlit as st
import pandas as pd
from mplsoccer import (VerticalPitch, Pitch,
                       FontManager, arrowhead_marker, Sbopen)
from statsbombpy import sb
import matplotlib.pyplot as plt

fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
'rubikmonoone/RubikMonoOne-Regular.ttf')

robotto_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')



def get_pass():
    parser = Sbopen()
    df, related, freeze, tactics = parser.event(3869685)
    passes = df.loc[df['type_name'] == 'Carry']
    pitch = Pitch(line_color = "black")
    fig, ax = pitch.draw(figsize=(10, 7))

    for i,thepass in passes.iterrows():
        #if pass made by Lucy Bronze
        if thepass['player_name']=='Lionel Andrés Messi Cuccittini':
            x=thepass['x']
            y=thepass['y']
            #plot circle
            passCircle=plt.Circle((x,y),2,color="blue")
            passCircle.set_alpha(.2)
            ax.add_patch(passCircle)
            dx=thepass['end_x']-x
            dy=thepass['end_y']-y
            #plot arrow
            passArrow=plt.Arrow(x,y,dx,dy,width=3,color="blue")
            ax.add_patch(passArrow)

    ax.set_title("Lucy Bronze passes against Sweden", fontsize = 24)
    fig.set_size_inches(10, 7)
    st.pyplot(fig)