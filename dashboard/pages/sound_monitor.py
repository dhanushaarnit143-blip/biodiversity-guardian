import streamlit as st
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def render():
    st.title("🎙️ Sound Monitor")
    st.markdown("Upload audio recordings for species identification")

    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg", "flac"])

    if uploaded_file:
        st.audio(uploaded_file, format="audio/wav")

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = Path(tmp.name)

        if st.button("🔍 Analyze Audio", type="primary"):
            with st.spinner("Processing audio..."):
                try:
                    from audio_processing import AudioPreprocessor, MelSpectrogramExtractor, AudioSpeciesClassifier

                    preprocessor = AudioPreprocessor()
                    extractor = MelSpectrogramExtractor()
                    classifier = AudioSpeciesClassifier()

                    audio = preprocessor.process_to_fixed_length(tmp_path)
                    if audio is not None:
                        features = extractor.extract_to_tensor(audio)
                        result = classifier.predict(tmp_path)

                        st.success("Analysis complete!")

                        st.subheader("Detected Species")
                        species = result.get("species", "Unknown")
                        confidence = result.get("confidence", 0)

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Primary Species", species)
                        with col2:
                            st.metric("Confidence", f"{confidence:.1%}")

                        st.subheader("All Probabilities")
                        probs = result.get("all_probabilities", {})
                        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
                        for sp, prob in sorted_probs[:10]:
                            st.progress(prob, text=f"{sp}: {prob:.1%}")
                    else:
                        st.error("Failed to process audio file")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("About Sound Monitoring")
    st.markdown('''
    Bioacoustic monitoring uses environmental audio to identify wildlife species
    without physical capture or disturbance. The AI analyzes:
    - **Bird calls** and songs
    - **Amphibian vocalizations**
    - **Insect sounds**
    - **Mammal calls**
    ''')