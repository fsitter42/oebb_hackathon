import imagehash
from PIL import Image

def get_image_hash(image_file):
    image_file.seek(0)
    img = Image.open(image_file)
    # Erzeugt einen 64-bit "Fingerabdruck" des Motivs
    phash = imagehash.phash(img)
    return str(phash)