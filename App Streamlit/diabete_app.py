import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image
from IPython.core.display import display,HTML



image = Image.open("images/da.png")
newsize = (212, 116)
image = image.resize(newsize)
st.image(image,'')

st.subheader("Mon application DIABETE-SCORE")


#Style CSS
st.write("""
<style>

table {
font-size:13px !important;
border:3px solid #6495ed;
border-collapse:collapse;
margin:auto;
width: auto;
height: auto;
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
height:60px;
}

.url {
  height:60px;
  margin-left:auto;
  margin-right:auto;
  display:block;
  -webkit-transform: scale(1.05);
  -moz-transform: scale(1.05);
  -o-transform: scale(1.05);
  transform: scale(1.05);

  -webkit-transition: all 700ms ease-in-out;
  -moz-transition: all 700ms ease-in-out;
  -o-transition: all 700ms ease-in-out;
  transition: all 700ms ease-in-out;
}

td:hover {
  font-family:sans-serif;
  /*font-weight: bolder; */
  font-size:120%;
  background-color: #f4f4f4;
  }


td:hover .url {
  /*-ms-transform: scale(1) translate(0px);*/ /* IE 9 */
  /*-webkit-transform: scale(1) translate(0px);*/ /* Safari 3-8 */
  /*transform: scale(1);*/ /* (200% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
  width:auto;
  height:250px;
}

</style>
""", unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------------
def food_caract_entree():
    code = st.text_input("Entrer le code barre", 3560071083472)


    data={
        'code':code,
    }

    food_features = pd.DataFrame(data,index=[0])
    return food_features
#--------------------------------------------------------------------------------------------------------------------

input_df=food_caract_entree()


#Transformer les données d'entrée en données adaptées à notre modèle
#importer la base de données
df=pd.read_csv('df_food.csv')

columns = ["code", "energy_100g", "sugars_100g", "saturated_fat_100g",
           "salt_100g", "sodium_100g", "fiber_100g", "proteins_100g"]

donnee_entree=pd.concat([input_df, df[columns]])

donnee_entree=donnee_entree[:1]


columns_result = ['image_url', 'code', 'product_name','pnns_groups_2', 'nutriscore_grade',
                  'ecoscore_grade_fr', 'nova_group', 'sugars_100g']

donnee_entree['code'] = donnee_entree['code'].apply(str)
donnee_sortie=pd.DataFrame(df[columns_result])

var_code = donnee_entree['code'][0]

donnee_sortie['code'] = donnee_sortie['code'].apply(str)
donnee_sortie = donnee_sortie[(donnee_sortie['code']==var_code)].sort_values(by=['nutriscore_grade', 'nova_group', 'ecoscore_grade_fr'],ascending=True)

nb_produit = donnee_sortie.shape[0]

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



def aply_logo_diabete (row):
    img = ''

    if row[0] == 'A':
        img = "https://i.ibb.co/rxr8t1Z/da.png"
    elif  row[0] == 'B':
        img = "https://i.ibb.co/0JCPN58/db.png"
    elif  row[0] == 'C':
        img = "https://i.ibb.co/42V7Sfd/dc.png"
    elif  row[0] == 'D':
        img = "https://i.ibb.co/CBd5jnN/dd.png"
    elif row[0] == 'E':
        img = "https://i.ibb.co/4ZDx6Dj/de.png"
    return img

donnee_sortie['ecoscore_grade_fr'].fillna(value='f', inplace=True)
donnee_sortie['image_url'].fillna(value='https://hearhear.org/wp-content/uploads/2019/09/no-image-icon.png', inplace=True)
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
    elif row[0] == 'f':
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

    return '<div class ="image" ><img class="url" src="'+ path + '""/></div>'
#----------------------------------------------------------------------------------------------------------------

if len(donnee_sortie['nutriscore_grade'])!=0 :
    donnee_sortie['nutriscore_grade'] = donnee_sortie.apply(lambda row : aply_logo_nutri(row['nutriscore_grade']), axis = 1)

#Remplacer NAN avec la valeur la plus frequetes
#df = df.fillna(df['Label'].value_counts().index[0])

if len(donnee_sortie['ecoscore_grade_fr'])!=0 :
    donnee_sortie['ecoscore_grade_fr'] = donnee_sortie.apply(lambda row : aply_logo_eco(row['ecoscore_grade_fr']), axis = 1)

if len(donnee_sortie['nova_group'])!=0 :
    donnee_sortie['nova_group'] = donnee_sortie.apply(lambda row : aply_logo_nova(row['nova_group']), axis = 1)


#Colonnes de sortie
columns_suggestion = ['image_url', 'code', 'product_name', 'nutriscore_grade', 'nova_group', 'ecoscore_grade_fr',
                      'sugars_100g', 'pnns_groups_2', 'fat_100g', 'proteins_100g', 'carbohydrates_100g']

donnee_suggerer =pd.DataFrame(df[columns_suggestion])
pd.options.display.float_format = '{:.2f}'.format

def repere_quantite(df):
    donnee_suggerer['quantite_lipide'] = ''
    donnee_suggerer['quantite_glucide'] = ''
    donnee_suggerer['quantite_proteine'] = ''
    donnee_suggerer['quantite_sucre'] = ''
    donnee_suggerer['nutrigrade'] = ''
    donnee_suggerer['nova'] = ''
    donnee_suggerer['ecograde'] = ''


    df.loc[df.eval("sugars_100g <= 3"), "quantite_sucre"] = "Faible"
    df.loc[df.eval("sugars_100g > 3"), "quantite_sucre"] = "Moderee"
    df.loc[df.eval("sugars_100g > 10"), "quantite_sucre"] = "Elevee"

    df.loc[df.eval("carbohydrates_100g <= 5"), "quantite_glucide"] = "Faible"
    df.loc[df.eval("carbohydrates_100g > 5"), "quantite_glucide"] = "Moderee"
    df.loc[df.eval("carbohydrates_100g > 20"), "quantite_glucide"] = "Elevee"

    df.loc[df.eval("fat_100g <= 3"), "quantite_lipide"] = "Faible"
    df.loc[df.eval("fat_100g > 3"), "quantite_lipide"] = "Moyenne"
    df.loc[df.eval("fat_100g > 10"), "quantite_lipide"] = "Elevee"

    df.loc[df.eval("proteins_100g <= 5"), "quantite_proteine"] = "Faible"
    df.loc[df.eval("proteins_100g > 5"), "quantite_proteine"] = "Moderee"
    df.loc[df.eval("proteins_100g > 20"), "quantite_proteine"] = "Elevee"

    df.loc[df.eval("nutriscore_grade == 'd'"), "nutrigrade"] = "Faible"
    df.loc[df.eval("nutriscore_grade == 'e'"), "nutrigrade"] = "Faible"
    df.loc[df.eval("nutriscore_grade == 'b'"), "nutrigrade"] = "Moderee"
    df.loc[df.eval("nutriscore_grade == 'c'"), "nutrigrade"] = "Moderee"
    df.loc[df.eval("nutriscore_grade == 'a'"), "nutrigrade"] = "Elevee"

    df.loc[df.eval("nova_group == 4"), "nova"] = "Faible"
    df.loc[df.eval("nova_group == 3"), "nova"] = "Moderee"
    df.loc[df.eval("nova_group == 2"), "nova"] = "Moderee"
    df.loc[df.eval("nova_group == 1"), "nova"] = "Elevee"

    df.loc[df.eval("ecoscore_grade_fr == 'd'"), "ecograde"] = "Faible"
    df.loc[df.eval("ecoscore_grade_fr == 'e'"), "ecograde"] = "Faible"
    df.loc[df.eval("ecoscore_grade_fr == 'b'"), "ecograde"] = "Moderee"
    df.loc[df.eval("ecoscore_grade_fr == 'c'"), "ecograde"] = "Moderee"
    df.loc[df.eval("ecoscore_grade_fr == 'a'"), "ecograde"] = "Elevee"

    return df



donnee_suggerer['note_lipide'] = 0
donnee_suggerer['note_glucide'] = 0
donnee_suggerer['note_proteine'] = 0
donnee_suggerer['note_sucre'] = 0
donnee_suggerer['note_nutrigrade'] = 0
donnee_suggerer['note_nova'] = 0
donnee_suggerer['note_ecograde'] = 0

donnee_suggerer['Diabete_score'] = 0

donnee_suggerer['Diabete_grade'] = ''

def note_produit(df):

  df.loc[df.eval("quantite_sucre == 'Faible'"), "note_sucre"] =10
  df.loc[df.eval("quantite_sucre == 'Moderee'"), "note_sucre"] =1
  df.loc[df.eval("quantite_sucre == 'Elevee'"), "note_sucre"] =1

  df.loc[df.eval("quantite_glucide == 'Faible'"), "note_glucide"] =5
  df.loc[df.eval("quantite_glucide == 'Moderee'"), "note_glucide"] =10
  df.loc[df.eval("quantite_glucide == 'Elevee'"), "note_glucide"] =1

  df.loc[df.eval("quantite_lipide == 'Faible'"), "note_lipide"] =10
  df.loc[df.eval("quantite_lipide == 'Moderee'"), "note_lipide"] =5
  df.loc[df.eval("quantite_lipide == 'Elevee'"), "note_lipide"] =1

  df.loc[df.eval("quantite_proteine == 'Faible'"), "note_proteine"] =5
  df.loc[df.eval("quantite_proteine == 'Moderee'"), "note_proteine"] =10
  df.loc[df.eval("quantite_proteine == 'Elevee'"), "note_proteine"] =5

  df.loc[df.eval("nutrigrade == 'Faible'"), "note_nutrigrade"] =1
  df.loc[df.eval("nutrigrade == 'Moderee'"), "note_nutrigrade"] =5
  df.loc[df.eval("nutrigrade == 'Elevee'"), "note_nutrigrade"] =10

  df.loc[df.eval("nova == 'Faible'"), "note_nova"] =1
  df.loc[df.eval("nova == 'Moderee'"), "note_nova"] =5
  df.loc[df.eval("nova == 'Elevee'"), "note_nova"] =10

  df.loc[df.eval("ecograde == 'Faible'"), "note_ecograde"] =1
  df.loc[df.eval("ecograde == 'Moderee'"), "note_ecograde"] =5
  df.loc[df.eval("ecograde == 'Elevee'"), "note_ecograde"] =10

  df["Diabete_score"] = round((df["note_sucre"]*3 + df["note_glucide"]*2 + df["note_lipide"] + df["note_proteine"]*3 +
                       df["note_nutrigrade"]*3 + df["note_nova"]*2 + df["note_ecograde"])/7,2)

  df.loc[df.eval("Diabete_score <=4"), "Diabete_grade"] = "E"
  df.loc[df.eval("Diabete_score >4"), "Diabete_grade"] = "D"
  df.loc[df.eval("Diabete_score >8"), "Diabete_grade"] = "C"
  df.loc[df.eval("Diabete_score >12"), "Diabete_grade"] = "B"
  df.loc[df.eval("Diabete_score >=16"), "Diabete_grade"] = "A"


  return df



repere_quantite(donnee_suggerer)

note_produit(donnee_suggerer)

if len(donnee_sortie)!=0:

    donnee_suggerer['code'] = donnee_suggerer['code'].apply(str)
    donnee_suggerer['ecoscore_grade_fr'].fillna(value='f', inplace=True)
    donnee_suggerer['image_url'].fillna(value='https://hearhear.org/wp-content/uploads/2019/09/no-image-icon.png',
                                        inplace=True)
    donnee_suggerer['nova_group'].fillna(value=5, inplace=True)
    donnee_suggerer['nova_group'] = donnee_suggerer['nova_group'].apply(np.int64)
    donnee_suggerer['nova_group'] = donnee_suggerer['nova_group'].apply(str)

    donnee_diabete = donnee_suggerer[['image_url', 'product_name', 'pnns_groups_2', 'nutriscore_grade', 'nova_group',
                                      'ecoscore_grade_fr','Diabete_grade',
                                      'sugars_100g']][(donnee_suggerer['code'] == var_code)]

    donnee_suggerer = donnee_suggerer[['image_url', 'code', 'product_name', 'pnns_groups_2', 'Diabete_score', 'Diabete_grade',
                                       'sugars_100g']][(donnee_suggerer['pnns_groups_2'] == donnee_sortie['pnns_groups_2'].values[0])
    ].sort_values(by=['Diabete_score'],ascending=False)


    nb_produit = donnee_suggerer.shape[0]
    donnee_suggerer=donnee_suggerer[:100]
#Remplacer les nan
    donnee_suggerer['image_url'].fillna(value='https://hearhear.org/wp-content/uploads/2019/09/no-image-icon.png',
                                            inplace=True)

    if len(donnee_suggerer['Diabete_grade'])!=0 :
        donnee_suggerer['Diabete_grade'] = donnee_suggerer.apply(lambda row : aply_logo_diabete(row['Diabete_grade']), axis = 1)

        donnee_diabete['Diabete_grade'] = donnee_diabete.apply(lambda row : aply_logo_diabete(row['Diabete_grade']), axis = 1)

    if len(donnee_diabete['nutriscore_grade']) != 0:
        donnee_diabete['nutriscore_grade'] = donnee_diabete.apply(lambda row: aply_logo_nutri(row['nutriscore_grade']),axis=1)

    if len(donnee_diabete['ecoscore_grade_fr']) != 0:
        donnee_diabete['ecoscore_grade_fr'] = donnee_diabete.apply(lambda row: aply_logo_eco(row['ecoscore_grade_fr']),axis=1)

    if len(donnee_diabete['nova_group']) != 0:
        donnee_diabete['nova_group'] = donnee_diabete.apply(lambda row: aply_logo_nova(row['nova_group']), axis=1)

    st.subheader('Produit sélectionné')

    if len(donnee_sortie) != 0:
        st.write(
            HTML(donnee_diabete.to_html(index=False, escape=False, formatters=dict(nutriscore_grade=path_to_image_html,
                                                                                   image_url=path_to_image_url,
                                                                                   nova_group=path_to_image_html,
                                                                                   ecoscore_grade_fr=path_to_image_html,
                                                                                   Diabete_grade=path_to_image_html))))
    # Produit Proposés
    st.subheader('Les Produits proposés pour les diabétiques')

    st.write(nb_produit,': Produit(s)')


    if len(donnee_suggerer)!=0:
        st.write(
            HTML(donnee_suggerer.to_html(index=False, escape=False, formatters=dict(nutriscore_grade=path_to_image_html,
                                                                                    image_url=path_to_image_url,
                                                                                    nova_group=path_to_image_html,
                                                                                    ecoscore_grade_fr=path_to_image_html,
                                                                                    Diabete_grade=path_to_image_html))))



#importer le modèle
#load_model=pickle.load(open('prevision_credit.pkl','rb'))


#appliquer le modèle sur le profil d'entrée
#prevision=load_model.predict(donnee_entree)

#st.subheader('Résultat de la prévision')
#st.write(prevision)
