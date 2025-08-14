import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from datetime import datetime
import os
from PIL import Image

torch.set_num_threads(os.cpu_count())

def jarvis_speak(text):
    print(f"[JARVIS] {text}")
    # Hook into your TTS if needed

# Force CPU mode
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Use float32 for CPU compatibility
jarvis_speak("Initializing image generator for CPU use...")

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float32
).to("cpu")

img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float32
).to("cpu")

def generate_image(prompt=None, negative_prompt=None):
    if prompt is None:
        jarvis_speak("What should I generate?")
        prompt = input("You: ")

    if negative_prompt is None:
        jarvis_speak("Anything you'd like me to avoid, sir?")
        negative_prompt = input("Avoid: ")

    jarvis_speak("Generating image now. This may take 3–10 minutes on CPU...")

    try:
        result = pipe(prompt=prompt, negative_prompt=negative_prompt)
        image = result.images[0]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"JARVIS_generated_{timestamp}.png"
        output_dir = "output_images"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        image.save(filepath)

        jarvis_speak(f"Done, sir. Image saved as {filename}")
        return filepath

    except Exception as e:
        jarvis_speak(f"Image generation failed: {e}")
        return None

def edit_image(image_path, prompt=None, negative_prompt=None, strength=0.7):
    if not os.path.isfile(image_path):
        jarvis_speak("Image file not found.")
        return None

    if prompt is None:
        jarvis_speak("What edits should I apply?")
        prompt = input("You: ")

    if negative_prompt is None:
        jarvis_speak("Anything you'd like me to avoid, sir?")
        negative_prompt = input("Avoid: ")

    jarvis_speak("Editing image now. This may take 3–10 minutes on CPU...")

    try:
        init_image = Image.open(image_path).convert("RGB")

        result = img2img_pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=init_image,
            strength=strength
        )
        edited_image = result.images[0]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"JARVIS_edited_{timestamp}.png"
        output_dir = "output_images"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        edited_image.save(filepath)

        jarvis_speak(f"Done, sir. Edited image saved as {filename}")
        return filepath

    except Exception as e:
        jarvis_speak(f"Image editing failed: {e}")
        return None
