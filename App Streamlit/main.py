import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image
from IPython.core.display import display,HTML
#import seaborn as sns
#import matplotlib.pyplot as plt


image = Image.open("images/food_fact.png")
newsize = (400, 300)
image = image.resize(newsize)
st.image(image,'')


img_a = Image.open("images/da.jpg")
img_b = Image.open("images/db.jpg")
img_c = Image.open("images/dc.jpg")
img_d = Image.open("images/dd.jpg")
img_e = Image.open("images/de.jpg")

st.write("L'application pour bien manger")

#Collecter le profil d'entrée
st.sidebar.header("Les caracteristiques des produits alimentaires")

#--------------------------------------------------------------------------------------------------------------------
def food_caract_entree():
    #categories = st.sidebar.selectbox('Catégorie',('A','B','C','D', 'E'))
    pnns_groups_2 = st.sidebar.selectbox('Catégorie',('Dressings and sauces', 'Biscuits and cakes', 'Fruits', 'Bread',
       'One-dish meals', 'Dairy desserts', 'Sweets',
       'Sweetened beverages', 'Fish and seafood', 'Cheese', 'unknown',
       'Appetizers', 'Salty and fatty products', 'Vegetables',
       'Sandwiches', 'Legumes', 'Unsweetened beverages',
       'Pizza pies and quiches', 'Breakfast cereals', 'Dried fruits',
       'Pastries', 'Cereals', 'Soups', 'Processed meat',
       'Artificially sweetened beverages', 'Milk and yogurt',
       'Plant-based milk substitutes', 'Nuts', 'Fats', 'Meat',
       'Chocolate products', 'Ice cream', 'Waters and flavored waters',
       'Fruit juices', 'Potatoes', 'Offals',
       'Teas and herbal teas and coffees', 'Alcoholic beverages', 'Eggs',
       'Fruit nectars'))
    #nutriscore_score = st.sidebar.slider('Nutriscore',-15,36,30)
    nutriscore_grade = st.sidebar.selectbox('Nutri-grade',('a','b','c','d','e'))
    #ecoscore_score_fr = st.sidebar.slider('Ecoscore',-23,124,75)
    #ecoscore_grade_fr = st.sidebar.selectbox('Eco-grade',('a','b','c','d','e'))
    energy_100g = st.sidebar.slider('Densité énergétique(≤ kJ/100g))',0,3760,3760)
    sugars_100g = st.sidebar.slider('Sucre(≤ g/100g)',0,100,33)
    fat_100g = st.sidebar.slider('Matières grasses(≤ g/100g)',0,100,44)
    saturated_fat_100g = st.sidebar.slider('Acides gras saturés(≤ g/100g)',0,100,40)
    salt_100g  = st.sidebar.slider('Sel(≤ g/100g)',0,100,20)
    sodium_100g = st.sidebar.slider('Sodium(≤ g/100g)',0,100,10)
    fiber_100g = st.sidebar.slider('Fibre(≤ g/100g)',0,100,50)
    carbohydrates_100g = st.sidebar.slider('Glucides(≤ g/100g)',0,100,50)
    proteins_100g = st.sidebar.slider('Protéine(≤ g/100g)',0,100,50)


    data={
        #'categories':categories,
        'pnns_groups_2':pnns_groups_2,
        'energy_100g':energy_100g,
        'sugars_100g':sugars_100g,
        'fat_100g':fat_100g,
        'saturated-fat_100g':saturated_fat_100g,
        'salt_100g':salt_100g,
        'sodium_100g':sodium_100g,
        'fiber_100g':fiber_100g,
        'proteins_100g':proteins_100g,
        'carbohydrates_100g':carbohydrates_100g,
        #'nutriscore_score':nutriscore_score,
        'nutriscore_grade':nutriscore_grade,
        #'ecoscore_score_fr':ecoscore_score_fr,
        #'ecoscore_grade_fr':ecoscore_grade_fr
    }

    food_features = pd.DataFrame(data,index=[0])
    return food_features
#--------------------------------------------------------------------------------------------------------------------

input_df=food_caract_entree()


#Transformer les données d'entrée en données adaptées à notre modèle
#importer la base de données
df=pd.read_csv('df_foods.csv')

