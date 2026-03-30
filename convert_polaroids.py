import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

photos = [
    ('photos/IMG_2127.HEIC', 'files/polaroid_1.jpg'),
    ('photos/IMG_6215.HEIC', 'files/polaroid_2.jpg'),
    ('photos/IMG_6746.JPG', 'files/polaroid_3.jpg')
]

for in_path, out_path in photos:
    try:
        print(f"Converting {in_path} to {out_path}...")
        img = Image.open(in_path)
        
        # Resize if too large
        max_size = 1000.0
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        img.save(out_path, "JPEG", quality=85)
        print(f"Saved {out_path}")
    except Exception as e:
        print(f"Failed to process {in_path}: {e}")
