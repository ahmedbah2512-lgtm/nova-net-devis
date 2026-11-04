import requests
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Devis Instantané - Nova Net", page_icon="✨", layout="centered"
)

# --- STYLE CSS & FOND DÉCORATIF ---
st.markdown(
    """
    <style>
    /* 1. Applique l'image en fond d'écran global fixe et couvrant */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                          url("https://images.unsplash.com/photo-1603712725038-e9334ae8f39f?q=80&w=1471&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* 2. Masquer les éléments superflus de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppToolbar {visibility: hidden;}

    /* 3. Style élégant et semi-transparent pour le formulaire et les blocs clés */
    .stForm, div[data-testid="stVerticalBlock"] > div > div.stForm {
        background-color: rgba(255, 255, 255, 0.92) !important;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* 4. Harmonisation des textes principaux pour qu'ils ressortent bien sur fond sombre */
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# En-tête de l'application
st.title("NOVA NET - Simulation & Devis")
st.write(
    "Obtenez une estimation instantanée pour l'entretien de vos locaux professionnels."
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

# =========================================================================
# --- TA ZONE DE CALCUL TARIFAIRE (MODIFIE ICI FACILEMENT) ---
# =========================================================================
TARIF_HORAIRE_HT = 31.0
M2_PAR_HEURE = 150.0
TEMPS_FIXE_PASSAGE = 0.5
FRAIS_FIXES_MENSUELS = 40.0
PLANCHER_PAR_PASSAGE = 35.0

semaines_par_mois = 52 / 12
facteur_freq = max(0.88, 1 - 0.02 * (passages - 1))
heures_par_passage = (TEMPS_FIXE_PASSAGE + surface / M2_PAR_HEURE) * facteur_freq
heures_mois = heures_par_passage * passages * semaines_par_mois

tarif_brut = FRAIS_FIXES_MENSUELS + heures_mois * TARIF_HORAIRE_HT
tarif_minimum = PLANCHER_PAR_PASSAGE * passages * semaines_par_mois

tarif_mensuel = round(max(tarif_minimum, tarif_brut), 2)
tarif_mensuel_ttc = round(tarif_mensuel * 1.20, 2)
# =========================================================================

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
    f"(Estimatif : {tarif_mensuel:.2f} € HT/mois) — Tarif récurrent mensuel."
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

# --- FORMULAIRE DE VALIDATION ---
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
                        "✅ Merci ! Votre demande a bien été transmise à Nova Net."
                        " Nous vous recontactons très rapidement."
                    )
                else:
                    st.error(
                        "❌ Une erreur est survenue lors de l'envoi. Veuillez réessayer."
                    )
            except Exception as e:
                st.error(f"❌ Erreur technique de connexion : {e}")