columns = ["pnns_groups_2", "energy_100g", "sugars_100g", "saturated-fat_100g",
           "salt_100g", "sodium_100g", "fiber_100g", "proteins_100g", 'nutriscore_grade']

donnee_entree=pd.concat([input_df, df[columns]])

donnee_entree=donnee_entree[:1]

#afficher les données transformées
st.subheader('Les caracteristiques transformés')

st.write("""
<style>

table {
font-size:13px !important;
border:3px solid #6495ed;
border-collapse:collapse;
margin:auto;
}

th {
font-family:monospace bold;
border:1px dotted #6495ed;
background-color:#EFF6FF;
text-align:center;
}
td {
font-family:sans-serif;
font-size:95%;
border:1px solid #6495ed;
text-align:left;
width:auto;
}

.url {
  transition: transform .2s; /* Animation */
  margin: 0 auto;
}

.url:hover {
  transform: scale(3); /* (300% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
}

</style>
</style>
""", unsafe_allow_html=True)

#st.write(donnee_entree.style.set_properties(**{'background-color': 'black','color': 'cyan','border-color': 'white',}))
st.write(HTML(donnee_entree.to_html(escape=False,index=False)),unsafe_allow_html=True)

#Colonnes de sortie
columns_result = ['image_small_url', 'code', 'nutriscore_grade', 'ecoscore_grade_fr', 'nova_group','pnns_groups_2',
                  'product_name', 'energy_100g', 'sugars_100g', 'fat_100g','saturated-fat_100g', 'salt_100g', 'sodium_100g',
                  'fiber_100g', 'proteins_100g', 'carbohydrates_100g', 'nutriscore_score', 'ecoscore_score_fr']

donnee_sortie=pd.DataFrame(df[columns_result])
donnee_sortie = donnee_sortie[(donnee_sortie['pnns_groups_2']==donnee_entree['pnns_groups_2'][0])&
                              (donnee_sortie['energy_100g']<=donnee_entree['energy_100g'][0]) &
                              (donnee_sortie['salt_100g']<=donnee_entree['salt_100g'][0]) &
                              (donnee_sortie['sugars_100g']<=donnee_entree['sugars_100g'][0]) &
                              (donnee_sortie['salt_100g']<=donnee_entree['salt_100g'][0]) &
                              (donnee_sortie['fat_100g']<=donnee_entree['fat_100g'][0]) &
                              (donnee_sortie['saturated-fat_100g']<=donnee_entree['saturated-fat_100g'][0]) &
                              (donnee_sortie['fiber_100g']<=donnee_entree['fiber_100g'][0]) &
                              (donnee_sortie['carbohydrates_100g']<=donnee_entree['carbohydrates_100g'][0]) &
                              (donnee_sortie['proteins_100g']<=donnee_entree['proteins_100g'][0]) &
                              (donnee_sortie['nutriscore_grade'] == donnee_entree['nutriscore_grade'][0])
                              #(donnee_sortie['ecoscore_grade_fr'] == donnee_entree['ecoscore_grade_fr'][0])
].sort_values(by=['nutriscore_grade', 'ecoscore_grade_fr', 'nova_group'],ascending=True)

nb_produit = donnee_sortie.shape[0]
donnee_sortie=donnee_sortie[:30]

st.subheader('Résultat')

def aply_logo_nutri (row):
    img = ''
    if row[0] == 'a':
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Nutri-score-A.svg/120px-Nutri-score-A.svg.png"
    elif  row[0] == 'b':
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nutri-score-B.svg/120px-Nutri-score-B.svg.png"
    elif  row[0] == 'c':
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Nutri-score-C.svg/120px-Nutri-score-C.svg.png"
    elif  row[0] == 'd':
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Nutri-score-D.svg/120px-Nutri-score-D.svg.png"
    elif row[0] == 'e':
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Nutri-score-E.svg/120px-Nutri-score-E.svg.png"
    return img

