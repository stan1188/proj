import streamlit as st
from mplsoccer import (VerticalPitch,  FontManager, Sbopen)
from statsbombpy import sb
from scipy.ndimage import gaussian_filter
import pandas as pd

fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
'rubikmonoone/RubikMonoOne-Regular.ttf')

robotto_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')


def get_formation(selected_match_id):
    df = sb.events(match_id=selected_match_id)
    tactic = df[['team','tactics']][:2]

    pitch = VerticalPitch(goal_type='box')
    fig, ax = pitch.draw(figsize=(6, 8.72))
    i = 0
    for i, team in tactic.iterrows():
        flips = [False, True]
        dfs = []
        team_formation = team['tactics']
        for lp in team_formation['lineup']:
            
            data = {
                'tactics_formation' : str(team_formation['formation']),
                'team': team['team'],
                'player_id': lp['player']['id'],
                'player_name': lp['player']['name'],
                'position_id': lp['position']['id'],
                'position_name': lp['position']['name'],
                'jersey_number': lp['jersey_number']
            }
            df = pd.DataFrame(data, index=[0])  # Convert data to DataFrame
            dfs.append(df)
        
        formation_plot = pd.concat(dfs, ignore_index=True)
        formation = '-'.join(formation_plot['tactics_formation'].iloc[0])
        
        text_side = { "False" : [30,40,'bottom', -3, -7], "True" : [95,40,'top', 3,130]}

        ax_text = pitch.formation(str(formation), positions=formation_plot['position_id'], kind='text',
                                text=formation_plot['player_name'].str.replace(' ','\n'), half=True,flip=flips[i], fontproperties=robotto_bold.prop,
                                va=text_side[f'{flips[i]}'][2], ha='center', fontsize=6, ax=ax, zorder=10)
              
        
        ax_text = pitch.text(text_side[f'{flips[i]}'][0], text_side[f'{flips[i]}'][1], team['team'], ax=ax, va='top', ha='center', zorder=5, fontsize=30, alpha=0.2, fontproperties=fm_rubik.prop)

        ax_text = pitch.text(text_side[f'{flips[i]}'][4], text_side[f'{flips[i]}'][1], formation, ax=ax, va='top', ha='center', zorder=5, fontsize=30, alpha=1, fontproperties=fm_rubik.prop)

        ax_scatter = pitch.formation(str(formation), positions=formation_plot['position_id'], kind='scatter',
                                    c='#7CFC00', alpha=0.8, edgecolor='black', linewidth=1, s=450, half=True, flip=flips[i], xoffset = text_side[f'{flips[i]}'][3],
                                    ax=ax, zorder=8)
        
        ax_text = pitch.formation(str(formation), positions=formation_plot['position_id'], kind='text',
                                text=formation_plot['jersey_number'], half=True, flip=flips[i],  xoffset = text_side[f'{flips[i]}'][3] ,
                                va='center', ha='center', fontsize=8, ax=ax, zorder=11)
        
        i += 1
    st.pyplot(fig)