import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os

st.set_page_config(page_title="Evaluation Joueur", page_icon="📝")
st.markdown(
    """
    <h2 style="text-align: center;">Evaluation de joueur📝</h2>
    """,
    unsafe_allow_html=True
)

# Display all labels (Home Team, Away Team, Category, Date) in the same row
col1, col2, col3, col4 = st.columns(4)

with col1:
    nom = st.text_input("Nom", key="nom")
with col2:
    match = st.text_input("Match", key="match")
with col3:
    categories = ['Ecole B', 'Ecole A', 'Minimes B', 'Minimes A', 'Cadets B', 'Cadets A', 'Juniors', 'Senior B']
    selected_category = st.selectbox("Category", categories, key="category")
with col4:
    # Default value is today's date if not in session_state
    default_date = st.session_state.get('match_date', datetime.date.today())
    if isinstance(default_date, str):
        default_date = datetime.datetime.strptime(default_date, "%Y-%m-%d").date()
    match_date = st.date_input("Date", key="match_date", value=default_date)

############################# Evaluation Technique #####################################################
st.markdown("## 1️⃣Evaluation Technique")

evaluation_labels = [
    "Qualité de la première touche (intention, enchaîner vers l'avant)",
    "Qualité de passes : Précision, dosage, puissance des passes (courte,longue) ",
    "Technique Défensive : Aptitudes aux duels",
    "Sens tactique, vision du jeu",
    "Vitesse de pensée",
    "Anticipation",
    "Adaptation à l’adversaire",
    "Sens du replacement",
    "Sens du démarquage",
    "Sens du marquage",
    "Technique générale",
    "Jeu de tête",
    "Puissance de frappe",
    "Drible et feinte",
    "Technique au poste",
    "Puissance physique",
    "Rapidité"
]

# Create input fields, arranged in rows of 3
evaluation_scores = {}

for i in range(0, len(evaluation_labels), 3):  # Loop through labels in chunks of 3
    cols = st.columns(3)  # Create 3 columns
    for col, label in zip(cols, evaluation_labels[i:i+3]):  # Pair each column with a label
        evaluation_scores[label] = col.number_input(label, min_value=0, max_value=5, value=0, step=1)

# Calculate the average score
total_score = sum(evaluation_scores.values())
num_labels = len(evaluation_labels)
average_score = total_score / num_labels if num_labels > 0 else 0

# Assign an emoji based on the average score
if average_score >= 4:
    emoji = "😊"
elif 2 <= average_score < 4:
    emoji = "😐"
else:
    emoji = "😞"

# Display the average score
st.markdown(f"### Note Moyenne : **{average_score:.2f}** {emoji}")


#st.markdown("### Résumé des évaluations")
# Display results in a table
#st.dataframe(pd.DataFrame(evaluation_scores.items(), columns=["Critère", "Score"]))

############################# Evaluation Tactique #####################################################    

st.markdown("## 2️⃣Evaluation Tactique")
evaluation_labels_2 = [
    "Intelligence de jeu: jouer, faire jouer",
    "Disponibilité",
    "Jouer vers l'avant",
    "Jouer dans le dos des adversaires",
    "Capacité à changer le rythme"
    
]
# Create input fields, arranged in rows of 3
evaluation_scores_2 = {}

for i in range(0, len(evaluation_labels_2), 3):  # Loop through labels in chunks of 3
    cols = st.columns(3)  # Create 3 columns
    for col, label in zip(cols, evaluation_labels_2[i:i+3]):  # Pair each column with a label
        evaluation_scores_2[label] = col.number_input(label, min_value=0, max_value=5, value=0, step=1)

# Calculate the average score
total_score = sum(evaluation_scores_2.values())
num_labels = len(evaluation_labels_2)
average_score_2 = total_score / num_labels if num_labels > 0 else 0

# Assign an emoji based on the average score
if average_score_2 >= 4:
    emoji = "😊"
elif 2 <= average_score_2 < 4:
    emoji = "😐"
else:
    emoji = "😞"

# Display the average score
st.markdown(f"### Note Moyenne : **{average_score_2:.2f}** {emoji}")



############################# Evaluation comportementale #####################################################  
st.markdown("## 3️⃣Evaluation Comportementale")
evaluation_labels_3 = [
    "Assiduité",
    "Motivation et volonté",
    "Confiance / Prise de risque",
    "Calme et maitrise de soi",
    "Combativité",
    "Sportivité",
    "Amabilité"
]
# Create input fields, arranged in rows of 3
evaluation_scores_3 = {}

for i in range(0, len(evaluation_labels_3), 3):  # Loop through labels in chunks of 3
    cols = st.columns(3)  # Create 3 columns
    for col, label in zip(cols, evaluation_labels_3[i:i+3]):  # Pair each column with a label
        evaluation_scores_3[label] = col.number_input(label, min_value=0, max_value=5, value=0, step=1)

# Calculate the average score
total_score = sum(evaluation_scores_3.values())
num_labels = len(evaluation_labels_3)
average_score_3 = total_score / num_labels if num_labels > 0 else 0

# Assign an emoji based on the average score
if average_score_3 >= 4:
    emoji = "😊"
elif 2 <= average_score_3 < 4:
    emoji = "😐"
else:
    emoji = "😞"

# Display the average score
st.markdown(f"### Note Moyenne : **{average_score_3:.2f}** {emoji}")

##################### Download a csv file ####################################
# Prepare data for the CSV file
player_data = {
    "Nom": [nom],
    "Match": [match],
    "Category": [selected_category],
    "Date": [match_date],
    "Note Moyenne Technique": [round(average_score, 2)],
    "Note Moyenne Tactique": [round(average_score_2, 2)],
    "Note Moyenne Comportementale": [round(average_score_3, 2)],
}

# Combine all the scores
player_data.update(evaluation_scores)
player_data.update(evaluation_scores_2)
player_data.update(evaluation_scores_3)

# Create a DataFrame
player_df = pd.DataFrame(player_data)

# Button to download the data as a CSV file
csv = player_df.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="📥 Save as CSV",
    data=csv,
    file_name=f"evaluation_{nom.replace(' ', '_')}_{match_date}.csv",
    mime="text/csv"
)

####################### Radar chart comparaison ###############################
# Radar Chart for Average Scores
categories = [
    "Technique",
    "Tactique",
    "Comportementale"
]

# Average values for the three categories
values = [
    average_score,  # Technique
    average_score_2,  # Tactique
    average_score_3,  # Comportementale
]

# Complete the radar chart loop (Plotly expects it)
values += values[:1]
categories += categories[:1]

# Create the radar chart
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Average Notes',
    line=dict(color='rgba(234, 17, 17, 0.8)', width=2)
))

# Set the chart limits and appearance
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5],  # Min 0, Max 5
            tickmode="array",
            tickvals=[0, 1, 2, 3, 4, 5],
            ticktext=["0", "1", "2", "3", "4", "5"],
            color="black",
            gridcolor="rgba(0, 0, 0, 0.1)",
        ),
        angularaxis=dict(
            color="#ffffff",  # Set angular axis labels to black
        ),
    ),
    showlegend=False,
    #title="Comparaison des Notes Moyennes"
)

# Display the radar chart in Streamlit
st.markdown("## 4️⃣Comparaison des Notes Moyennes 🎯")
st.plotly_chart(fig)


