import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Charger le modèle
from joblib import load
model = load('pipeline_xgb.pkl')

# Configuration de la page
st.set_page_config(
    page_title="Détection de Fraude",
    page_icon="🔍",
    layout="wide"
)

# Affichage du logo et personnalisation du style avec Bootstrap
st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
        }
        .container-fluid {
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 30px;
            margin: 20px auto;
            max-width: 800px;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .btn-predict {
            background: linear-gradient(45deg, #0072C6, #0056b3);
            border: none;
            border-radius: 10px;
            padding: 12px 30px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            transition: all 0.3s ease;
        }
        .btn-predict:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,114,198,0.4);
        }
        .result-fraud {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        }
        .result-no-fraud {
            background: linear-gradient(45deg, #51cf66, #40c057);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
        }
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .card-header {
            background: linear-gradient(45deg, #0072C6, #0056b3);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            font-weight: bold;
        }
        /* Forcer la couleur des labels Streamlit */
        label, .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: #111 !important;
            font-weight: 600;
            font-size: 1.05rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Affichage du logo en haut
st.image("Logo.png", width=150)
st.markdown(
    """
    <div class="logo-container">
        <h1 style="color: #0072C6; font-weight: bold; margin-bottom: 30px; text-align:center;">🔍 Détection de Fraude</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Conteneur principal
st.markdown('<div class="container-fluid">', unsafe_allow_html=True)

# Formulaire de saisie
st.markdown(
    """
    <div class="card">
        <div class="card-header">
            <h3 style="margin: 0;">📊 Paramètres de la Transaction</h3>
        </div>
        <div class="card-body">
    """,
    unsafe_allow_html=True
)

# Création de colonnes pour une meilleure organisation
col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("💰 Montant de la transaction", value=0.0, help="Montant en euros")
    type_operation = st.selectbox("🏦 Type d'opération", ("CASH_OUT", "TRANSFER"), help="Type de transaction")
    oldbalanceOrg = st.number_input("💳 Ancien solde expéditeur", value=0.0, help="Solde avant transaction")
    newbalanceOrig = st.number_input("💳 Nouveau solde expéditeur", value=0.0, help="Solde après transaction")

with col2:
    oldbalanceDest = st.number_input("💳 Ancien solde destinataire", value=0.0, help="Solde destinataire avant")
    newbalanceDest = st.number_input("💳 Nouveau solde destinataire", value=0.0, help="Solde destinataire après")
    step = st.number_input("⏰ Étape temporelle", value=1, min_value=1, step=1, help="Moment de la transaction")

# Encodage des variables binaires
CASH_OUT = 1 if type_operation == "CASH_OUT" else 0
TRANSFER = 1 if type_operation == "TRANSFER" else 0

st.markdown('</div></div>', unsafe_allow_html=True)

# Bouton de prédiction
st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
if st.button("🔍 Analyser la Transaction", key="predict_btn"):
    # Création du DataFrame pour la prédiction
    X = pd.DataFrame([[step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, CASH_OUT, TRANSFER]],
        columns=["step","amount","oldbalanceOrg", "newbalanceOrig", "oldbalanceDest","newbalanceDest","type_CASH_OUT", "type_TRANSFER"])
    
    # Prédiction
    prediction = model.predict(X)[0]
    
    # Affichage du résultat
    if prediction == 1:
        st.markdown(
            '<div class="result-fraud">🚨 FRAUDE DÉTECTÉE 🚨</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="result-no-fraud">✅ TRANSACTION LÉGITIME ✅</div>',
            unsafe_allow_html=True
        )
    
    # Affichage des détails
    st.markdown(
        """
        <div class="card">
            <div class="card-header">
                <h4 style="margin: 0;">📋 Détails de l'Analyse</h4>
            </div>
            <div class="card-body">
        """,
        unsafe_allow_html=True
    )
    
    st.write("**Données analysées :**")
    st.dataframe(X, use_container_width=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; color: #666; font-size: 14px;">
        <p>🔒 Système de détection de fraude basé sur XGBoost</p>
    </div>
    """,
    unsafe_allow_html=True
)
