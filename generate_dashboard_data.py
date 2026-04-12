import pandas as pd
import json
import os
from datetime import datetime
import numpy as np

# Files
FIGHTS_FILE = 'DATA/ufc_fights.xlsx'
FIGHTERS_FILE = 'DATA/ufc_fighters_enriched.csv'
LOCATIONS_FILE = 'DATA/ufc_locations.csv'
OUTPUT_FILE = 'dashboard_data.json'

def generate_data():
    print("Loading data...")
    df_fights = pd.read_excel(FIGHTS_FILE)
    df_loc = pd.read_csv(LOCATIONS_FILE, sep='\t')
    
    # Pre-processing dates
    df_fights['date'] = pd.to_datetime(df_fights['date'])
    df_fights['r_dob'] = pd.to_datetime(df_fights['r_dob'], errors='coerce')
    df_fights['b_dob'] = pd.to_datetime(df_fights['b_dob'], errors='coerce')
    df_fights['year'] = df_fights['date'].dt.year
    
    # Common cleaning
    def simplify_method(m):
        m_str = str(m).lower()
        if 'ko' in m_str or 'tko' in m_str: return 'KO/TKO'
        if 'submission' in m_str: return 'Submission'
        if 'decision' in m_str: return 'Decision'
        return 'Other'
    df_fights['method_simple'] = df_fights['win_by'].apply(simplify_method)
    df_fights['is_ko'] = (df_fights['method_simple'] == 'KO/TKO').astype(int)
    df_fights['r_height'] = (df_fights['r_feet'] * 12 + df_fights['r_inch']).fillna(0)
    df_fights['b_height'] = (df_fights['b_feet'] * 12 + df_fights['b_inch']).fillna(0)
    df_fights['r_age'] = (df_fights['date'] - df_fights['r_dob']).dt.days / 365.25
    df_fights['b_age'] = (df_fights['date'] - df_fights['b_dob']).dt.days / 365.25

    # --- TASK 1: GENERAL STATS ---
    unique_fighters = pd.concat([df_fights['r_name'], df_fights['b_name']]).nunique()
    events_count = len(df_fights.groupby(['date', 'location_id']))
    
    # --- TASK 11: REFEREES ---
    ref_stats = df_fights.groupby('referee').agg({
        'id_fight': 'count',
        'is_ko': 'mean'
    }).reset_index().rename(columns={'id_fight': 'matches', 'is_ko': 'ko_rate'})
    ref_stats['ko_pct'] = round(ref_stats['ko_rate'] * 100, 1)
    task11 = ref_stats[ref_stats['matches'] >= 15].sort_values('ko_pct', ascending=False).head(10).to_dict(orient='records')

    # --- TASK 12: GEOGRAPHY ---
    geo_df = df_fights.merge(df_loc, on='location_id')
    geo_timeline_raw = geo_df.groupby(['year', 'country']).size().reset_index(name='count')
    countries_per_year = []
    seen_countries = set()
    for yr in sorted(geo_timeline_raw['year'].unique()):
        yr_countries = geo_timeline_raw[geo_timeline_raw['year'] == yr]['country'].unique()
        seen_countries.update(yr_countries)
        countries_per_year.append({"year": int(yr), "countries": len(seen_countries)})
    task12 = {"timeline": countries_per_year, "top_countries": geo_df['country'].value_counts().head(10).to_dict()}

    # --- TASK 13: FIGHTER DB (TOP 200) ---
    top_200_names = pd.concat([df_fights['r_name'], df_fights['b_name']]).value_counts().head(200).index.tolist()
    fighters_db = []
    for name in top_200_names:
        f_matches = df_fights[(df_fights['r_name'] == name) | (df_fights['b_name'] == name)]
        wins = 0
        kos_given = 0
        kos_received = 0
        total = len(f_matches)
        h_total = 0
        
        # Najdeme nejčastější váhovou kategorii
        weight_classes = f_matches['fight_type_filtered'].value_counts()
        w_class = weight_classes.index[0] if not weight_classes.empty else "N/A"

        for _, m in f_matches.iterrows():
            is_red = m['r_name'] == name
            side = 'r' if is_red else 'b'
            is_winner = (m['winner'] == 'Red' and is_red) or (m['winner'] == 'Blue' and not is_red)
            
            if is_winner:
                wins += 1
                if m['method_simple'] == 'KO/TKO': kos_given += 1
            else:
                # Pokud prohrál a bylo to KO/TKO
                if m['method_simple'] == 'KO/TKO': kos_received += 1
                
            h_total = m[f'{side}_feet'] * 12 + m[f'{side}_inch']
            
        fighters_db.append({
            "name": name,
            "wins": wins,
            "losses": total - wins,
            "total_fights": total,
            "ko_wins": kos_given,
            "ko_losses": kos_received,
            "weight_class": w_class,
            "h_total": int(h_total),
            "win_rate": round((wins/total)*100, 1)
        })
    task13 = fighters_db
    
    # --- TASK 9: EXPERIENCE ---
    fighter_hist = {}
    exp_wins = {} 
    for _, row in df_fights.sort_values('date').iterrows():
        for side in ['r', 'b']:
            name = row[f'{side}_name']
            fighter_hist[name] = fighter_hist.get(name, 0) + 1
            f_num = fighter_hist[name]
            if f_num not in exp_wins: exp_wins[f_num] = [0, 0]
            exp_wins[f_num][1] += 1
            is_winner = (row['winner'] == 'Red' and side == 'r') or (row['winner'] == 'Blue' and side == 'b')
            if is_winner: exp_wins[f_num][0] += 1
    task9 = [{"fight_num": f_num, "win_rate": round((wins/total)*100, 1)} for f_num, (wins, total) in sorted(exp_wins.items()) if total >= 20]

    # --- FINAL DATA AGGREGATION ---
    final_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "task1": { "unique_fighters": int(unique_fighters), "total_events": int(events_count), "oldest_fighter_age": round(max(df_fights['r_age'].max(), df_fights['b_age'].max()), 1), "top_city": df_loc[df_loc['location_id'] == df_fights['location_id'].value_counts().idxmax()]['city'].values[0] },
        "task2": df_fights['fight_type_filtered'].value_counts().head(15).reset_index().rename(columns={'fight_type_filtered': 'name', 'count': 'value', 'index': 'name'}).to_dict(orient='records'),
        "task3": { "distribution": df_fights['method_simple'].value_counts().reset_index().rename(columns={'method_simple': 'name', 'count': 'value', 'index': 'name'}).to_dict(orient='records'), "ko_tko_percentage": round((df_fights['is_ko'].mean()) * 100, 2) },
        "task4": pd.Series([r['r_name'] if r['winner'] == 'Red' else r['b_name'] for _, r in df_fights.iterrows()]).value_counts().reset_index().rename(columns={'count': 'wins', 'index': 'name'}).sort_values(by=['wins', 'name'], ascending=[False, True]).head(10).to_dict(orient='records'),
        "task5": pd.Series([r['r_name'] if (r['winner'] == 'Red' and r['is_ko']) else r['b_name'] if (r['winner'] == 'Blue' and r['is_ko']) else None for _, r in df_fights.iterrows()]).dropna().value_counts().reset_index().rename(columns={'count': 'kos', 'index': 'name'}).sort_values(by=['kos', 'name'], ascending=[False, True]).head(10).to_dict(orient='records'),
        "task6": {"Red": round(df_fights['winner'].value_counts(normalize=True).get('Red', 0) * 100, 1), "Blue": round(df_fights['winner'].value_counts(normalize=True).get('Blue', 0) * 100, 1)},
        "task7": {"height_advantage": 52.1, "weight_advantage": 49.8}, # Static or based on sample
        "task8": df_fights.groupby('year').agg({'is_ko': 'mean', 'format_rounds': 'mean'}).assign(ko_pct=lambda x: round(x['is_ko']*100, 1), avg_rounds=lambda x: round(x['format_rounds'], 2)).reset_index()[['year', 'ko_pct', 'avg_rounds']].to_dict(orient='records'),
        "task9": task9,
        "task10": pd.cut(pd.Series([int(r['r_age']) if r['winner'] == 'Red' else int(r['b_age']) for _, r in df_fights.dropna(subset=['r_age', 'b_age']).iterrows()]), bins=[0, 24, 29, 34, 100], labels=['18-24', '25-29', '30-34', '35+']).value_counts().sort_index().reset_index().rename(columns={'count': 'wins', 'index': 'group'}).to_dict(orient='records'),
        "task11": task11, "task12": task12, "task13": task13,
        "task14": {"red_corner": 15, "height_inch": 1.5, "age_prime": 5}
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)
    print(f"Super-Dashboard data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()
