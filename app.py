import requests
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Devis Instantané - Nova Net", page_icon="✨", layout="centered"
)

# Masquer la barre d'outils et le pied de page Streamlit
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stAppToolbar {visibility: hidden;}
div[class*="viewerBadge"] {display: none !important;}
a[href*="streamlit.io"] {display: none !important;}
</style>
"""
st.markdown(
    """
    <style>
    /* 1. Applique l'image de fond sur toute l'application */
    .stApp {
        background-image: url("MET_TON_LIEN_IMAGE_ICI");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* 2. Rend les conteneurs et blocs semi-transparents pour voir l'image à travers */
    .stApp > header {
        background-color: transparent !important;
    }
    
    div.stBlock, div.stVerticalBlock > div, .stForm {
        background-color: rgba(255, 255, 255, 0.85) !important; /* Fond blanc semi-transparent */
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.image(
    "https://images.unsplash.com/photo-1603712725038-e9334ae8f39f?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D",
    use_container_width=True,
)
st.title("NOVA NET - Simulation & Devis")
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

# --- FORMULE DE CALCUL TARIF ---
frais_fixes = 120.0
base_surface = surface * 1.3
multiplicateur_frequence = passages**1.25 + (passages * 0.4)
tarif_brut = frais_fixes + (base_surface * multiplicateur_frequence)

# Plancher dynamique
if surface <= 40:
  tarif_minimum = 280.0
else:
  tarif_minimum = 280.0 + ((surface - 40) * 3.5)

tarif_mensuel = max(tarif_minimum, tarif_brut)
tarif_mensuel_ttc = tarif_mensuel * 1.20

# --- AFFICHAGE DU RÉSULTAT CLIENT ---
st.divider()
st.subheader("📋 Résultat de votre estimation")

col1, col2 = st.columns(2)
with col1:
  st.metric(
      label="Tarif Mensuel HT", value=f"{tarif_mensuel:,.2f} € HT / mois"
  )
with col2:
  st.metric(
      label="Tarif Mensuel TTC", value=f"{tarif_mensuel_ttc:,.2f} € TTC / mois"
  )

st.caption(
    f" (Estimatif : {tarif_mensuel:.2f} € HT/mois) — Tarif récurrent mensuel."
    " Une visite de validation sera réalisée."
)

st.info(
    "💡 **Sans engagement** - Ce tarif inclut notre prestation professionnelle"
    " sur-mesure. Remplissez le formulaire ci-dessous pour valider votre"
    " demande !"
)

prestation_choisie = (
    f"Nettoyage - {surface} m², {passages} passage(s)/semaine"
    f" (Estimatif : {tarif_mensuel:.2f} € HT/mois - TTC : {tarif_mensuel_ttc:.2f}"
    " €)"
)

# --- FORMULAIRE UNIQUE DE VALIDATION ---
st.markdown("### Finalisez votre demande")

with st.form("formulaire_devis_nova_net"):
  nom_client = st.text_input("Nom du cabinet / Société *")

  col1, col2 = st.columns(2)
  with col1:
    tel_client = st.text_input("Téléphone *")
  with col2:
    email_client = st.text_input("Adresse e-mail *")

  ville_chantier = st.text_input("Ville ou Code Postal du cabinet *")
  jours_souhaites = st.text_input(
      "Jours souhaités pour l'intervention (ex: du lundi au vendredi...)"
  )
  remarques = st.text_area(
      "Demandes particulières / Précisions (accès, horaires...)"
  )

  valider_form = st.form_submit_button(
      "🚀 Valider et envoyer ma demande de devis"
  )

  if valider_form:
    if not nom_client or not tel_client or not email_client or not ville_chantier:
      st.error("Veuillez remplir tous les champs obligatoires (*).")
    else:
      # METS TON URL GOOGLE APPS SCRIPT ICI :
      URL_GOOGLE_SCRIPT = "https://script.google.com/macros/s/AKfycbw1nyVx0Ihou3pb3gb2HMUPn9_hj9yvrk__sPyFx_VRvHWvGdmfeKXVhaw_PhU-yiBdvA/exec"

      donnees = {
          "nom": nom_client,
          "telephone": tel_client,
          "email": email_client,
          "ville": ville_chantier,
          "prestation": prestation_choisie,
          "jours": jours_souhaites,
          "remarques": remarques,
      }

      try:
        reponse = requests.post(URL_GOOGLE_SCRIPT, json=donnees)
        if reponse.status_code == 200:
          st.success(
              "✅ Merci ! Votre demande a bien été transmise à Nova Net. Nous"
              " vous recontactons très rapidement."
          )
        else:
          st.error(
              "❌ Une erreur est survenue lors de l'envoi. Veuillez réessayer."
          )
      except Exception as e:
        st.error(f"❌ Erreur technique de connexion : {e}")
