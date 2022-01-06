import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import datetime

df = pd.read_csv("eco2mix-national-cons-def_court.csv")
df['Date et Heure'] = pd.to_datetime(df['Date et Heure'], format = "%Y-%m-%dT%H:%M:%S")
df = df.sort_values(by = ["Date et Heure"])
df = df.set_index('Date et Heure')

st.sidebar.title("Panorama du réseau électrique français")
st.sidebar.subheader("Menu")
parties_menu = ["Boites à moustache des filières de production",
                "Boites à moustache mensuelles des filières de production et de la consommation",
                "Courbes des filières de production",
                "Carte des filières de production par région",
                "Prédiction de la consommation d'une région comme série temporelle",
                "Prédiction de la consommation d'une région en prenant en compte la température"]

choix_menu = st.sidebar.radio('', options=parties_menu)

if choix_menu==parties_menu[0]:
    st.title(parties_menu[0])
    st.info("Le graphique suivant permet de comparer, année après année, l'amplitude de puissance moyenne produite quotidiennement par filière de production.")


    choix_annee = ["2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
    annee = st.selectbox("Choisissez une année :", options = choix_annee)
    
    fig1 = plt.figure(figsize=(15,8))
    ax1 = fig1.add_subplot(111)
    ax1.boxplot(df.loc[str(annee),'Fioul (MW)' : 'Bioénergies (MW)'].resample("D").mean(), showfliers=False)
    ax1.set_xticklabels(['Fioul','Charbon','Gaz','Nucléaire','Eolien','Solaire','Hydraulique','Bioénergies'])
    ax1.set_ylim(0, 61000)
    ax1.set_ylabel("Production (MW)")
    ax1.set_title("Moyennes quotidiennes de puissance de production de l'année " + str(annee) )
    st.pyplot(fig1)

    
elif choix_menu==parties_menu[1]:
    st.title(parties_menu[1])
    st.info("Le graphique suivant permet de visuliser la saisonnalité de chacune des filière de production et de la consommation.")
    
    
    choix_filiere = ['Consommation (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)','Fioul (MW)', \
                     'Charbon (MW)', 'Gaz (MW)','Bioénergies (MW)']
    filiere = st.selectbox("Choisissez une filière :", options = choix_filiere)   
    
    fig2 = plt.figure(figsize=[15,8])
    ax2 = fig2.add_subplot(111)

    df = df.loc["2012":"2020",:]

    l=list()
    for i in df.resample("M").mean().index.month.unique():
      st.write(i)
    #    l.append(df.resample("M").mean()[df.resample("M").mean().index.month == i]['Solaire (MW)'])
    ax2.plot(df['Solaire (MW)'])
    #plt.sca(ax2)
    #plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12], ['J', 'F', 'M', 'A','M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    ax2.set_ylabel("Consommation (MW)")
    st.pyplot(fig2)

