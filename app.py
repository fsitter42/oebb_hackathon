import streamlit as st
from forensics.ela import run_ela
from PIL import Image
from forensics.metadata import get_image_metadata
from forensics.hashing import get_image_hash
import os
from forensics.database import init_db, check_and_store_hash
from forensics.hashing import get_image_hash

init_db()

def save_uploaded_file(uploaded_file):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    path = os.path.join("uploads", uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

st.set_page_config(page_title="ÖBB Integrity Audit", layout="wide")

st.title("🏗️ ÖBB Construction Photo Audit")
st.write("Lade ein Baustellenfoto hoch, um es auf Manipulation zu prüfen.")

uploaded_file = st.file_uploader("Bild auswählen...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Bilder nebeneinander anzeigen
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Original")
        st.image(uploaded_file, use_container_width=True)
    
    with col2:
        st.header("ELA Analysis (Forensik)")
        with st.spinner('Berechne ELA...'):
            ela_result = run_ela(uploaded_file)
            st.image(ela_result, use_container_width=True)
            st.info("Helle Bereiche deuten auf höhere Fehlerstufen (mögliche Manipulation) hin.")


    st.divider()
    st.header("📍 Standort- & Zeit-Check")
    
    meta = get_image_metadata(uploaded_file)
    
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.metric("Datum/Zeit", str(meta['timestamp']) if meta['timestamp'] else "Keine Daten")
    
    with m_col2:
        st.metric("Latitude", f"{meta['lat']:.5f}" if meta['lat'] else "Nicht verfügbar")
    
    with m_col3:
        st.metric("Longitude", f"{meta['lon']:.5f}" if meta['lon'] else "Nicht verfügbar")

    if meta['lat'] and meta['lon']:
        # Ein kleiner interaktiver Punkt auf der Karte
        map_data = [{"lat": meta['lat'], "lon": meta['lon']}]
        st.map(map_data)
    else:
        st.warning("⚠️ Achtung: Keine GPS-Daten im Bild gefunden. Möglicher Betrugsversuch oder Metadaten wurden gelöscht!")

    phash_value = get_image_hash(uploaded_file)
    is_unique, original_file = check_and_store_hash(uploaded_file.name, phash_value)
    
    if not is_unique:
        st.error(f"❌ BETRUGSVERDACHT: Dieses Motiv wurde bereits hochgeladen!")
        st.warning(f"Ursprünglicher Dateiname: {original_file}")
        st.toast("Duplikat erkannt!", icon="🚨")
    else:
        st.success("✅ Bild-Fingerabdruck ist neu. Foto wurde im Audit-Log registriert.")
    st.sidebar.header("🔍 Bild-Fingerabdruck")
    st.sidebar.code(phash_value, language=None)
    st.sidebar.info("Dieser Hash identifiziert das Motiv. Gleiche Hashes = Gleiches Foto!")

    file_path = save_uploaded_file(uploaded_file)
    st.sidebar.success(f"Gespeichert unter: {file_path}")

        