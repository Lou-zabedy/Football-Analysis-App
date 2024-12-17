import streamlit as st

st.set_page_config(page_title='Application-Club Africain', page_icon=
                   'https://upload.wikimedia.org/wikipedia/fr/thumb/3/33/Logo_Club_africain.svg/1200px-Logo_Club_africain.svg.png',
                     layout='wide')

# Put the logo of the club africain as a title or header
logo_url = 'https://upload.wikimedia.org/wikipedia/fr/thumb/3/33/Logo_Club_africain.svg/1200px-Logo_Club_africain.svg.png'
# Custom HTML/CSS for the logo
custom_html = f"""
<div style="text-align: center; margin-top: -20px;">
    <img src="{logo_url}" style="width: 300px;">
</div>
"""
# Display the custom HTML
st.markdown(custom_html, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        #custom-text {
            fontsize=10px;
            padding: 15px; /* Adjust the padding value as needed */
            
        }
        .highlight-text {
            color: #da2c38;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div id="custom-text">
        <span class="highlight-text">Club Africain Analyse</span> est une application en version bêta
        qui permet d'effectuer une analyse des matchs des jeunes joueurs. Elle propose des graphiques visuels
        pour tirer des conclusions sur le rendement de l'équipe, 
        ainsi qu'une analyse des performances des joueurs lors de chaque match.
    </div>
""",
    unsafe_allow_html=True
)
