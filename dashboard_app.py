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
    initial_sidebar_state="expanded",
)

# --- THEME / STYLING ---
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.stMetric {
    background-color: #1a1c24;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #2e313d;
}
.excel-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #10b981;
    margin-bottom: 15px;
}
.pandas-box {
    background-color: #1e1b4b;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #6366f1;
    margin-bottom: 15px;
}
.added-value-card {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #4338ca;
    margin-bottom: 20px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Antigravity DS")
    st.info("Tento dashboard kopíruje váš postup v Excelu pomocí Pythonu.")
    
    st.subheader("📍 Aktuální krok")
    current_step = st.selectbox(
        "Vyberte fázi procesu:",
        ["1. Framing the problem", "2. Obtaining data", "3. Cleaning and processing", "4. Exploration", "5. Analysis"]
    )
    
    st.divider()
    
# --- DATA PATHS (Robust for Linux/Windows) ---
# Note: "Sesssion" contains triple 's' as per local disk structure.
DATA_ROOT = os.path.join("data", "SESSION1_DATA", "Downloadable exercise materials (Sesssion 1)")
MAIN_DATA_PATH = os.path.join(DATA_ROOT, "spotify_eda.xlsx")
EXERCISE_DATA_PATH = os.path.join(DATA_ROOT, "spotify_cleaning_exercises.xlsx")

# --- DIAGNOSTIC HEADER ---
if not os.path.exists(MAIN_DATA_PATH):
    st.error(f"⚠️ Soubor nebyl nalezen na cestě: `{MAIN_DATA_PATH}`")
    st.write("Obsah aktuálního adresáře (pwd):", os.getcwd())
    if os.path.exists("data"):
        st.write("Složka 'data' nalezena. Obsah:")
        st.write(os.listdir("data"))
    else:
        st.error("Složka 'data' nebyla nalezena v rootu projektu!")

# --- DATA LOADING & ANALYTICS ---
@st.cache_data
def load_and_analyze_data():
    try:
        if os.path.exists(MAIN_DATA_PATH):
            df_raw = pd.read_excel(MAIN_DATA_PATH)
            df = df_raw.drop_duplicates().copy()
            
            # Cleaning & Features (Filtering Roman Empire data)
            df = df[df['year'] >= 1998].copy()
            
            df['duration_min'] = (df['duration_ms'] / 60000).round(2)
            df['primary_genre'] = df['genre'].apply(lambda x: str(x).split(',')[0].strip())
            df['year_str'] = df['year'].astype(str)
            
            return df_raw, df
        return None, None
    except Exception as e:
        st.error(f"❌ Chyba při načítání Excelu: {e}")
        return None, None

df_raw, df = load_and_analyze_data()

# --- MAIN CONTENT ---
st.title("📊 Data Science Parallel Flow")
st.markdown(f"### Aktuální fáze: `{current_step}`")

if current_step == "1. Framing the problem":
    tab1, tab2 = st.tabs(["🚀 Official Constraints", "🎬 Added Value Ideas"])
    
    with tab1:
        st.header("🎯 Cíle analýzy (Official Requirements)")
        st.markdown("""
        1. **Top Artists:** Kteří umělci mají v seznamu nejvíce skladeb?
        2. **Duration vs Year:** Existuje korelace mezi délkou a rokem vydání?
        3. **Popularity Drivers:** Ovlivňují vlastnosti jako energy nebo loudness popularitu?
        4. **Negative Artists:** Kteří top umělci tvoří převážně negativní skladby?
        5. **Superstars:** Kteří umělci mají nejvíce skladeb s vysokou popularitou?
        6. **Tempo Evolution:** Mění se tempo skladeb v čase?
        7. **Genre Split:** Rozdělení skladeb podle žánrů.
        8. **Yearly Count:** Rozdělení skladeb podle let.
        9. **Explicit Analysis:** Analýza nevhodného obsahu v průběhu let.
        """)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="excel-box"><b>📗 Excel Approach:</b><br>Zápis cílů do prvního listu, definice rozsahu.</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="pandas-box"><b>🐼 Pandas Approach:</b><br>Komentování kódu, definování hlaviček v Jupyteru.</div>', unsafe_allow_html=True)

    with tab2:
        st.header("💡 Naše přidaná hodnota")
        if df is not None:
            # TREND 1: Sadness Paradox
            st.markdown('<div class="added-value-card">', unsafe_allow_html=True)
            st.subheader("😢 The Sadness Paradox (Záhada smutku)")
            trend_valence = df.groupby('year')['valence'].mean().reset_index()
            fig_valence = px.line(trend_valence, x='year', y='valence', title="Trend nálady v čase")
            fig_valence.update_layout(yaxis_range=[0.4, 0.7], template="plotly_dark")
            st.plotly_chart(fig_valence, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # TREND 2: Loudness VS Popularity
            st.markdown('<div class="added-value-card">', unsafe_allow_html=True)
            st.subheader("🔊 The Loudness War (Válka o hlasitost)")
            fig_loud = px.scatter(df, x='loudness', y='popularity', color='popularity', template="plotly_dark")
            st.plotly_chart(fig_loud, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif current_step == "2. Obtaining data":
    if df_raw is not None:
        st.success(f"✅ Data úspěšně načtena ({len(df_raw)} řádků).")
        st.dataframe(df_raw.head(10))
    else:
        st.warning("⚠️ Data nejsou k dispozici. Zkontrolujte diagnostické hlášení nahoře.")

elif current_step == "3. Cleaning and processing":
    st.header("🧹 Čištění a zpracování")
    view_type = st.radio("Vyberte dataset:", ["Hlavní analýza", "Cleaning Exercise 1"])
    if view_type == "Hlavní analýza":
        if df_raw is not None and df is not None:
            st.metric("Snížení počtu řádků (Deduplikace)", len(df_raw), delta=int(len(df)-len(df_raw)))
            st.dataframe(df[['artist_name', 'song', 'duration_min', 'primary_genre']].head(10))
    else:
        try:
            if os.path.exists(EXERCISE_DATA_PATH):
                df_ex = pd.read_excel(EXERCISE_DATA_PATH, sheet_name='songs')
                st.write("📋 **Vyčištěná data (Exercise 1):**")
                st.dataframe(df_ex.head(15).style.format({'instrumentalness': '{:.6f}'}))
        except Exception as e:
            st.error(f"Chyba při načítání cvičení: {e}")

elif current_step == "5. Analysis":
    st.header("📈 Finální analýza (Dle zadání 1-9)")
    
    if df is not None:
        # Question 1: Total Hits
        st.subheader("1. Kteří umělci mají nejvíce hitů?")
        top_v = df['artist_name'].value_counts().head(10).reset_index()
        fig1 = px.bar(top_v, x='count', y='artist_name', orientation='h', template="plotly_dark")
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)

        # Question 2: Duration
        st.divider()
        st.subheader("2. Korelace délky skladeb a let")
        fig2 = px.box(df.sort_values('year'), x='year', y='duration_min', template="plotly_dark")
        fig2.update_xaxes(type='category')
        st.plotly_chart(fig2, use_container_width=True)

        # Question 3: Features vs Pop
        st.divider()
        st.subheader("3. Vliv hudebních vlastností na popularitu")
        corr = df[['popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo']].corr()
        fig3 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)

        # Question 5: Superstars
        st.divider()
        st.subheader("5. Hvězdy s nejvíce superhity")
        thr = st.slider("Hranice popularity:", 60, 95, 80)
        top_i = df[df['popularity'] > thr]['artist_name'].value_counts().head(10).reset_index()
        fig5 = px.bar(top_i, x='count', y='artist_name', orientation='h', template="plotly_dark", color_continuous_scale='Sunsetdark')
        fig5.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig5, use_container_width=True)

        # Question 9: Explicit
        st.divider()
        st.subheader("9. Vývoj explicitního obsahu")
        ex_trend = df.groupby('year')['explicit'].sum().reset_index()
        fig9 = px.line(ex_trend, x='year', y='explicit', markers=True, template="plotly_dark")
        st.plotly_chart(fig9, use_container_width=True)

else:
    st.info("Přejděte na 'Analysis' pro výsledky.")

# --- FOOTER ---
st.divider()
st.caption("🚀 Vytvořeno pro váš 300h rekvalifikační kurz.")
