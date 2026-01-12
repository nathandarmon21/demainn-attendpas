"""
Demain N'Attend Pas - Multi-Agent Podcast Assistant
Main Streamlit Application
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Import agents
from agents.short_video_agent import ShortVideoAgent
from agents.seo_agent import SEOAgent
from agents.prep_agent import PrepAgent
from agents.transcript_agent import TranscriptAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Demain N'Attend Pas - Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #FAF7F2;
    }

    /* Headers */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Georgia', serif;
    }
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 2.5rem;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
    }

    /* Upload section styling */
    .upload-section {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E8E4DE;
    }

    /* Buttons */
    .stButton>button {
        background-color: #3498DB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.5rem;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button:hover {
        background-color: #2980B9;
    }

    /* Text areas and inputs */
    .stTextArea textarea, .stTextInput input {
        font-family: 'Courier New', monospace;
        background-color: #FFFFFF;
        border: 1px solid #D5D8DC;
        border-radius: 6px;
    }

    /* Success/Error/Warning boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 8px;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #FFFFFF;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_keys_set' not in st.session_state:
    st.session_state.api_keys_set = False
if 'uploaded_video_path' not in st.session_state:
    st.session_state.uploaded_video_path = None
if 'uploaded_video_name' not in st.session_state:
    st.session_state.uploaded_video_name = None


def check_api_keys():
    """Check if API keys are configured"""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    return (anthropic_key and anthropic_key != "your_claude_api_key_here" and
            openai_key and openai_key != "your_openai_api_key_here")


def main():
    # Header
    st.markdown('<div class="main-header">🎙️ Demain N\'Attend Pas</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Assistant Multi-Agent pour Podcast</div>', unsafe_allow_html=True)

    # Check API keys
    if not check_api_keys():
        st.error("⚠️ API Keys not configured!")
        st.warning("""
        Please set up your API keys:

        1. Copy `.env.example` to `.env`
        2. Add your API keys:
           - ANTHROPIC_API_KEY (Get from: https://console.anthropic.com/settings/keys)
           - OPENAI_API_KEY (Get from: https://platform.openai.com/api-keys)
        3. Restart the application

        Need help? Check the README.md file.
        """)
        return

    # Sidebar
    with st.sidebar:
        # Try to load local logo, fallback to placeholder if not found
        try:
            st.image("assets/logo.png", use_container_width=True)
        except:
            st.markdown("### 🎙️ Demain N'Attend Pas")
        st.markdown("---")
        st.markdown("### 🤖 Agents disponibles")
        st.markdown("""
        - 🎬 **Short Video Agent**: Créer des clips viraux
        - 🔍 **SEO Agent**: Optimiser la découvrabilité
        - 📝 **Transcript Agent**: Nettoyer les transcripts
        - 📚 **Prep Agent**: Préparer les interviews
        """)
        st.markdown("---")
        st.info("💡 Téléchargez votre vidéo ci-dessus, puis utilisez les agents ci-dessous")

    # ========================================
    # CENTRALIZED VIDEO UPLOAD SECTION
    # ========================================
    st.markdown("## 📤 Télécharger votre épisode")

    st.info("💡 **Limite de taille:** Jusqu'à 10 GB. Les fichiers volumineux prendront plus de temps à traiter (env. 10-20 min pour un épisode de 2-4 heures).")

    video_file = st.file_uploader(
        "Téléchargez votre vidéo ou audio d'épisode (tous les agents utiliseront ce fichier)",
        type=['mp4', 'mp3', 'mov'],
        key="centralized_video_upload",
        help="Formats acceptés: MP4, MP3, MOV. Taille max: 10000 MB"
    )

    # Process uploaded video
    if video_file:
        # Save to temporary location and store in session state
        if st.session_state.uploaded_video_name != video_file.name:
            temp_video_path = f"data/temp_{video_file.name}"
            os.makedirs("data", exist_ok=True)

            with open(temp_video_path, "wb") as f:
                f.write(video_file.read())

            st.session_state.uploaded_video_path = temp_video_path
            st.session_state.uploaded_video_name = video_file.name
            st.success(f"✅ Vidéo chargée: {video_file.name}")
        else:
            st.info(f"📹 Vidéo actuelle: {video_file.name}")

    st.markdown("---")

    # ========================================
    # AGENT SECTIONS (Only show if video uploaded)
    # ========================================
    if st.session_state.uploaded_video_path:

        # ========================================
        # SHORT VIDEO AGENT
        # ========================================
        with st.expander("🎬 Short Video Agent - Créer des clips viraux", expanded=False):
            st.markdown("Identifiez et créez des clips viraux à partir de votre épisode complet")

            num_clips = st.slider(
                "Nombre de clips à générer",
                min_value=4,
                max_value=10,
                value=6,
                help="Le nombre de clips courts à créer"
            )

            if st.button("🚀 Générer les clips", type="primary", key="generate_clips"):
                with st.spinner("🎬 Traitement en cours... Cela peut prendre plusieurs minutes."):
                    try:
                        # Run Short Video Agent
                        agent = ShortVideoAgent()
                        generated_clips, posting_instructions = agent.run_full_pipeline(
                            st.session_state.uploaded_video_path,
                            num_clips=num_clips
                        )

                        if generated_clips:
                            st.success(f"✅ {len(generated_clips)} clips générés avec succès!")

                            # Display results
                            st.markdown("### 📦 Clips générés")

                            for i, clip_data in enumerate(generated_clips):
                                with st.expander(f"Clip {i+1}: {clip_data['clip_info']['title']}"):
                                    col1, col2 = st.columns([1, 1])

                                    with col1:
                                        st.video(clip_data['file_path'])

                                    with col2:
                                        st.markdown(f"**Type:** {clip_data['clip_info']['type']}")
                                        st.markdown(f"**Citation:** {clip_data['clip_info']['quote'][:100]}...")
                                        st.markdown(f"**Hashtags:** {' '.join(clip_data['clip_info']['hashtags'])}")

                                    st.download_button(
                                        label=f"📥 Télécharger Clip {i+1}",
                                        data=open(clip_data['file_path'], 'rb').read(),
                                        file_name=f"clip_{i+1}.mp4",
                                        mime="video/mp4",
                                        key=f"download_clip_{i}"
                                    )

                            # Display posting instructions
                            st.markdown("### 📝 Instructions de publication")
                            st.text_area(
                                "Copiez ces instructions pour publier vos clips",
                                posting_instructions,
                                height=400,
                                key="short_video_instructions"
                            )

                        else:
                            st.error("❌ Échec de la génération de clips. Veuillez réessayer.")

                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")

        # ========================================
        # SEO AGENT
        # ========================================
        with st.expander("🔍 SEO Agent - Optimiser la découvrabilité", expanded=False):
            st.markdown("Optimisez la découvrabilité de votre épisode sur toutes les plateformes")

            col1, col2 = st.columns(2)
            with col1:
                guest_name = st.text_input("Nom de l'invité(e) (optionnel)", key="seo_guest_name")
            with col2:
                episode_topic = st.text_input("Sujet de l'épisode (optionnel)", key="seo_episode_topic")

            if st.button("🔍 Générer le package SEO", type="primary", key="generate_seo"):
                with st.spinner("🔍 Analyse SEO en cours..."):
                    try:
                        # Run SEO Agent
                        agent = SEOAgent()
                        formatted_output, seo_package = agent.run_full_analysis(
                            st.session_state.uploaded_video_path,
                            guest_name=guest_name if guest_name else None,
                            episode_topic=episode_topic if episode_topic else None
                        )

                        if formatted_output:
                            st.success("✅ Package SEO généré avec succès!")

                            # Display formatted output
                            st.text_area(
                                "Package SEO complet",
                                formatted_output,
                                height=600,
                                key="seo_package_output"
                            )

                            # Download button for SEO package
                            st.download_button(
                                label="📥 Télécharger le package SEO (JSON)",
                                data=str(seo_package),
                                file_name="seo_package.json",
                                mime="application/json"
                            )

                        else:
                            st.error("❌ Échec de la génération du package SEO")

                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")

        # ========================================
        # TRANSCRIPT AGENT
        # ========================================
        with st.expander("📝 Transcript Agent - Nettoyer les transcripts", expanded=False):
            st.markdown("Générez un transcript propre et professionnel, prêt pour publication")

            col1, col2 = st.columns(2)
            with col1:
                episode_title = st.text_input("Titre de l'épisode (optionnel)", key="transcript_title")
            with col2:
                episode_guest = st.text_input("Nom de l'invité(e) (optionnel)", key="transcript_guest")

            if st.button("📝 Générer le transcript nettoyé", type="primary", key="generate_transcript"):
                with st.spinner("📝 Transcription et nettoyage en cours..."):
                    try:
                        # Run Transcript Agent
                        agent = TranscriptAgent()

                        episode_info = {}
                        if episode_title:
                            episode_info['title'] = episode_title
                        if episode_guest:
                            episode_info['guest'] = episode_guest

                        formatted_output, cleaned_transcript, raw_transcript = agent.run_full_pipeline(
                            st.session_state.uploaded_video_path,
                            episode_info=episode_info if episode_info else None
                        )

                        if formatted_output:
                            st.success("✅ Transcript nettoyé généré avec succès!")

                            # Display cleaned transcript
                            st.markdown("### ✨ Transcript Nettoyé (Prêt pour Publication)")
                            st.text_area(
                                "Transcript nettoyé",
                                formatted_output,
                                height=500,
                                key="transcript_cleaned_output"
                            )

                            # Download button
                            st.download_button(
                                label="📥 Télécharger le transcript nettoyé (.txt)",
                                data=formatted_output,
                                file_name=f"transcript_{episode_title.replace(' ', '_') if episode_title else 'episode'}.txt",
                                mime="text/plain"
                            )

                            # Show raw transcript in expander
                            with st.expander("📄 Voir le transcript brut (avant nettoyage)"):
                                st.text_area(
                                    "Transcript brut",
                                    raw_transcript,
                                    height=400,
                                    key="transcript_raw_output"
                                )

                        else:
                            st.error("❌ Échec de la génération du transcript")

                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")

        # ========================================
        # PREP AGENT
        # ========================================
        with st.expander("📚 Prep Agent - Préparer les interviews", expanded=False):
            st.markdown("Préparez vos interviews avec des ressources ciblées et prioritisées")

            guest_name_prep = st.text_input(
                "Nom de l'invité(e) à préparer",
                placeholder="Ex: Michel Houellebecq",
                key="prep_guest_name"
            )

            additional_context = st.text_area(
                "Contexte additionnel (optionnel)",
                placeholder="Ex: Focus sur son dernier roman, controverses récentes, etc.",
                height=100,
                key="prep_additional_context"
            )

            if st.button("📚 Générer le guide de préparation", type="primary", key="generate_prep"):
                if guest_name_prep:
                    with st.spinner(f"🔍 Recherche en cours sur {guest_name_prep}..."):
                        try:
                            # Run Prep Agent
                            agent = PrepAgent()
                            formatted_guide, prep_package = agent.run_prep_analysis(
                                guest_name_prep,
                                additional_context=additional_context if additional_context else None
                            )

                            if formatted_guide:
                                st.success("✅ Guide de préparation généré!")

                                # Display formatted guide
                                st.text_area(
                                    "Guide de préparation complet",
                                    formatted_guide,
                                    height=600,
                                    key="prep_guide_output"
                                )

                                # Download button
                                st.download_button(
                                    label="📥 Télécharger le guide (JSON)",
                                    data=str(prep_package),
                                    file_name=f"prep_guide_{guest_name_prep.replace(' ', '_')}.json",
                                    mime="application/json"
                                )

                            else:
                                st.error("❌ Échec de la génération du guide")

                        except Exception as e:
                            st.error(f"❌ Erreur: {str(e)}")
                else:
                    st.warning("⚠️ Veuillez entrer le nom d'un invité")

    else:
        st.info("👆 Veuillez d'abord télécharger une vidéo ci-dessus pour utiliser les agents")


if __name__ == "__main__":
    main()
