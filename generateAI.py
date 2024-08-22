from random import randint

import google.generativeai as genai
import os

def generate():
    genai.configure(api_key=os.environ["API_KEY"])

    chance = randint(0, 3)

    if chance == 2:
        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(
            "Write a random topic about 3-6 sentences long, as if you were a real person posting to Facebook, "
            "and don't start with 'Just spent' and don't use hashtags")

        return response.text
    else:
        return None