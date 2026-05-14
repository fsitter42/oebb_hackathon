def generate_summary(meta, is_unique, ai_verdict):
    score = 100
    flags = []

    if not is_unique:
        return "🔴 ABGELEHNT", "Dieses Foto ist ein Duplikat eines bereits existierenden Eintrags.", 0
    
    if not meta['lat'] or not meta['lon']:
        score -= 40
        flags.append("Keine GPS-Daten")
    
    if "manipulation" in ai_verdict.lower() or "fake" in ai_verdict.lower():
        score -= 60
        flags.append("KI erkennt Unstimmigkeiten")

    # Status-Logik
    if score >= 90:
        status = "🟢 FREIGEGEBEN"
    elif score >= 50:
        status = "🟡 MANUELLE PRÜFUNG ERFORDERLICH"
    else:
        status = "🔴 VERDACHT AUF BETRUG"

    return status, flags, score