donnee_sortie['ecoscore_grade_fr'].fillna(value='f', inplace=True)
donnee_sortie['image_small_url'].fillna(value='https://hearhear.org/wp-content/uploads/2019/09/no-image-icon.png', inplace=True)
donnee_sortie['nova_group'].fillna(value=5, inplace=True)
donnee_sortie['nova_group'] = donnee_sortie['nova_group'].apply(np.int64)
donnee_sortie['nova_group'] = donnee_sortie['nova_group'].apply(str)

#----------------------------------------------------------------------------------------------------------------
def aply_logo_eco (row):
    img = ''
    if row[0] == 'a':
        img = "https://static.openfoodfacts.org/images/icons/ecoscore-a.svg"
    elif  row[0] == 'b':
        img = "https://static.openfoodfacts.org/images/attributes/ecoscore-b.svg"
    elif  row[0] == 'c':
        img = "https://fr.openfoodfacts.org/images/icons/ecoscore-c.svg"
    elif  row[0] == 'd':
        img = "https://static.openfoodfacts.org/images/attributes/ecoscore-d.svg"
    elif  row[0] == 'e':
        img = "https://static.openfoodfacts.org/images/attributes/ecoscore-e.svg"
    elif      row[0] == 'f':
        img = "https://static.openfoodfacts.org/images/attributes/ecoscore-unknown.svg"

    return img
#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------
def aply_logo_nova (row):
    img = ''
    if row[0] == '1':
        img = "https://static.openfoodfacts.org/images/attributes/nova-group-1.svg"
    elif  row[0] == '2':
        img = "https://static.openfoodfacts.org/images/attributes/nova-group-2.svg"
    elif  row[0] == '3':
        img = "https://static.openfoodfacts.org/images/attributes/nova-group-3.svg"
    elif  row[0] == '4':
        img = "https://static.openfoodfacts.org/images/attributes/nova-group-4.svg"
    elif  row[0] == '5':
        img = "https://static.openfoodfacts.org/images/attributes/nova-group-unknown.svg"

    return img
#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------
def path_to_image_html(path):
    '''
     This function essentially convert the image url to
     '<img src="'+ path + '"/>' format. And one can put any
     formatting adjustments to control the height, aspect ratio, size etc.
     within as in the below example.
    '''

    return '<img src="'+ path + '" style=max-height:60px;margin-left:auto;margin-right:auto;display:block;"/>'

#----------------------------------------------------------------------------------------------------------------
def path_to_image_url(path):
    '''
     This function essentially convert the image url to
     '<img src="'+ path + '"/>' format. And one can put any
     formatting adjustments to control the height, aspect ratio, size etc.
     within as in the below example.
    '''

    return '<img class="url" src="'+ path + '" style=max-height:60px;margin-left:auto;margin-right:auto;display:block;"/>'
#----------------------------------------------------------------------------------------------------------------

if len(donnee_sortie['nutriscore_grade'])!=0 :
    donnee_sortie['nutriscore_grade'] = donnee_sortie.apply(lambda row : aply_logo_nutri(row['nutriscore_grade']), axis = 1)

#Remplacer NAN avec la valeur la plus frequetes
#df = df.fillna(df['Label'].value_counts().index[0])

if len(donnee_sortie['ecoscore_grade_fr'])!=0 :
    donnee_sortie['ecoscore_grade_fr'] = donnee_sortie.apply(lambda row : aply_logo_eco(row['ecoscore_grade_fr']), axis = 1)

if len(donnee_sortie['nova_group'])!=0 :
    donnee_sortie['nova_group'] = donnee_sortie.apply(lambda row : aply_logo_nova(row['nova_group']), axis = 1)

st.write(nb_produit,': Produit(s)')

if len(donnee_sortie)!=0:
    st.write(HTML(donnee_sortie.to_html(index=False, escape=False, formatters=dict(nutriscore_grade=path_to_image_html,
                                                                                   image_small_url=path_to_image_url,
                                                                                   nova_group=path_to_image_html,
                                                                                   ecoscore_grade_fr=path_to_image_html))))





#importer le modèle
#load_model=pickle.load(open('prevision_credit.pkl','rb'))


#appliquer le modèle sur le profil d'entrée
#prevision=load_model.predict(donnee_entree)

#st.subheader('Résultat de la prévision')
#st.write(prevision)
