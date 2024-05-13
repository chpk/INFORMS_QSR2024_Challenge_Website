import os
from PIL import Image, ImageSequence
import numpy as np

def process_image(image_path):
    # Load image
    img = Image.open(image_path)
    # Resize image to 64x64
    img = img.resize((64, 64), Image.ANTIALIAS)
    # Convert image to grayscale
    img = img.convert("L")
    # Convert to binary image
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    return img

def create_gif(images, gif_path):
    # Save images as a gif
    images = [img.convert("P") for img in images]
    # Save images as a gif
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=500, # duration for each frame in milliseconds
        loop=0        # loop=0 means infinite loop
    )

def main(directory_path):
    # Iterate through subdirectories
    gif_count = 0
    for subdir, _, _ in os.walk(directory_path):
        images = []
        # Iterate through image files in subdirectory
        for file_name in sorted(os.listdir(subdir)):
            if file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
                
                image_path = os.path.join(subdir, file_name)
                print(image_path)
                img = process_image(image_path)
                images.append(img)
                # Ensure to not exceed 64 frames
                if len(images) == 64:
                    break
        # Create GIF if there are enough frames
        if len(images) >= 64:
            #gif_path = os.path.join(subdir, str(gif_count)+".gif")
            create_gif(images, "D:/GenAI_data/data/"+str(gif_count)+".gif")
        else:
            print(f"Not enough images in {subdir} to create a GIF")
        gif_count = gif_count+1

if __name__ == "__main__":
    main("D:/GenAI_data/GenAI_dataset_3/")  # Replace path_to_directory with the actual path to your main directory.
