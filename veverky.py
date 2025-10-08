import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Central Park Squirrel Explorer", page_icon="🐿️", layout="wide")

# Title and description
st.title("🐿️ Central Park Squirrel Census 2018")
st.markdown("Explore data from the 2018 Central Park Squirrel Census - a fascinating dataset of 3,023 squirrel observations!")

# Load data from CSV file
@st.cache_data
def load_data():
    # Read data from the mapped CSV file
    file_path = "/data/in/tables/Veverky-2018.csv"
    df = pd.read_csv(file_path)
    
    # Convert coordinates to numeric - handle both string and numeric formats
    df['X'] = pd.to_numeric(df['X'].astype(str).str.replace(',', '.'), errors='coerce')
    df['Y'] = pd.to_numeric(df['Y'].astype(str).str.replace(',', '.'), errors='coerce')
    
    # Convert boolean columns
    bool_cols = ['Running', 'Chasing', 'Climbing', 'Eating', 'Foraging', 'Kuks', 'Quaas', 
                 'Moans', 'Tail_flags', 'Tail_twitches', 'Approaches', 'Indifferent', 'Runs_from']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: True if str(x).upper() == 'TRUE' else False)
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Fur color filter
fur_colors = df['Primary_Fur_Color'].dropna().unique().tolist()
selected_colors = st.sidebar.multiselect("Fur Color", fur_colors, default=fur_colors)

# Age filter
ages = df['Age'].dropna().unique().tolist()
selected_ages = st.sidebar.multiselect("Age", ages, default=ages)

# Shift filter
shifts = df['Shift'].dropna().unique().tolist()
selected_shifts = st.sidebar.multiselect("Observation Shift", shifts, default=shifts)

# Apply filters
filtered_df = df.copy()
if selected_colors:
    filtered_df = filtered_df[filtered_df['Primary_Fur_Color'].isin(selected_colors)]
if selected_ages:
    filtered_df = filtered_df[filtered_df['Age'].isin(selected_ages)]
if selected_shifts:
    filtered_df = filtered_df[filtered_df['Shift'].isin(selected_shifts)]

# Key metrics
st.header("📊 Key Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Squirrels", len(filtered_df))
with col2:
    adult_count = len(filtered_df[filtered_df['Age'] == 'Adult'])
    st.metric("Adults", adult_count)
with col3:
    gray_count = len(filtered_df[filtered_df['Primary_Fur_Color'] == 'Gray'])
    st.metric("Gray Squirrels", gray_count)
with col4:
    eating_count = filtered_df['Eating'].sum()
    st.metric("Eating Observed", int(eating_count))

# Map visualization
st.header("🗺️ Squirrel Locations")

map_df = filtered_df.dropna(subset=['X', 'Y'])

if len(map_df) > 0:
    fig = px.scatter_mapbox(
        map_df,
        lat="Y",
        lon="X",
        color="Primary_Fur_Color",
        hover_data=["Age", "Shift", "Location"],
        zoom=12,
        height=500,
        title="Squirrel Sightings in Central Park"
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No location data available for selected filters")

# Two column layout for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎨 Fur Color Distribution")
    color_counts = filtered_df['Primary_Fur_Color'].value_counts()
    fig = px.pie(values=color_counts.values, names=color_counts.index, 
                 title="Primary Fur Colors")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏃 Activities Observed")
    activities = ['Running', 'Chasing', 'Climbing', 'Eating', 'Foraging']
    activity_counts = [filtered_df[act].sum() for act in activities]
    fig = px.bar(x=activities, y=activity_counts, 
                 title="Squirrel Activities",
                 labels={'x': 'Activity', 'y': 'Count'})
    st.plotly_chart(fig, use_container_width=True)

# Behavior analysis
st.header("🐿️ Behavior Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔊 Vocalizations")
    vocalizations = ['Kuks', 'Quaas', 'Moans']
    vocal_counts = [filtered_df[v].sum() for v in vocalizations]
    fig = px.bar(x=vocalizations, y=vocal_counts,
                 title="Types of Vocalizations",
                 labels={'x': 'Vocalization', 'y': 'Count'},
                 color=vocalizations)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("👋 Human Interactions")
    interactions = ['Approaches', 'Indifferent', 'Runs_from']
    interaction_counts = [filtered_df[i].sum() for i in interactions]
    fig = px.bar(x=interactions, y=interaction_counts,
                 title="Squirrel Reactions to Humans",
                 labels={'x': 'Reaction', 'y': 'Count'},
                 color=interactions)
    st.plotly_chart(fig, use_container_width=True)

# Observation timing
st.header("⏰ Observation Patterns")
shift_counts = filtered_df['Shift'].value_counts()
fig = px.bar(x=shift_counts.index, y=shift_counts.values,
             title="Observations by Time of Day",
             labels={'x': 'Shift (AM/PM)', 'y': 'Number of Observations'},
             color=shift_counts.index)
st.plotly_chart(fig, use_container_width=True)

# Data table
st.header("📋 Raw Data")
st.dataframe(
    filtered_df[['Unique_Squirrel_ID', 'Age', 'Primary_Fur_Color', 'Shift', 
                 'Running', 'Climbing', 'Eating', 'Foraging']].head(100),
    use_container_width=True
)

st.markdown("---")
st.caption("Data from the 2018 Central Park Squirrel Census")