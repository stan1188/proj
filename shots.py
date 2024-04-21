import streamlit as st
import pandas as pd
from mplsoccer import (VerticalPitch, Pitch,
                       FontManager, arrowhead_marker, Sbopen)
from statsbombpy import sb

fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
'rubikmonoone/RubikMonoOne-Regular.ttf')

robotto_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')

def get_shots(df_event):
    df = df_event[df_event['type_name'] == 'Shot']#[['team_name','player_name','sub_type_name','outcome_name','type_name','shot_statsbomb_xg','x','y','end_x','end_y']]
    teams = df['team_name'].unique().tolist()
    pitch = VerticalPitch(goal_type='box',half=True)

    for i , team in enumerate(teams):
        shots = df[df['team_name'] == team]
        fig, ax = pitch.draw(figsize=(8, 8))
        df2 = df[(df['period'] < 5) & (df['team_name'] == team) & (df['outcome_name'].isin(['Goal', 'Saved', 'Off T', 'Wayward', 'Blocked']))]
        stats = df2['outcome_name'].value_counts().reindex(['Goal', 'Saved', 'Off T', 'Wayward', 'Blocked']).fillna(0).astype(int)
        print(stats)
        for index, shot in shots.iterrows():
            shot_scatter = pitch.scatter(shot['x'], shot['y'],
                        s=(shot['shot_statsbomb_xg'] * 1200) + 100,
                            edgecolors='black',
                            color='None',
                            marker='o',
                            alpha= 1 if shot['outcome_name'] == 'Goal' else 0.6,   
                            ax=ax)   
            
            pitch.lines(shot['x'], shot['y'], shot['end_x'], shot['end_y'],
                        linewidth=0.4,  
                        linestyle='-',
                        color='black',
                        alpha=0.5,
                        ax=ax)
           
        pitch.text(75, 20, f'Shots:{stats.sum()}', ax=ax, va='top', ha='center', color='black', zorder=5, fontsize=15, alpha=0.6, fontproperties=fm_rubik.prop) 
        pitch.text(75, 40, f'On:{stats["Saved"] + stats["Goal"]}', ax=ax, va='top', ha='center', color='black', zorder=5, fontsize=15, alpha=0.6, fontproperties=fm_rubik.prop)
        pitch.text(75, 60, f'Off: {stats["Off T"] + stats["Wayward"]}', ax=ax, va='top', ha='center', color='black', zorder=5, fontsize=15, alpha=0.6, fontproperties=fm_rubik.prop)

        #pitch.text(85,50, f'{stats['Off T'] + stats['Wayward']}', ax=ax, va='top', ha='center', color='black', zorder=5, fontsize=15, alpha=0.6, fontproperties=fm_rubik.prop)
        pitch.text(65,40, shots['team_name'].iloc[0], ax=ax, va='top', ha='center', color='black', zorder=5, fontsize=15, alpha=0.6, fontproperties=fm_rubik.prop)
        
        st.pyplot(fig)

