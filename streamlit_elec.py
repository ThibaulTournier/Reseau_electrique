import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import datetime
import folium
import json
from math import *
from streamlit_folium import folium_static

df = pd.read_csv("eco2mix-national-cons-def_court.csv")
df['Date et Heure'] = pd.to_datetime(df['Date et Heure'], format = "%Y-%m-%dT%H:%M:%S")
df = df.sort_values(by = ["Date et Heure"])
df = df.set_index('Date et Heure')
df["Mois"] = df.index.month


df0 = pd.read_csv("eco2mix-regional-cons-def_court.csv")
df0['Date - Heure'] = pd.to_datetime(df0['Date - Heure'])
df0 = df0.set_index('Date - Heure')
df0 = df0.fillna(0)


regions_geo = json.load(open("regions.geojson"))


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
      
    l=list()
    for i in df.resample("M").mean().index.month.unique():
        l.append(df.resample("M").mean()[df.resample("M").mean().index.month == i][filiere])
    ax2.boxplot(l, showfliers=False)
    plt.sca(ax2)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12], ['J', 'F', 'M', 'A','M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    ax2.set_ylabel("Puissance (MW)")
    st.pyplot(fig2)

    
elif choix_menu==parties_menu[2]:
    st.title(parties_menu[2])
    st.info("Le graphique suivant permet de visuliser l'évolution de la consommation et des productions au cours du temps.")
    
    dico = {"3 heures" : "H", "1 jour" : "D", "1 semaine" : "W", "1 mois" : "M"}
    pas = st.selectbox("Choisissez un pas :", options = ['3 heures', '1 jour', '1 semaine', '1 mois']) 
    
    start = st.date_input("Date de début",
     datetime.date(2012, 1, 1))
    
    end = st.date_input("Date de fin",
     datetime.date(2021, 7, 31))
    
    liste_prod = ['Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Bioénergies (MW)']
    
    options = st.multiselect(
     'Choix des filières à visualiser :',
     liste_prod)
    
    liste_graphes =[]
    for i in range(len(options)) :
      liste_graphes.append(options[i])
      
    fig3 = plt.figure(figsize=(15,10))
    ax3 = fig3.add_subplot(111)

    ax3.plot(df.loc[start : end,options].resample(dico[pas]).mean(), label = options)
    ax3.legend()
    ax3.set_xlabel("Temps")
    ax3.set_ylabel("Puissance (MW)")
    ax3.set_title("Consommation et productions lissées par jour (2019)")
    st.pyplot(fig3)
    
elif choix_menu==parties_menu[3]:
    st.title(parties_menu[3])
    st.info("Carte permettant de visualiser la moyenne annuelle de puissance produite par une filière sur une région")
    
    choix_annee = ["2013","2014","2015","2016","2017","2018","2019","2020","2021"]
    annee = st.selectbox("Choisissez une année :", options = choix_annee)
    
    df_reg = df0.copy()
    df_reg = df_reg.loc[str(annee),:]
    df_reg = df_reg.groupby("Région").mean()
    df_reg = round(df_reg,1)
    df_reg["Nom de la région"] = df_reg.index
    
    
    liste_prod = ['Consommation (MW)', 'Gaz (MW)', 'Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)']
    
    filiere_region = st.multiselect(
     'Choix des filières à visualiser :',
     liste_prod)
    
    for i in range(12) :
        nom_region = regions_geo["features"][i]['properties']["nom"]
        regions_geo["features"][i]['properties'][filiere_region] = df[df["Nom de la région"]==nom_region].loc[nom_region,filiere_region]
    
    regions_map = folium.Map(location=[47,1], zoom_start=6, tiles='cartodbpositron')
    
    choropleth = folium.Choropleth(
        geo_data=regions_geo,
        data=df,
        columns=['Nom de la région', filiere_region],
        key_on='feature.properties.nom',
        fill_color='OrRd', 
        fill_opacity=1, 
        line_opacity=1,
        legend_name= filiere_region,
        bins=[int(floor(df[filiere_region].min()/100)*100), 
            int(round((df[filiere_region].min() + (df[filiere_region].max() - df[filiere_region].min())/6)/10,0)*10),
            int(round((df[filiere_region].min() + (df[filiere_region].max() - df[filiere_region].min())*2/6)/10,0)*10),
            int(round((df[filiere_region].min() + (df[filiere_region].max() - df[filiere_region].min())*3/6)/10,0)*10),
            int(round((df[filiere_region].min() + (df[filiere_region].max() - df[filiere_region].min())*4/6)/10,0)*10),
            int(round((df[filiere_region].min() + (df[filiere_region].max() - df[filiere_region].min())*5/6)/10,0)*10),
            int(ceil(df[filiere_region].max()/100)*100)],
        highlight=True,
        smooth_factor=1)
    
    choropleth.add_to(regions_map)
    
    style_function = "font-size: 15px; font-weight: bold"
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(
        fields=['nom',filiere_region], aliases = ['Région :',filiere_region + " :"], labels = True))
    
    folium_static(regions_map)  
