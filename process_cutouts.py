import os
from PIL import Image
from rembg import remove
from pillow_heif import register_heif_opener

register_heif_opener()

input_dir = 'photos'
output_dir = 'cutouts'

os.makedirs(output_dir, exist_ok=True)

files = os.listdir(input_dir)
for file in files:
    if file.startswith('.'): continue
    input_path = os.path.join(input_dir, file)
    output_path = os.path.join(output_dir, os.path.splitext(file)[0] + '.png')
    
    try:
        print(f"Processing {file}...")
        img = Image.open(input_path)
        output_img = remove(img)
        
        # Calculate bounding box of non-transparent pixels and crop
        bbox = output_img.getbbox()
        if bbox:
            output_img = output_img.crop(bbox)
        
        # Max dimension 800px to save space
        max_size = 800.0
        if max(output_img.size) > max_size:
            ratio = max_size / max(output_img.size)
            new_size = (int(output_img.size[0] * ratio), int(output_img.size[1] * ratio))
            output_img = output_img.resize(new_size, Image.Resampling.LANCZOS)
        
        output_img.save(output_path, "PNG")
        print(f"Saved {output_path}")
    except Exception as e:
        print(f"Error processing {file}: {e}")
