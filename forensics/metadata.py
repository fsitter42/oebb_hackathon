import exifread

def get_image_metadata(image_file):
    # Springe zum Anfang der Datei
    image_file.seek(0)
    tags = exifread.process_file(image_file, details=False)
    
    metadata = {
        "timestamp": tags.get('EXIF DateTimeOriginal'),
        "lat": None,
        "lon": None
    }

    # GPS Daten extrahieren
    def _to_decimal(values, ref):
        d = float(values[0].num) / float(values[0].den)
        m = float(values[1].num) / float(values[1].den)
        s = float(values[2].num) / float(values[2].den)
        dec = d + (m / 60.0) + (s / 3600.0)
        if ref in ['S', 'W']:
            dec = -dec
        return dec

    if 'GPS GPSLatitude' in tags and 'GPS GPSLatitudeRef' in tags:
        metadata["lat"] = _to_decimal(tags['GPS GPSLatitude'].values, tags['GPS GPSLatitudeRef'].printable)
    if 'GPS GPSLongitude' in tags and 'GPS GPSLongitudeRef' in tags:
        metadata["lon"] = _to_decimal(tags['GPS GPSLongitude'].values, tags['GPS GPSLongitudeRef'].printable)

    return metadata