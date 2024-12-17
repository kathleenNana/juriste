import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Charger les données
file_path = "competence.xlsx"  # Remplacez par votre fichier
data = pd.read_excel(file_path)

# Renommer les colonnes pour simplifier l'accès
data.rename(columns={
    'Nom et Prénoms': 'Name',
    'Grade': 'Grade',
    'Emploi': 'Job',
    'Fonction': 'Function',
    'Département': 'Department',
    'Localité': 'Location',
    'Responsabilité principale': 'Main_Responsibility',
    'Compétence': 'Competence'
}, inplace=True)

# Supprimer les colonnes inutiles
data.drop(columns=['Unnamed: 0', 'MATR.'], inplace=True, errors='ignore')

# Titre de l'application
st.title("Tableau de bord interactif des compétences des juristes")

# Sidebar pour filtres
st.sidebar.header("Filtres")
selected_name = st.sidebar.selectbox("Sélectionnez un juriste :", ['Tous'] + list(data['Name'].unique()))
selected_department = st.sidebar.multiselect("Sélectionnez un département :", data['Department'].unique(), default=data['Department'].unique())

# Filtrer les données
filtered_data = data.copy()
if selected_name != 'Tous':
    filtered_data = filtered_data[filtered_data['Name'] == selected_name]
filtered_data = filtered_data[filtered_data['Department'].isin(selected_department)]

# -------------------- 1. Diagramme en anneau --------------------
st.subheader("Proportion des compétences par département (Anneau)")

# Calculer la somme des compétences globales
competence_global = data.groupby('Department')['Competence'].sum().reset_index()

# Filtrer pour le juriste sélectionné
if selected_name != 'Tous':
    competence_selected = filtered_data.groupby('Department')['Competence'].sum().reset_index()
    competence_global = pd.merge(competence_global, competence_selected, on='Department', how='left', suffixes=('_global', '_selected'))
    competence_global['Competence_selected'] = competence_global['Competence_selected'].fillna(0)
else:
    competence_global['Competence_selected'] = competence_global['Competence']

# Créer l'anneau
fig_donut = go.Figure(data=[
    go.Pie(labels=competence_global['Department'],
           values=competence_global['Competence_selected'],
           hole=0.4, 
           hoverinfo="label+percent+value",
           textinfo='percent+label')
])
st.plotly_chart(fig_donut)

# -------------------- 2. Barres groupées --------------------
st.subheader("Comparaison des compétences par département")

fig_bar = px.bar(
    filtered_data, 
    x='Department', 
    y='Competence', 
    color='Grade',
    title="Compétences par département et par grade",
    barmode='group'
)
st.plotly_chart(fig_bar)

# -------------------- 3. Graphique radar --------------------
st.subheader("Forces et faiblesses du juriste")

if selected_name != 'Tous':
    radar_data = filtered_data.groupby('Department')['Competence'].sum().reset_index()
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=radar_data['Competence'],
        theta=radar_data['Department'],
        fill='toself',
        name=selected_name
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False
    )
    st.plotly_chart(fig_radar)
else:
    st.info("Veuillez sélectionner un juriste spécifique pour afficher le graphique radar.")

# -------------------- 4. Carte géographique --------------------
st.subheader("Localisation des compétences")

fig_map = px.scatter_geo(
    filtered_data, 
    locations='Location', 
    locationmode='country names',
    color='Department', 
    size='Competence',
    title="Carte des compétences par localité",
    hover_name='Name'
)
st.plotly_chart(fig_map)

# -------------------- 5. Heatmap --------------------
st.subheader("Répartition des compétences par Grade et Département")

heatmap_data = filtered_data.pivot_table(index='Grade', columns='Department', values='Competence', aggfunc='sum', fill_value=0)
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='Viridis'
))

fig_heatmap.update_layout(
    title="Carte thermique des compétences",
    xaxis_title="Département",
    yaxis_title="Grade"
)
st.plotly_chart(fig_heatmap)

# -------------------- Statistiques clés --------------------
st.sidebar.header("Statistiques clés")
total_competence = filtered_data['Competence'].sum()
average_competence = filtered_data['Competence'].mean()

st.sidebar.metric("Total des compétences", f"{total_competence:.2f}")
st.sidebar.metric("Moyenne des compétences", f"{average_competence:.2f}")

# -------------------- Fin --------------------
st.write("Visualisations interactives réalisées avec Plotly et Streamlit pour une meilleure expérience utilisateur.")
