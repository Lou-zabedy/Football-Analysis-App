import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go



st.set_page_config(page_title="Match Analysis", page_icon="📈")
st.markdown(
    """
    <h2 style="text-align: center;">Analyse de match📊</h2>
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
    
    # Filter the DataFrame into three tables based on the Metric column
    defensive_table = df[df.index.isin(defensive_metrics)]
    offensive_table = df[df.index.isin(offensive_metrics)]
    possession_table = df[df.index.isin(possession_metrics)]
    
    # Sum the values across players for each metric (row) for each table
    defensive_sums = defensive_table.sum(axis=1)
    offensive_sums = offensive_table.sum(axis=1)
    possession_sums = possession_table.sum(axis=1)
    
    # Convert Series to DataFrames for styling
    defensive_sums_df = defensive_sums.to_frame(name="Total Defensive Metrics")
    offensive_sums_df = offensive_sums.to_frame(name="Total Offensive Metrics")
    possession_sums_df = possession_sums.to_frame(name="Total Possession Metrics")

    # Convert all values to integers in each DataFrame
    defensive_sums_df = defensive_sums_df.astype(int)
    possession_sums_df = possession_sums_df.astype(int)
    offensive_sums_df = offensive_sums_df.astype(int)
    
    def get_donut_chart(metrics: dict, use_container_width: bool):
        # Convert the metrics dictionary into a DataFrame
        source = pd.DataFrame(list(metrics.items()), columns=["category", "value"])

        # Create the donut chart
        chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="category", type="nominal"),
            tooltip=["category", "value"]
        )

        # Display the chart with Streamlit
        st.altair_chart(chart, use_container_width=use_container_width)

    # Convert offensive sums to a dictionary to pass to the donut chart
    offensive_metrics_dict = offensive_sums_df["Total Offensive Metrics"].to_dict()
    defensive_metrics_dict = defensive_sums_df["Total Defensive Metrics"].to_dict()
    possession_metrics_dict = possession_sums_df["Total Possession Metrics"].to_dict()

    # Display Defensive Metrics with the chart
    st.markdown("### **Métriques Défensives🛡️**")
    st.write("Ces métriques se concentrent sur les actions défensives telles que les tacles, les interceptions et les duels.")
    st.table(defensive_sums_df.style.set_properties(**{'text-align': 'left'}))
    get_donut_chart(defensive_metrics_dict, use_container_width=True)

    # Display Possession Metrics with the chart
    st.markdown("### **Métriques de Possession⚽**")
    st.write("Ces métriques concernent le contrôle du ballon, y compris les pertes de balle et les récupérations de balle.")
    st.table(possession_sums_df.style.set_properties(**{'text-align': 'left'}))
    get_donut_chart(possession_metrics_dict, use_container_width=True)

    # Display Offensive Metrics with the chart
    st.markdown("### **Métriques Offensives🎯**")
    st.write("Ces métriques se concentrent sur les actions offensives telles que les passes décisives, les tirs et les passes.")
    st.table(offensive_sums_df.style.set_properties(**{'text-align': 'left'}))
    get_donut_chart(offensive_metrics_dict, use_container_width=True)
    # Part 2: Match comparison with radar chart
    st.markdown("## Partie 2 : Comparaison entre deux matchs⚖️")

    # File uploader for Match 2
    uploaded_file_2 = st.file_uploader("Choisissez un fichier pour le deuxième match", type=["csv", "xlsx"])

    if uploaded_file and uploaded_file_2:
        # Load second match data
        if uploaded_file_2.name.endswith(".csv"):
            df2 = pd.read_csv(uploaded_file_2)
        elif uploaded_file_2.name.endswith(".xlsx"):
            df2 = pd.read_excel(uploaded_file_2)
        df2.set_index('Metric', inplace=True)
        
        # Metric selection
        st.markdown("### **Sélectionnez les métriques à comparer**")
        all_metrics = list(df.index.intersection(df2.index))  # Ensure metrics exist in both matches
        selected_metrics = st.multiselect(
            "Choisissez les métriques pour la comparaison (radar chart)",
            options=all_metrics,
            default=all_metrics[:5]  # Default selection
        )
        
        if selected_metrics:
            # Prepare data
            match1_data = df.loc[selected_metrics].sum(axis=1)
            match2_data = df2.loc[selected_metrics].sum(axis=1)
            
            radar_df = pd.DataFrame({
                "Metric": selected_metrics,
                "Match 1": match1_data.values,
                "Match 2": match2_data.values
            })
            
            # Radar chart with polygonal format
            fig = go.Figure()

            # Match 1 - Red
            fig.add_trace(go.Scatterpolar(
                r=radar_df["Match 1"],
                theta=radar_df["Metric"],
                fill='toself',
                name='Match 1',
                line_color='red',
                fillcolor='rgba(255, 0, 0, 0.3)'  # Semi-transparent red
                
            ))

            # Match 2 - Blue
            fig.add_trace(go.Scatterpolar(
                r=radar_df["Match 2"],
                theta=radar_df["Metric"],
                fill='toself',
                name='Match 2',
                line_color='blue',
                fillcolor='rgba(0, 0, 255, 0.3)' # Semi-transparent blue
                
            ))

            # Adjust layout for polygonal radar chart
            fig.update_layout(
                polar=dict(
                    angularaxis=dict(linecolor='black', showline=True),  # Straight grid lines
                    radialaxis=dict(visible=True, range=[0, radar_df[["Match 1", "Match 2"]].values.max() + 5]),
                    bgcolor="#f1faee"
                ),
                
                showlegend=True
            )

            # Display in Streamlit
            st.markdown("### **Radar Chart - Comparaison des matchs**")
            st.plotly_chart(fig, use_container_width=True)
            
            # Comparison table
            st.markdown("### **Tableau de comparaison**")
            st.table(radar_df.style.format(precision=0).set_caption("Valeurs des métriques sélectionnées"))


    