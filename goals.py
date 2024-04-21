import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import (Pitch,  FontManager)
import numpy as np
from matplotlib.patches import FancyArrowPatch

fm_rubik = FontManager('https://raw.githubusercontent.com/google/fonts/main/ofl/'
'rubikmonoone/RubikMonoOne-Regular.ttf')

robotto_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')



def add_arrow(x,y,end_x,end_y,color,scale, ax):
    mid_x = (x + end_x) / 2
    mid_y = (y + end_y) / 2
    mid_arrow = FancyArrowPatch((x,y), (mid_x, mid_y), arrowstyle='-|>', mutation_scale=scale, color=color)
    ax.add_patch(mid_arrow)

def plot_goal_sq(df_event, pos_id):

    columns = ['match_id','team_name','player_name','player_id','position_id','play_pattern_name','possession','x','y','end_x', 'end_y', 'end_z', 'timestamp','sub_type_name','outcome_name','type_name']
    df_event = df_event[df_event['possession'] == pos_id][columns].reset_index(drop = True)
    df_event = df_event.sort_values(by=['timestamp', 'type_name'], ascending=[True, True]).reset_index(drop=True)
    teams = df_event['team_name'].unique()
    
    df_event = df_event[df_event['type_name'].isin(['Pass','Clearance','Carry','Shot','Goal Keeper'])]
    df_event = df_event[~df_event['outcome_name'].isin(['Lost In Play', 'In Play Danger'])]

    df_event = df_event[df_event['sub_type_name'] != 'Shot Saved']
    df_event['type_name'] = df_event['type_name'].replace('Ball Receipt', 'Carry') 

    #remove event with little movement
    threshold_distance = 4.0 
    # Function to calculate distance between two points
    def calculate_distance(x1, y1, x2, y2):
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


    df_event.loc[df_event['team_name'] == teams[0], 'x'] = abs(120 - df_event['x'])
    df_event.loc[df_event['team_name'] == teams[0], 'y'] = abs(df_event['y'] - 80)
    df_event.loc[df_event['team_name'] == teams[0], 'end_x'] = abs(120 - df_event['end_x'])
    df_event.loc[df_event['team_name'] == teams[0], 'end_y'] = abs(80 - df_event['end_y'])


    #Carry has no movement -> remove
    df_event = df_event[(df_event['type_name'] != 'Carry') | ((df_event['type_name'] == 'Carry') & (calculate_distance(df_event['x'], df_event['y'], df_event['end_x'], df_event['end_y']) > threshold_distance))]
    #Remove no movement
    df_event = df_event[~((df_event['x'] == df_event['end_x']) & (df_event['y'] == df_event['end_y']))].reset_index(drop=True)

    #last 15 events
    df_event = df_event.tail(10).reset_index(drop=True)

    df_event['original_end_x'] = df_event['end_x']
    df_event['original_end_y'] = df_event['end_y']
    df_event['end_x'] = df_event['x'].shift(-1)
    df_event['end_y'] = df_event['y'].shift(-1)
    df_event.loc[df_event['type_name'] == 'Shot', 'end_x'] = df_event['original_end_x']
    df_event.loc[df_event['type_name'] == 'Shot', 'end_y'] = df_event['original_end_y']

    df_event = df_event[(df_event['type_name'] != 'Carry') | ((df_event['type_name'] == 'Carry') & (calculate_distance(df_event['x'], df_event['y'], df_event['end_x'], df_event['end_y']) > threshold_distance))]
    
    #return df_event
    pitch = Pitch(pad_bottom=1,  pad_top=5, # pitch extends slightly below halfway line
                        #half=True,  # half of a pitch
                        goal_type='box',
                        goal_alpha=0.8)  # control the goal transparency
    fig, ax = pitch.draw(figsize=(10, 10))

    line_properties = {
        "Carry": {"color": "#58D68D", "linestyle": "--", "linewidth": 2},
        "Pass": {"color": "#3498DB", "linestyle": "-", "linewidth": 1, "comet": True},
        "Shot": {"color": "#EC7063", "comet": True, "alpha": 0.8, "zorder":70},
        "Clearance": {"color": "gray", "linestyle": "-", "linewidth": 2, "alpha": 0.5}
    }

    for index, row in df_event.iterrows():
        markers = 'D'
        color = '#00ffff'
        if row['team_name'] == teams[0]:
            markers = 'o'
            color = '#ccffcc'
        #markers
        if row['outcome_name'] == 'Saved':
            pitch.scatter(row['x'], row['y'],s=180,c=color, edgecolors='black', marker=markers,alpha=1, ax=ax, zorder=15)
            pitch.scatter(row['end_x'], row['end_y'],s=90,c='red', edgecolors='black', marker='x',alpha=1, ax=ax, zorder=30)
        else:
            pitch.scatter(row['x'], row['y'],s=180,c=color,edgecolors='black', marker=markers,alpha=1, ax=ax, zorder=15)
            
        #lines 
        if row['type_name'] in line_properties:
            properties = line_properties[row['type_name']]
            pitch.lines(row['x'], row['y'], row['end_x'], row['end_y'], ax=ax, **properties)
            if row['type_name'] == "Pass":
                add_arrow(row['x'], row['y'], row['end_x'], row['end_y'], '#3498DB', 20, ax)

        #text
        if row['type_name'] == 'Goal Keeper':
            pitch.text(row['x'] , row['y'] , 'GK', color="black", fontsize=6, va='center',ha='center' ,ax=ax,zorder=20)
        else:
            pitch.text(row['x'] , row['y'] , str(index), color="black", fontsize=7, va='center',ha='center' ,ax=ax,zorder=20)
        
        #others
        if row['outcome_name'] == 'Goal':
            pitch.scatter(row['end_x'] , row['end_y'],s=200,c='white',edgecolors='black', marker='football',alpha=1, ax=ax , zorder=50)
        if row['sub_type_name'] == 'Free Kick' or row['sub_type_name'] == 'Corner'  :
            pitch.scatter(row['x'], row['y'],s=400,c='yellow',edgecolors='black', marker='o',alpha=1, ax=ax , zorder=10, facecolors='none')



    legend_labels = {
        "Saved Goal": {"color": "red", "marker": "x"},
        "Carry": {"color": "green", "linestyle": "--"},
        "Pass": {"color": "blue", "linestyle": "-"},
        "Shot": {"color": "red", "linestyle": "-"},
        "Clearance": {"color": "gray", "linestyle": "-"},
        "Opponent": {"color": "black", "marker":"D"}
    }       



    #title text
    ax.text(60, -5, f"{df_event[df_event['outcome_name'] == 'Goal']['team_name'].values[0]}", fontsize=15, fontproperties=fm_rubik.prop, va='center', ha='center')
    ax.text(60, -2, f"{df_event[df_event['outcome_name'] == 'Goal']['player_name'].values[0]}", fontsize=12, alpha=0.9, color='gray' ,fontproperties=fm_rubik.prop,va='center', ha='center')

    # Plot the legend
    legend_elements = []
    for label, props in legend_labels.items():
        legend_elements.append(plt.Line2D([0], [0], marker=props.get("marker", None), color=props.get("color", ''), linewidth=2, linestyle=props.get("linestyle", ''), label=label))

    # Add legend to the plot
    ax.legend(handles=legend_elements, loc='lower right',ncol=len(legend_labels),frameon=False)
    st.pyplot(fig)