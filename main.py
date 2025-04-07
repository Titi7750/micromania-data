import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- LOAD DATA ---
@st.cache_data
def load_data():
    dataframe = pd.read_excel("./excel/micromania_donnees_fictives.xlsx", engine="openpyxl")
    dataframe["Maturité CA"] = (dataframe["Chiffre d'Affaires Annuel (€)"] - dataframe["Chiffre d'Affaires Annuel (€)"].min()) / \
                        (dataframe["Chiffre d'Affaires Annuel (€)"].max() - dataframe["Chiffre d'Affaires Annuel (€)"].min())

    def classer_taille(surface):
        if surface < 250:
            return 'Petit'
        elif surface < 350:
            return 'Moyen'
        else:
            return 'Grand'

    dataframe["Taille Magasin"] = dataframe["Surface (m²)"].apply(classer_taille)
    return dataframe

dataframe = load_data()

# --- HIERARCHICAL FILTERS ---
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ff000050;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Les filtres")

# Step 1: Store size
available_sizes = dataframe["Taille Magasin"].unique()
selected_size = st.sidebar.multiselect("Taille du magasin", options=available_sizes, default=available_sizes)
dataframe_step_one = dataframe[dataframe["Taille Magasin"].isin(selected_size)]

# Step 2: City (filtered by size)
available_cities = dataframe_step_one["Ville"].unique()
selected_city = st.sidebar.multiselect("Ville", options=available_cities, default=available_cities)
dataframe_step_two = dataframe_step_one[dataframe_step_one["Ville"].isin(selected_city)]

# Step 3: Store (filtered by size AND city)
available_stores = dataframe_step_two["Nom Magasin"].unique()
selected_store = st.sidebar.multiselect("Magasin", options=available_stores, default=available_stores)

# Final filtering
filter_dataframe = dataframe_step_two[dataframe_step_two["Nom Magasin"].isin(selected_store)]

# --- DASHBOARD DISPLAY ---
st.title("🦩Tableau de Bord Micromania")

if not filter_dataframe.empty:
    # Radar Chart
    st.subheader("🔍 Maturité d’un magasin (Radar Chart)")
    store_name = st.selectbox("Sélectionne un magasin :", filter_dataframe["Nom Magasin"])
    store = filter_dataframe[filter_dataframe["Nom Magasin"] == store_name].iloc[0]

    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=[store["Chiffre d'Affaires Annuel (€)"], store["Nombre de Transactions"], store["Nombre d'Employés"]],
        theta=["Chiffre d'affaires", "Transactions", "Employés"],
        fill='toself',
        name=store_name
    ))
    radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
    st.plotly_chart(radar_fig)

    # Bar Chart
    st.subheader("🏆 Comparatif de la maturité (CA)")
    bar_fig = px.bar(filter_dataframe, x="Nom Magasin", y="Maturité CA", color="Maturité CA", title="Maturité du chiffre d'affaires")
    st.plotly_chart(bar_fig)

    # Camembert
    st.subheader("📍 Répartition par domaine")
    domain_option = st.radio("Regrouper par :", ["Ville", "Taille Magasin"], horizontal=True)
    camembert_fig = px.pie(filter_dataframe, names=domain_option, title=f"Répartition par {domain_option.lower()}")
    st.plotly_chart(camembert_fig)

    # Data
    st.subheader("📋 Données détaillées")
    st.dataframe(filter_dataframe)

else:
    st.warning("Aucun magasin ne correspond aux filtres sélectionnés.")
