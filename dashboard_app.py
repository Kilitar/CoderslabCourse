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
DATA_ROOT = os.path.join("data", "SESSION1_DATA", "Downloadable exercise materials (Sesssion 1)")
MAIN_DATA_PATH = os.path.join(DATA_ROOT, "spotify_eda.xlsx")
EXERCISE_DATA_PATH = os.path.join(DATA_ROOT, "spotify_cleaning_exercises.xlsx")

# --- DATA LOADING ---
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        try:
            return pd.read_excel(path)
        except Exception as e:
            st.error(f"Nepodařilo se přečíst soubor {path}: {e}")
    return None

# --- DIAGNOSTIC INFO ---
if not os.path.exists(MAIN_DATA_PATH):
    with st.expander("🔍 Diagnostika souborů (Rozbalte pro detaily)"):
        st.write(f"Hledám: `{MAIN_DATA_PATH}`")
        st.write("Aktuální složka:", os.getcwd())
        if os.path.exists("data"):
            st.write("Obsah 'data':", os.listdir("data"))
            if os.path.exists(os.path.join("data", "SESSION1_DATA")):
                st.write("Obsah 'data/SESSION1_DATA':", os.listdir(os.path.join("data", "SESSION1_DATA")))

# --- APP LOGIC ---
st.title("📊 Data Science Parallel Flow")
st.markdown(f"### Aktuální fáze: `{current_step}`")

if current_step == "1. Framing the problem":
    tab1, tab2 = st.tabs(["🚀 Official Constraints", "🎬 Added Value Ideas"])
    with tab1:
        st.header("🎯 Cíle analýzy (1-9)")
        st.markdown("""
        1. **Top Artists:** Kteří umělci mají nejvíce hitů?
        2. **Duration vs Year:** Korelace délky a roku vydání.
        3. **Popularity Drivers:** Vliv hudebních vlastností na popularitu.
        4. **Negative Artists:** Valence u top autorů.
        5. **Superstars:** Umělci s nejvíce 'superhity' (Intensity).
        6. **Tempo Evolution:** Vývoj BPM v čase.
        7. **Genre Split:** Rozdělení podle žánrů.
        8. **Yearly Count:** Počet hitů v jednotlivých letech.
        9. **Explicit Analysis:** Vývoj nevhodného obsahu.
        """)
    with tab2:
        df_raw = load_data(MAIN_DATA_PATH)
        if df_raw is not None:
            df = df_raw.drop_duplicates().copy()
            df = df[df['year'] >= 1998]
            st.markdown('<div class="added-value-card">', unsafe_allow_html=True)
            st.subheader("😢 The Sadness Paradox (Valence)")
            st.plotly_chart(px.line(df.groupby('year')['valence'].mean().reset_index(), x='year', y='valence', template="plotly_dark"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif current_step == "2. Obtaining data":
    df_raw = load_data(MAIN_DATA_PATH)
    if df_raw is not None:
        st.success(f"✅ Data načtena ({len(df_raw)} řádků).")
        st.dataframe(df_raw.head(10))

elif current_step == "3. Cleaning and processing":
    df_raw = load_data(MAIN_DATA_PATH)
    if df_raw is not None:
        df = df_raw.drop_duplicates().copy()
        st.metric("Deduplikace", len(df_raw), delta=int(len(df)-len(df_raw)))
        st.dataframe(df.head(10))

elif current_step == "5. Analysis":
    df_raw = load_data(MAIN_DATA_PATH)
    if df_raw is not None:
        df = df_raw.drop_duplicates().copy()
        df = df[df['year'] >= 1998]
        df['duration_min'] = (df['duration_ms'] / 60000).round(2)
        df['primary_genre'] = df['genre'].apply(lambda x: str(x).split(',')[0].strip())

        # 1. Top Artists
        st.subheader("1. Kteří umělci mají v seznamu nejvíce skladeb?")
        top_v = df['artist_name'].value_counts().head(10).reset_index()
        fig1 = px.bar(top_v, x='count', y='artist_name', orientation='h', color='count', template="plotly_dark")
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)

        # 2. Duration Box
        st.divider()
        st.subheader("2. Korelace mezi délkou skladby a rokem vydání")
        fig2 = px.box(df.sort_values('year'), x='year', y='duration_min', template="plotly_dark")
        fig2.update_xaxes(type='category')
        st.plotly_chart(fig2, use_container_width=True)

        # 3. Correlation Heatmap
        st.divider()
        st.subheader("3. Ovlivňují hudební vlastnosti popularitu?")
        corr = df[['popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'valence', 'tempo']].corr()
        st.plotly_chart(px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', template="plotly_dark"), use_container_width=True)

        # 4. Negative Artists
        st.divider()
        st.subheader("4. Analýza negativity u top autorů")
        top_list = df['artist_name'].value_counts().head(10).index
        neg_df = df[df['artist_name'].isin(top_list)].groupby('artist_name')['valence'].mean().reset_index().sort_values('valence')
        st.plotly_chart(px.bar(neg_df, x='valence', y='artist_name', orientation='h', color='valence', color_continuous_scale='RdYlGn', template="plotly_dark"), use_container_width=True)

        # 5. Superstars Slider
        st.divider()
        st.subheader("5. Kteří umělci mají nejvyšší počet nejpopulárnějších skladeb?")
        thr = st.slider("Hranice 'Superhitu':", 60, 95, 80)
        top_i = df[df['popularity'] > thr]['artist_name'].value_counts().head(10).reset_index()
        fig5 = px.bar(top_i, x='count', y='artist_name', orientation='h', color='count', template="plotly_dark", color_continuous_scale='Sunsetdark')
        fig5.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig5, use_container_width=True)

        # 6. Tempo Line
        st.divider()
        st.subheader("6. Změna tempa (BPM) v čase")
        st.plotly_chart(px.line(df.groupby('year')['tempo'].mean().reset_index(), x='year', y='tempo', markers=True, template="plotly_dark"), use_container_width=True)

        # 7. Genre Pie
        st.divider()
        st.subheader("7. Skladby podle žánru")
        st.plotly_chart(px.pie(df['primary_genre'].value_counts().reset_index(), values='count', names='primary_genre', template="plotly_dark", hole=0.4), use_container_width=True)

        # 8. Hits per Year
        st.divider()
        st.subheader("8. Počet hitů v jednotlivých letech")
        st.plotly_chart(px.bar(df['year'].value_counts().reset_index().sort_values('year'), x='year', y='count', template="plotly_dark"), use_container_width=True)

        # 9. Explicit
        st.divider()
        st.subheader("9. Vývoj explicitního obsahu")
        colA, colB = st.columns(2)
        colA.plotly_chart(px.pie(df['explicit'].value_counts().reset_index(), values='count', names='explicit', template="plotly_dark"), use_container_width=True)
        colB.plotly_chart(px.line(df.groupby('year')['explicit'].sum().reset_index(), x='year', y='explicit', markers=True, template="plotly_dark"), use_container_width=True)
    else:
        st.error("Data nebyla načtena. Zkontrolujte cestu k souborům.")

st.divider()
st.caption("🚀 Vytvořeno pro váš kurz.")
