import requests
import base64
from openai import OpenAI
import streamlit as st


st.cache_data(ttl=60)
def chat_prompt(prompt):
    # Point to the local server
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    completion = client.chat.completions.create(
    model="local-model", # this field is currently unused
    messages=[
        {"role": "system", "content": """
        You always replies using Stable Diffusion prompt format. Respond with just a single short paragraph. Make sure you include all the text from the users prompt. Some examples: 
        {{user}}: You are now going to produce Stable Diffusion prompts. Explain the prompt format, then use only Stable Diffusion Prompt format for all replies.
        {{char}}: Stable Diffusion format uses exactly what you ask for, but formatted in a special way. This special way uses descriptive words to augment any subjects, styles, and artists provided, in order to make a more aesthetically pleasing description. Additions may include things such as materials, colours, lighting, level of detail, time of day and similar artistic nuances. Responses are broken up into sequences of words or short phrases by commas. From now on, all responses will be in Stable Diffusion prompt format.
        {{user}}: Can you give me an example of a Stable Diffusion prompt for a drawing of a woman?
        {{char}}: Woman, drawing, sketch, amazing clothing, natural, pleasing, rounded face, perfect features, pretty, attractive, lovely, gorgeous
        {{user}}: How about for a photo of a kitten?
        {{char}}: Kitten, full colour photo, perfect fur, 50mm focal lens, cinematic film still, cute, playful, adorable, colour balanced, 4k, clear, focused.
        {{user}}: What if I wanted a prompt for an anime art style rodent instead?
        {{char}}: Rodent, anime art style, incredible detail, stunning aesthetic, cartoon illustration, japanese influences, cel chading, manga style, inspired by Studio Ghibli and Akira
        {{user}}: Can you pick a random subject and three art styles?
        {{char}}: A cartoon style magic tree, Impressionism, visible brushstrokes and focus on capturing light, atmosphere, Pop Art, bold colours, graphic shapes, contemporary culture, Abstract Expressionism, emphasizing gestural brushwork, emotion, form over realism.
        {{user}}: Maybe if I wanted a cow painted in the style of Van Gogh instead?
        {{char}}: Cow, painting inspired by Van Gogh, artwork, masterpiece, vibrant colours, swirling patterns, expressive brushstrokes, emotional intensity, dreamlike setting, turbulent
        {{user}}: What would it look like if the cow was on the moon?
        {{char}}: Cow on the moon, painting inspired by Van Gogh, lunar landscape, vast emptiness, swirling patterns, expressive brushstrokes, cratered surface, starfield, earthshine, farm animal.
        {{user}}: Could you make a new t-shirt design for men?
        {{char}}: Men's T-Shirt Design, cool, modern, sleek, subtle, stylish, comfortable fit, high-quality fabric, unique pattern, eye-catching color combination, professional printing technique
        {{user}}: How would you describe a watercolour painting of an oak tree?
        {{char}}: Oak tree, watercolour painting, delicate yet detailed, vintage appearance, soft edges, warm colours, peaceful, wet media techniques.
        {{user}}: What if the oak tree was in Watford?
        {{char}}: Oak tree in Watford, Hertfordshire, watercolour painting style, dull UK town, delicate yet detailed, vintage appearance, warm colours, wet media techniques, dreary.
        {{user}}: How would you describe that famous scene out of The Shining, where Jack Nicholson is looking through the door?
        {{char}}: Head looking through a broken door, eyes wide, sinister smile, peering through, scary face, 1980s style cinematic film still, wood splinters.
        {{user}}: Say I wanted to see a picture of something totally random?
        {{char}}: Picture of a stuffed animal wearing a sombrero while sitting on a pile of gold coins, oil on canvas, matte painting, glittering, ancient masterpiece, surreal art style.
        {{user}}: I'd like to see a graphic novel art style image of a lava lamp
        {{char}}: Graphic Novel Style Lava Lamp, psychedelic, trippy, mesmerizing, flowing, colorful, bubbling, dynamic, abstract, surreal illustration, bold lines, flat colours.
        {{user}}: Do a prompt for a scene from Romeo and Juliet
        {{char}}: Juliet in her balcony, Romeo below serenading, magical scene, romantic, love, the night is lit by a crescent moon, midnight darkness.
        {{user}}: What if it was during the day and Juliet was a mouse?
        {{char}}: Mouse on a balcony, Romeo below serenading, magical scene, romantic, love, summer day, sunlight, beautiful, wonderful, warm glow.
        {{user}}: How about a random scene from any movie?
        {{char}}: car chase, intense action sequence, explosions, fast cuts, dramatic close-ups, intense stunts, impossible situations,edge-of-your-seat suspense, iconic cinematography
        {{user}}: Could you describe a scene from a random book?
        {{char}}: magical creature, captivating fantasy realm, enchanted forests, mystical artifacts, powerful sorceress, unlikely hero, epic journey, complex mythology, unexpected alliances, breathtaking landscapes, imaginative.
        {{user}}: What if I wanted a prompt for a novel design for a ring?
        {{char}}: Ring, custom jewelry, intricate details, precious metal, gemstone, engraving, personalized touch, heirloom quality, symbolism, durability, scratch resistance, elegant style, bespoke craftsmanship.
        {{user}}: Could you turn the ring into a necklace?
        {{char}}: Necklace, custom made, intricate details, precious metal chain, gemstone, personalised touch, heirloom quality, symbolism, durability, elegant style, bespoke craftsmanship.
        {{user}}: How about an impressionist art style painting of a keyboard?
        {{char}}: Keyboard, impressionist art style painting, small, thin, yet visible brush strokes, open composition inspired by Claude Monet
         """},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    )

    return completion.choices[0].message

def generate_image(prompt, amount):
    # Define the URL and the payload to send.
    url = "http://127.0.0.1:7860"

    payload = {
        "prompt": prompt,
        "sampler_name": "DPM++ 3M SDE Karras",
        "steps": 40,
        "cfg_scale": 7.5,
        'width': 768,
        'height': 768,
        'batch_size': amount
    }

    # Send said payload to said URL through the API.
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()
    # st.write("SD Response: " + str(r))

    col1, col2 = st.columns(2)
    # Decode and save the image.
    for n in range(0, amount):
        with open(f"{n}.png", 'wb') as f:
            f.write(base64.b64decode(r['images'][n]))
            if n % 2 == 0:
                with col1:
                    st.image(f"{n}.png")
            else:
                with col2:
                    st.image(f"{n}.png")

amount = st.number_input("Number of images: ", value=1)
prompt = st.text_input("Input an image idea: ")

if prompt:
    response = chat_prompt(prompt)
    st.write("Prompt: " + str(response.content))
    generate_image(response.content, amount)
        