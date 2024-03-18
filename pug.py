import datetime
import random
import openai
from openai import OpenAI
import json
import requests


from dotenv import load_dotenv
import os

# Load secrets from .env file
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")

client = OpenAI(api_key=OPENAI_KEY)

PUG_FACTS_URL = "https://dogapi.dog/api/v2/breeds/a6ea38ed-f692-478e-af29-378d0e2cc270"


class Pug:
    """Create a PUG with a name, age, home, and time for puppy dinner"""

    def __init__(self, name, age, home, puppy_dinner):
        print(
            f"Creating a PUG with name: {name}, age: {age}, home: {home}, and puppy dinner: {puppy_dinner}."
        )

        self.name = name
        self.age = age
        self.home = home

        try:
            # Try converting age to int
            # Try converting puppy dinner time to datetime
            # If it doesn't work, raise an exception

            self.age = int(age)
            puppy_dinner_format = "%I:%M %p"
            self.puppy_dinner = datetime.datetime.strptime(
                puppy_dinner, puppy_dinner_format
            ).strftime("%H:%M")
            print("PUG created!")

        except ValueError as err:
            raise ValueError(
                f"Error creating PUG with name {self.name}: {err}"
            ) from err

    def describe_pug(self):
        """Return a description of the pug"""

        result = f"{self.name} is a pug who is {self.age} years old and lives in {self.home}."
        return result

    def build_pug(self):

        pug_description = self.describe_pug()

        pug_prompt = f"A cute photo of {self.name}. {pug_description}."

        response = client.images.generate(prompt=pug_prompt, n=1, size="1024x1024")
        image_url = response.data[0].url
        return image_url

    @staticmethod
    def check_for_puppy_dinner(puppy_dinner):
        """Check to see if it's time for puppy dinner
        and return a string"""

        current_time = datetime.datetime.now()
        if puppy_dinner == current_time.strftime("%H:%M"):
            result = f"The current time is {current_time.strftime('%I:%M %p')}. It is time for puppy dinner! 😍"
        else:
            result = f"The current time is {current_time.strftime('%I:%M %p')}. It is not yet time for puppy dinner 😔"
        return result


def get_pug_facts():
    """"Get pug facts from Dog API"""

    pug_breed_response = requests.get(PUG_FACTS_URL)
    pug_breed_facts = json.loads(pug_breed_response.content)["data"]["attributes"]
    pug_weight = float(pug_breed_facts["male_weight"]["max"]) * 2.2046
    pug_facts = {
        "description": pug_breed_facts["description"],
        "max_age": pug_breed_facts["life"]["max"],
        "weight": round(pug_weight),
    }

    return pug_facts


def demo_pug():
    """Demo the pug class"""

    gary = Pug("Gary", "14", "San Francisco", "5:00 PM")
    print(gary.describe_pug())
    print(gary.check_for_puppy_dinner(gary.puppy_dinner))
    print(gary.build_pug())
    gary.drop_it()


if __name__ == "__main__":
    demo_pug()
