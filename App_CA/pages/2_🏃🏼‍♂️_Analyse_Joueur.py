import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analyse Joueur", page_icon="📈")
st.markdown(
    """
    <h2 style="text-align: center;">Analyse de joueur🏃🏼‍♂️</h2>
    """,
    unsafe_allow_html=True
)

st.write("")
st.markdown("## Partie 1 : Visualisation les données📈")

# File uploader
uploaded_file = st.file_uploader("Choisissez un fichier", type=["csv", "xlsx"])

if uploaded_file:
    # Check file type and read accordingly
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    
    # Set 'Metric' column as index for easier access to rows
    df.set_index('Metric', inplace=True)

    # Define metric categories (if needed for filtering)
    defensive_metrics = [
        "Dégagement", "tackles", "interceptions", "duel aerien", 
        "duel au sol", "duels total gagnés", "2éme balle", "couverture"
    ]
    
    offensive_metrics = [
        "Assist", "Tirs", "Tirs cadrés", "Jeu de tete offensif", "passes", 
        "passes reussies %", "passes progressives", "passes derniers tiers", 
        "passe zone 14", "passe penalty zone", "Passes en arriére et latérales", 
        "cross", "cross reussi %"
    ]
    
    possession_metrics = [
        "Balles perdue", "contrôle de balle sous pression", 
        "contrôle sans pression", "conduite de balle", "faute commise"
    ]
    
    # User selects metric category
    metric_category = st.selectbox(
        "Select a metric category", 
        ["Defensive Metrics", "Offensive Metrics", "Possession Metrics"]
    )

    # Map category to metric list
    metrics_mapping = {
        "Defensive Metrics": defensive_metrics,
        "Offensive Metrics": offensive_metrics,
        "Possession Metrics": possession_metrics
    }
    selected_metrics = metrics_mapping[metric_category]

    # User selects specific metric
    selected_metric = st.selectbox("Select a metric", selected_metrics)

    if selected_metric in df.index:
        # Get the row for the selected metric
        data = df.loc[selected_metric]

        # Plotting the bar chart with Plotly Express
        fig = px.bar(
            data,
            x=data.index,   # Players or index of the DataFrame
            y=selected_metric,  # Metric selected for comparison
            labels={'x': 'Players', 'y': selected_metric},
            title=f"Comparaison de {selected_metric} entre les joueurs",
            text_auto=True,  # Display values on bars
            color_discrete_sequence=['skyblue']  # Custom color
        )

        # Update layout for better styling
        fig.update_layout(
            title_font_size=16,
            xaxis_title="Joueur",
            yaxis_title="Valeur",
            xaxis_tickangle=45,  # Rotate x-axis labels
            template="simple_white",
            yaxis=dict(gridcolor="lightgray"),  # Add horizontal gridlines
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Metric '{selected_metric}' not found in the data!")

    ################## Player Stats Individual #################################
    
    # Streamlit app layout
    st.markdown("## Partie 2: Statistique de joueur spécifié🏃🏼‍♂️")

    # Player selection (Dropdown for single player)
    selected_player = st.selectbox(
        "Choisis le joueur:",
        options=df.columns,  # Include all player columns
        key="player_select"  # Unique key for the player selectbox
    )

    # Filter data for the selected player
    if selected_player:
        # User selects metric category
        metric_category = st.selectbox(
            "Choisis la catégorie des métriques",
            ["Defensive Metrics", "Offensive Metrics", "Possession Metrics"],
            key="category_metrics"  # Unique key for the category selectbox
        )

        # Map category to metric list
        metrics_mapping = {
            "Defensive Metrics": defensive_metrics,
            "Offensive Metrics": offensive_metrics,
            "Possession Metrics": possession_metrics
        }

        # Get the metrics for the selected category
        selected_metrics = metrics_mapping[metric_category]

        # Filter the DataFrame for the selected metrics and player
        filtered_metrics = [metric for metric in selected_metrics if metric in df.index]  # Ensure valid metrics

        if filtered_metrics:  # Check if the filtered metrics list is not empty
            data = df.loc[filtered_metrics, [selected_player]].reset_index()  # Correctly handle the list

            # Rename columns for easier plotting
            data.columns = ['Metric', 'Value']

            # Plotting the bar chart with Plotly Express
            fig = px.bar(
                data,
                x='Metric',          # Metrics as x-axis
                y='Value',           # Metric values as y-axis
                labels={'Value': 'Stat Value', 'Metric': 'Metrics'},
                title=f"Stats de {selected_player} - {metric_category}",
                text_auto=True,      # Show values on bars
                color_discrete_sequence=['#c1121f']  # Custom color
            )

            # Update layout for better styling
            fig.update_layout(
                title_font_size=16,
                xaxis_title="Metrics",
                yaxis_title="Value",
                xaxis_tickangle=45,  # Rotate x-axis labels for clarity
                template="simple_white",
                yaxis=dict(gridcolor="lightgray"),  # Add horizontal gridlines
            )

            # Display the plot in Streamlit
            st.plotly_chart(fig, use_container_width=True)

        # Optional Button for Comparing Metrics
        
        compare_metrics = st.checkbox("Voulez-vous comparer des métriques spécifiques?", key="compare_metrics_checkbox")

        if compare_metrics:
            # Let the user select multiple metrics
            specified_metrics = st.multiselect(
                "Sélectionnez les métriques à comparer:",
                options=[metric for metric in df.index],  # All available metrics in the DataFrame
                default=None  # No default selection
            )

            if specified_metrics:  # If specific metrics are chosen
                # Filter the data for selected metrics
                compare_data = df.loc[specified_metrics, [selected_player]].reset_index()

                # Rename columns for easier plotting
                compare_data.columns = ['Metric', 'Value']

                # Create a bar chart for metric comparison
                compare_fig = px.bar(
                    compare_data,
                    x='Metric',          # Metrics as x-axis
                    y='Value',           # Metric values as y-axis
                    labels={'Value': 'Stat Value', 'Metric': 'Metrics'},
                    title=f"Comparaison des métriques pour {selected_player}",
                    text_auto=True,      # Show values on bars
                    color_discrete_sequence=['#2a9d8f']  # Custom color
                )

                # Update layout for better styling
                compare_fig.update_layout(
                    title_font_size=16,
                    xaxis_title="Metrics",
                    yaxis_title="Value",
                    xaxis_tickangle=45,  # Rotate x-axis labels for clarity
                    template="simple_white",
                    yaxis=dict(gridcolor="lightgray"),  # Add horizontal gridlines
                )

                # Display the comparison bar chart in Streamlit
                st.plotly_chart(compare_fig, use_container_width=True)
            else:
                st.warning("Veuillez sélectionner des métriques à comparer!")
            
    ################## Radar Chart for Player Comparison ##################
    

    st.markdown("## Partie 3: Comparaison entre deux joueurs 🏃🏼‍♂️🏃")

    # Select two players for comparison
    selected_players = st.multiselect(
        "Choisissez deux joueurs à comparer:",
        options=df.columns,  # List all player columns
        default=df.columns[:2],  # Preselect the first two players
        key="player_multiselect"
    )

    if len(selected_players) == 2:
        # Select multiple metrics for comparison
        selected_metrics = st.multiselect(
            "Sélectionnez plusieurs métriques à comparer",
            options=df.index,  # All available metrics in the DataFrame
            default=df.index[:5]  # Preselect the first five metrics for comparison
        )

        if selected_metrics:
            # Prepare data for comparison
            player1_values = [df.loc[metric, selected_players[0]] for metric in selected_metrics]
            player2_values = [df.loc[metric, selected_players[1]] for metric in selected_metrics]

            # Create columns for the radio buttons
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<style>div[role="radiogroup"] { display: flex; flex-direction: row; }</style>', unsafe_allow_html=True)
                chart_type = st.radio(
                    "Choisissez le type de graphique:",
                    options=["Radar Chart", "Bar Chart"],
                    index=0  # Default to Radar Chart
                )

            if chart_type == "Radar Chart":
                # Create radar chart using Plotly
                fig = go.Figure()

                # Add Player 1
                fig.add_trace(go.Scatterpolar(
                    r=player1_values,
                    theta=selected_metrics,  # Multiple metrics as categories
                    fill='toself',
                    name=selected_players[0],
                    line=dict(color='#1f77b4', width=2)
                ))

                # Add Player 2
                fig.add_trace(go.Scatterpolar(
                    r=player2_values,
                    theta=selected_metrics,
                    fill='toself',
                    name=selected_players[1],
                    line=dict(color='#ff7f0e', width=2)
                ))

                # Update layout for the radar chart
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, max(max(player1_values), max(player2_values))])  # Adjust range based on data
                    ),
                    showlegend=True,
                    title=f"Comparaison entre {selected_players[0]} et {selected_players[1]}",
                )

                # Display radar chart
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Bar Chart":
                # Create bar chart using Plotly Express
                data = pd.DataFrame({
                    'Metric': selected_metrics,
                    selected_players[0]: player1_values,
                    selected_players[1]: player2_values
                })

                # Create bar chart using Plotly Express
                fig = px.bar(data, x='Metric', y=[selected_players[0], selected_players[1]], barmode='group',
                            title=f"Comparaison des métriques entre {selected_players[0]} et {selected_players[1]}")
                
                # Display bar chart
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Veuillez sélectionner au moins une métrique pour la comparaison.")
    else:
        st.warning("Veuillez sélectionner exactement deux joueurs pour comparer.")
else:
    st.warning("Veuillez importer votre data.")