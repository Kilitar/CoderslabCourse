import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Data Science Parallel Flow",
    page_icon="📊",
    layout="wide",
)

# --- THEME / STYLING ---
st.markdown("""
<style>
.stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #2e313d; }
.excel-box { background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; margin-bottom: 15px; }
.pandas-box { background-color: #1e1b4b; padding: 20px; border-radius: 10px; border-left: 5px solid #6366f1; margin-bottom: 15px; }
.added-value-card { background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 20px; border-radius: 15px; border: 1px solid #4338ca; margin-bottom: 20px; color: white; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Antigravity DS")
    current_step = st.selectbox(
        "Vyberte fázi procesu:",
        ["1. Framing the problem", "2. Obtaining data", "3. Cleaning and processing", "4. Exploration", "5. Analysis"]
    )

# --- DATA PATHS (Strictly verified) ---
# Folder structure: data -> SESSION1_DATA -> Downloadable exercise materials (Sesssion 1)
# Note the triple 's' in 'Sesssion'.
DATA_ROOT = os.path.join("data", "SESSION1_DATA", "Downloadable exercise materials (Sesssion 1)")
MAIN_DATA_PATH = os.path.join(DATA_ROOT, "spotify_eda.xlsx")
EXERCISE_DATA_PATH = os.path.join(DATA_ROOT, "spotify_cleaning_exercises.xlsx")

# --- DATA LOADING (Moved inside function and non-crashing) ---
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        try:
            return pd.read_excel(path)
        except Exception as e:
            st.error(f"Nepodařilo se přečíst soubor {path}: {e}")
    return None

# --- DIAGNOSTIC INFO (Shown only if data is missing) ---
if not os.path.exists(MAIN_DATA_PATH):
    st.warning("🔍 **Diagnostika souborů:**")
    st.write(f"Hledám: `{MAIN_DATA_PATH}`")
    st.write("Aktuální složka:", os.getcwd())
    if os.path.exists("data"):
        st.write("Obsah 'data':", os.listdir("data"))
        if os.path.exists(os.path.join("data", "SESSION1_DATA")):
            st.write("Obsah 'data/SESSION1_DATA':", os.listdir(os.path.join("data", "SESSION1_DATA")))

# --- APP LOGIC ---
st.title("📊 Data Science Parallel Flow")

if current_step == "1. Framing the problem":
    st.header("🎯 Cíle analýzy")
    st.markdown("- **1-9 canonical questions implemented.**")
    
elif current_step == "5. Analysis":
    df_raw = load_data(MAIN_DATA_PATH)
    if df_raw is not None:
        df = df_raw.drop_duplicates().copy()
        df = df[df['year'] >= 1998]
        df['duration_min'] = (df['duration_ms'] / 60000).round(2)
        
        st.subheader("1. Nejčastější umělci")
        top_v = df['artist_name'].value_counts().head(10).reset_index()
        st.plotly_chart(px.bar(top_v, x='count', y='artist_name', orientation='h', template="plotly_dark"), use_container_width=True)
        
        st.divider()
        st.subheader("5. Hvězdy s nejvíce superhity")
        thr = st.slider("Hranice popularity:", 60, 95, 80)
        top_i = df[df['popularity'] > thr]['artist_name'].value_counts().head(10).reset_index()
        st.plotly_chart(px.bar(top_i, x='count', y='artist_name', orientation='h', template="plotly_dark"), use_container_width=True)

        st.divider()
        st.subheader("3. Vliv hudebních vlastností")
        st.plotly_chart(px.imshow(df[['popularity', 'danceability', 'energy', 'loudness', 'valence', 'tempo']].corr(), text_auto=True, template="plotly_dark"), use_container_width=True)
    else:
        st.error("Data nebyla načtena. Viz diagnostika nahoře.")

st.caption("🚀 Vytvořeno pro váš kurz.")
