import requests
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Devis Instantané - Nova Net", page_icon="✨", layout="centered"
)

# --- STYLE CSS : FOND NOIR UNI ---
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppToolbar {visibility: hidden;}
div[class*="viewerBadge"] {display: none !important;}
a[href*="streamlit.io"] {display: none !important;}

/* 1. Fond noir uni sur toute l'application */
.stApp {
    background-color: #0e1117 !important;
}

.stApp > header {
    background-color: transparent !important;
}

/* 2. Suppression de tout fond blanc sur le formulaire */
.stForm {
    background-color: transparent !important;
    border: none !important;
    padding: 0px;
}

/* 3. Tous les textes en blanc pour un contraste parfait sur fond noir */
h1, h2, h3, p, label, span {
    color: #ffffff !important;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# En-tête
st.title("NOVA NET - Simulation & Devis")

# L'image replacée juste en dessous du titre
st.image(
    "https://images.unsplash.com/photo-1603712725038-e9334ae8f39f?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    use_container_width=True,
)

st.write(
    "Obtenez une estimation instantanée pour l'entretien de vos locaux"
    " professionnels."
)

# Entrées utilisateur
surface = st.number_input(
    "Superficie de vos locaux (en m²) :",
    min_value=10,
    max_value=1000,
    value=50,
    step=5,
)
passages = st.slider(
    "Nombre de passages par semaine :", min_value=1, max_value=7, value=3
)

# --- PARAMÈTRES (à ajuster) ---
TARIF_HORAIRE_HT = 31.0
M2_PAR_HEURE = 150.0
TEMPS_FIXE_PASSAGE = 0.5
FRAIS_FIXES_MENSUELS = 40.0
PLANCHER_PAR_PASSAGE = 35.0

# --- FORMULE DE CALCUL TARIF ---
semaines_par_mois = 52 / 12
facteur_freq = max(0.88, 1 - 0.02 * (passages - 1))
heures_par_passage = (TEMPS_FIXE_PASSAGE + surface / M2_PAR_HEURE) * facteur_freq
heures_mois = heures_par_passage * passages * semaines_par_mois

tarif_brut = FRAIS_FIXES_MENSUELS + heures_mois * TARIF_HORAIRE_HT
tarif_minimum = PLANCHER_PAR_PASSAGE * passages * semaines_par_mois

tarif_mensuel = round(max(tarif_minimum, tarif_brut), 2)
tarif_mensuel_ttc = round(tarif_mensuel * 1.20, 2)

# --- AFFICHAGE DU RÉSULTAT CLIENT ---
st.divider()
st.subheader("📋 Résultat de votre
