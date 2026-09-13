import streamlit as st
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def render():
    st.title("📷 Wildlife Monitor")
    st.markdown("Upload camera trap images for species detection")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "bmp"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = Path(tmp.name)

        if st.button("🔍 Detect Wildlife", type="primary"):
            with st.spinner("Running detection..."):
                try:
                    from image_detection import WildlifeDetector, SpeciesIdentifier

                    detector = WildlifeDetector()
                    identifier = SpeciesIdentifier()

                    result = detector.detect_and_count(tmp_path)
                    summary = identifier.get_summary(result)

                    st.success("Detection complete!")

                    st.subheader("Detection Results")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Species", summary["total_species"])
                    with col2:
                        st.metric("Total Individuals", summary["total_individuals"])

                    if result["species_counts"]:
                        st.subheader("Species Counts")
                        for species, info in result["species_counts"].items():
                            st.write(f"**{species}**: {info['count']} (confidence: {info['avg_confidence']:.1%})")

                    if summary["by_category"]:
                        st.subheader("By Taxonomic Category")
                        for cat, info in summary["by_category"].items():
                            st.write(f"**{cat.title()}**: {info['species_count']} species, {info['individuals']} individuals")

                    annotated = detector.annotate_image(tmp_path)
                    st.subheader("Annotated Image")
                    st.image(str(annotated), use_column_width=True)

                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("About Wildlife Detection")
    st.markdown('''
    Camera trap analysis uses computer vision to identify and count wildlife:
    - **Object detection** locates animals in images
    - **Species classification** identifies what was detected
    - **Population counting** tracks animal abundance
    ''')