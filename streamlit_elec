import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import streamlit as st

df = pd.read_csv("eco2mix-national-cons-def_court.csv")
df['Date et Heure'] = pd.to_datetime(df['Date et Heure'], format = "%Y-%m-%dT%H:%M:%S")
df = df.sort_values(by = ["Date et Heure"])
df = df.set_index('Date et Heure')

st.sidebar.title("Panorama du réseau électrique français")
st.sidebar.subheader("Menu")
parties_menu = ["Boites à moustache des filières de production",
                "Courbes des filières de production",
                "Carte des filières de production par région",
                "Prédiction de la consommation d'une région comme série temporelle",
                "Prédiction de la consommation d'une région en prenant en compte la température"]

choix_menu = st.sidebar.radio('', options=parties_menu)

if choix_menu==parties_menu[0]:
    st.title(parties_menu[0])
    st.info("Test de texte")


    choix_annee = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
    annee = st.selectbox("Choisissez une année :", options = choix_annee)
    
    fig1 = plt.figure(figsize=(15,8))
    ax1 = fig1.add_subplot(111)
    ax1.boxplot(df.loc[str(annee),'Fioul (MW)' : 'Bioénergies (MW)'].resample("D").mean(), showfliers=False)
    ax1.set_xticklabels(['Fioul','Charbon','Gaz','Nucléaire','Eolien','Solaire','Hydraulique','Pompage','Bioénergies'])
    ax1.set_ylabel("Production (MW)")
    ax1.set_title("Moyennes quotidiennes de puissance de production de l'année " + str(annee) )
    st.pyplot(fig1);
