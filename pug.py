import datetime
import random

class Pug:
    """Create a PUG with a name, age, home, and time for puppy dinner"""
    
    def __init__(self, name, age, home, puppy_dinner):
        print(
            f"Creating a PUG with name: {name}, age: {age}, home: {home}, and puppy dinner: {puppy_dinner}.")

        self.name = name
        self.age = age
        self.home = home
        
        try:
            # Try converting age to int
            # Try converting puppy dinner time to datetime
            # If it doesn't work, raise an exception
            
            self.age = int(age)
            puppy_dinner_format = '%I:%M %p'
            self.puppy_dinner = datetime.datetime.strptime(puppy_dinner,
            puppy_dinner_format).strftime("%H:%M")
            print("PUG created!")

        except ValueError as err:
            raise ValueError(f"Error creating PUG with name {self.name}: {err}") from err

    def describe_pug(self):
        """Return a description of the pug"""
        
        result = f"{self.name} is a pug who is {self.age} years old and lives in {self.home}."
        return result
 
    def check_for_puppy_dinner(self):
        """Check to see if it's time for puppy dinner
        and return a string"""
        
        current_time = datetime.datetime.now().strftime("%H:%M")
            
        if self.puppy_dinner == current_time:
            result = f"The current time is {current_time}. It is time for puppy dinner!"
        else:
            result = f"The current time is {current_time}. It is not yet time for puppy dinner."

        return result
    
    def drop_it(self):
        """Command pug to drop whatever is in their mouth!"""

        print("What's in your mouth? Drop it!")
        
        items = ["slice of pizza",
        "poisonous house plant leaf", 
        "tennis ball", 
        "greenie", 
        "router plug", 
        "squeaky toy", 
        "trash"]
        drop_item = random.choice(items)

        print("Good dog!")


def demo_pug():
    """Demo the pug class"""

    gary = Pug("Gary", "14", "San Francisco", "5:00 PM")
    print(gary.describe_pug())
    print(gary.check_for_puppy_dinner())
    gary.drop_it()

    print("**********")
    lily = Pug("Lily", "6", "San Francisco", "5:00")

    print("**********")
    penny = Pug("Penny", "one", "San Francisco", "5:00")

if __name__ == '__main__':
    demo_pug()
