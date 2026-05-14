from PIL import Image, ImageChops
import os

def run_ela(image_path, quality=90):
    original = Image.open(image_path).convert('RGB')
    
    # Temporärer Pfad
    resaved_path = "temp_resaved.jpg"
    original.save(resaved_path, 'JPEG', quality=quality)
    resaved = Image.open(resaved_path)
    
    # Differenz berechnen
    ela_image = ImageChops.difference(original, resaved)
    
    # Kontrast verstärken
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0: max_diff = 1
    scale = 255.0 / max_diff
    
    ela_image = ImageChops.multiply(ela_image, Image.new('RGB', ela_image.size, (int(scale), int(scale), int(scale))))
    
    # Cleanup: Temporäre Datei löschen (optional)
    if os.path.exists(resaved_path):
        os.remove(resaved_path)
        
    return ela_image