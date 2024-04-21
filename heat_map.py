import streamlit as st
from scipy.ndimage import gaussian_filter

from mplsoccer import (Pitch,  FontManager)

fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
'rubikmonoone/RubikMonoOne-Regular.ttf')

robotto_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')

def get_hm(df_event):    
    team_names = df_event['team_name'].dropna().unique().tolist()

    pitch = Pitch(line_zorder=2,
                    pitch_color='white', line_color='lightgray')
    
    fig, axs = pitch.grid(nrows=2 , axis=False,title_height=0, endnote_height=0.05)

    for i,team in enumerate(team_names):

        heat = df_event[(df_event['team_name'] == team) & (df_event['type_name'].isin(['Shot','Pass','Ball Receipt','Clearance','Interception']))][['x','y','end_x','end_y']]
        #heat = pd.concat([pd.DataFrame(zip(team_df['x'], team_df['y'])), pd.DataFrame(zip(team_df['end_x'], team_df['end_y']))])
        #heat.columns = ['x', 'y']

        bin_statistic = pitch.bin_statistic(heat['x'], heat['y'], statistic='count', bins=(30,30))
        bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'],1)
    
        pcm = pitch.heatmap(bin_statistic, ax=axs['pitch'][i], cmap='hot', edgecolors='#22312b')
        axs['pitch'][i].text(0.5, 0.5, f'{team}', horizontalalignment='center', fontproperties=fm_rubik.prop, verticalalignment='center', transform=axs['pitch'][i].transAxes, fontsize=15, color='white')
        
        bbox_props = dict(boxstyle="rarrow", fc="black")
        axs['pitch'][i].text(60,-5,100*' ', ha="center", va="center",
            size=2,bbox=bbox_props)

    st.pyplot(fig)