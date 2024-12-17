import sqlite3
import pandas as pd
import streamlit as st

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('dossiers.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dossiers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_imputation TEXT,
        numero_dossier TEXT,
        origine_affaires TEXT,
        objet TEXT,
        juridictions TEXT,
        juriste TEXT,
        instructions_et_delais TEXT
    )
    """)
    conn.commit()
    conn.close()

# Ajouter un dossier
def add_dossier(numero_imputation, numero_dossier, origine_affaires, objet, juridictions, juriste, instructions_et_delais):
    conn = sqlite3.connect('dossiers.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO dossiers (numero_imputation, numero_dossier, origine_affaires, objet, juridictions, juriste, instructions_et_delais)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (numero_imputation, numero_dossier, origine_affaires, objet, juridictions, juriste, instructions_et_delais))
    conn.commit()
    conn.close()

# Charger les dossiers
def load_dossiers():
    conn = sqlite3.connect('dossiers.db')
    df = pd.read_sql("SELECT * FROM dossiers", conn)
    conn.close()
    return df

# Interface utilisateur avec Streamlit
st.title("Système d'Information Juridique")
menu = st.sidebar.selectbox("Menu", ["Ajouter Dossier", "Voir Dossiers"])

if menu == "Ajouter Dossier":
    st.subheader("Ajouter un nouveau dossier")
    numero_imputation = st.text_input("Numéro d'imputation")
    numero_dossier = st.text_input("Numéro de dossier")
    origine_affaires = st.text_area("Origine / Affaires")
    objet = st.text_input("Objet")
    juridictions = st.text_input("Juridictions")
    juriste = st.text_input("Juriste")
    instructions_et_delais = st.text_area("Instructions et Délais")

    if st.button("Ajouter"):
        add_dossier(numero_imputation, numero_dossier, origine_affaires, objet, juridictions, juriste, instructions_et_delais)
        st.success("Dossier ajouté avec succès !")

elif menu == "Voir Dossiers":
    st.subheader("Liste des dossiers")
    df = load_dossiers()
    st.dataframe(df)

# Initialisation de la base de données
init_db()
