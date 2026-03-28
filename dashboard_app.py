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
    
# --- DATA PATHS ---
MAIN_DATA_PATH = 'data/SESSION1_DATA/Downloadable exercise materials (Sesssion 1)/spotify_eda.xlsx'

# --- DATA LOADING & ANALYTICS ---
@st.cache_data
def load_and_analyze_data():
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

df_raw, df = load_and_analyze_data()

# --- MAIN CONTENT ---
st.title("📊 Data Science Parallel Flow")
st.markdown(f"### Aktuální fáze: `{current_step}`")

if current_step == "1. Framing the problem":
    tab1, tab2 = st.tabs(["🚀 Official Constraints", "🎬 Added Value Ideas"])
    
    with tab1:
        st.header("🎯 Cíle analýzy (Official Requirements)")
        st.write("Dle zadání musíme odpovědět na těchto 9 klíčových otázek:")
        
        questions = [
            "1. Kteří umělci mají v seznamu nejvíce skladeb?",
            "2. Existuje korelace mezi délkou skladby a rokem jejího vydání?",
            "3. Ovlivňují vlastnosti jako danceability, energy nebo loudness popularitu skladby?",
            "4. Najdeme mezi top autory takové, jejichž tvorba obsahuje převážně 'negativní' skladby?",
            "5. Kteří umělci mají nejvyšší počet nejpopulárnějších skladeb?",
            "6. Mění se tempo skladby v závislosti na roce vydání?",
            "7. Kolik skladeb máme v seznamu podle hudebního žánru?",
            "8. Kolik skladeb máme v seznamu podle roku vydání?",
            "9. Kolik skladeb obsahuje 'explicitní' texty? Souvisí jejich počet s rokem vydání?"
        ]
        
        for q in questions:
            st.markdown(f"- **{q}**")
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="excel-box"><b>📗 Excel Approach:</b><br>Zápis cílů do prvního listu, definice rozsahu.</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="pandas-box"><b>🐼 Pandas Approach:</b><br>Komentování kódu, definování hlaviček v Jupyteru.</div>', unsafe_allow_html=True)

    with tab2:
        st.header("💡 Naše přidaná hodnota")
        st.write("Zde realizujeme nápady s přidanou hodnotou, na které v Excelu narazíte jen zřídka.")
        
        if df is not None:
            # TREND 1: Sadness Paradox
            st.markdown('<div class="added-value-card">', unsafe_allow_html=True)
            st.subheader("😢 The Sadness Paradox (Záhada smutku)")
            st.write("Analýza průměrné pozitivity (Valence) v letech 2000-2019.")
            trend_valence = df.groupby('year')['valence'].mean().reset_index()
            fig_valence = px.line(trend_valence, x='year', y='valence', 
                                  title="Průměrná nálada písní v čase",
                                  markers=True, line_shape='spline')
            fig_valence.update_layout(yaxis_range=[0.4, 0.7], template="plotly_dark")
            st.plotly_chart(fig_valence, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # TREND 2: Loudness VS Popularity
            st.markdown('<div class="added-value-card">', unsafe_allow_html=True)
            st.subheader("🔊 The Loudness War (Válka o hlasitost)")
            fig_loud = px.scatter(df, x='loudness', y='popularity', color='popularity',
                                  title="Korelace hlasitosti a popularity",
                                  hover_data=['song', 'artist_name'],
                                  color_continuous_scale='Viridis')
            fig_loud.update_layout(template="plotly_dark")
            st.plotly_chart(fig_loud, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

elif current_step == "2. Obtaining data":
    if df_raw is not None:
        st.success(f"✅ Data úspěšně načtena ({len(df_raw)} řádků).")
        st.dataframe(df_raw.head(10))

elif current_step == "3. Cleaning and processing":
    st.header("🧹 Čištění a zpracování")
    view_type = st.radio("Vyberte dataset:", ["Hlavní analýza", "Cleaning Exercise 1"])
    if view_type == "Hlavní analýza":
        if df_raw is not None and df is not None:
            st.metric("Snížení počtu řádků (Deduplikace)", len(df_raw), delta=int(len(df)-len(df_raw)))
            st.dataframe(df[['artist_name', 'song', 'duration_min', 'primary_genre']].head(10))
    else:
        EXERCISE_DATA_PATH = 'data/SESSION1_DATA/Downloadable exercise materials (Sesssion 1)/spotify_cleaning_exercises.xlsx'
        if os.path.exists(EXERCISE_DATA_PATH):
            df_ex = pd.read_excel(EXERCISE_DATA_PATH, sheet_name='songs')
            st.write("📋 **Finálně vyčištěná data (Exercise 1):**")
            st.dataframe(df_ex.head(15).style.format({'instrumentalness': '{:.6f}'}))

elif current_step == "5. Analysis":
    st.header("📈 Finální analýza (Dle zadání 1-9)")
    
    if df is not None:
        # Question 1: Total Hits Volume
        st.subheader("1. Kteří umělci mají v seznamu nejvíce skladeb?")
        top_artists_v = df['artist_name'].value_counts().head(10).reset_index()
        top_artists_v.columns = ['Artist', 'Count']
        fig1 = px.bar(top_artists_v, x='Count', y='Artist', orientation='h', 
                      title="TOP 10 umělců (Všechny hity)", color='Count', template="plotly_dark")
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)

        # Question 2: Duration vs Year (Box Plot)
        st.divider()
        st.subheader("2. Korelace mezi délkou skladby a rokem vydání")
        df_sorted_year = df.sort_values('year')
        fig2 = px.box(df_sorted_year, x='year', y='duration_min', title="Distribuce délky skladeb v letech", 
                      color_discrete_sequence=['#6366f1'], template="plotly_dark")
        fig2.update_xaxes(type='category')
        st.plotly_chart(fig2, use_container_width=True)

        # Question 3: Features vs Popularity (Heatmap)
        st.divider()
        st.subheader("3. Ovlivňují danceability, energy nebo loudness popularitu?")
        corr_cols = ['popularity', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'valence', 'tempo']
        corr_matrix = df[corr_cols].corr()
        fig3 = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r',
                         title="Korelační matice hudebních vlastností", template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)
        st.write("**Výsledek:** Nejsilnější pozitivní korelaci s popularitou má `loudness` (hlasitost).")

        # Question 4: Negative Artists
        st.divider()
        st.subheader("4. Analýza negativity u top autorů")
        top_list_v = df['artist_name'].value_counts().head(10).index
        neg_df = df[df['artist_name'].isin(top_list_v)].groupby('artist_name')['valence'].mean().reset_index()
        neg_df = neg_df.sort_values('valence')
        fig4 = px.bar(neg_df, x='valence', y='artist_name', orientation='h', color='valence',
                      title="Průměrná 'pozitivita' (Valence) TOP 10 umělců", 
                      color_continuous_scale='RdYlGn', template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)

        # Question 5: Superstars (Threshold)
        st.divider()
        st.subheader("5. Kteří umělci mají nejvyšší počet nejpopulárnějších skladeb?")
        pop_threshold = st.slider("Stanovte hranici 'Superhitu' (skóre popularity):", 60, 95, 80)
        top_artists_i = df[df['popularity'] > pop_threshold]['artist_name'].value_counts().head(10).reset_index()
        top_artists_i.columns = ['Artist', 'Count']
        fig5 = px.bar(top_artists_i, x='Count', y='Artist', orientation='h', 
                      title=f"Umělci s nejvíce songy nad {pop_threshold} bodů", color='Count', template="plotly_dark",
                      color_continuous_scale='Sunsetdark')
        fig5.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig5, use_container_width=True)

        # Question 6: Tempo vs Year
        st.divider()
        st.subheader("6. Mění se tempo skladby v závislosti na roce vydání?")
        trend_tempo = df.groupby('year')['tempo'].mean().reset_index()
        fig6 = px.line(trend_tempo, x='year', y='tempo', markers=True, 
                       title="Vývoj průměrného tempa (BPM) 2000-2019", template="plotly_dark")
        st.plotly_chart(fig6, use_container_width=True)

        # Question 7: Genre Distribution
        st.divider()
        st.subheader("7. Počet skladeb podle hudebního žánru")
        genre_counts = df['primary_genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        fig7 = px.pie(genre_counts, values='Count', names='Genre', title="Podíl žánrů v žebříčcích",
                      template="plotly_dark", hole=0.4)
        st.plotly_chart(fig7, use_container_width=True)

        # Question 8: Count per Year
        st.divider()
        st.subheader("8. Počet skladeb podle roku vydání")
        year_counts = df['year'].value_counts().reset_index().sort_values('year')
        year_counts.columns = ['Year', 'Count']
        fig8 = px.bar(year_counts, x='Year', y='Count', title="Počet hitů v jednotlivých letech",
                      color='Count', template="plotly_dark")
        st.plotly_chart(fig8, use_container_width=True)

        # Question 9: Explicit Content
        st.divider()
        st.subheader("9. Počet explicitních skladeb a jejich vývoj")
        colA, colB = st.columns(2)
        with colA:
            explicit_counts = df['explicit'].value_counts().reset_index()
            explicit_counts.columns = ['Is Explicit', 'Count']
            fig9a = px.pie(explicit_counts, values='Count', names='Is Explicit', title="Celkový podíl explicitního obsahu",
                           template="plotly_dark", color_discrete_sequence=['#ef4444', '#10b981'])
            st.plotly_chart(fig9a, use_container_width=True)
        with colB:
            explicit_trend = df.groupby('year')['explicit'].sum().reset_index()
            fig9b = px.line(explicit_trend, x='year', y='explicit', markers=True, 
                            title="Vývoj počtu explicitních songů v čase", template="plotly_dark")
            st.plotly_chart(fig9b, use_container_width=True)

else:
    st.info("Přejděte na 'Analysis' v postranním panelu pro finální výsledky v pořadí 1-9.")

# --- FOOTER ---
st.divider()
st.caption("🚀 Vytvořeno pro váš 300h rekvalifikační kurz.")
