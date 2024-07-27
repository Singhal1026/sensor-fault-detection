# To make a sensor package, we need to create a __init__.py file in the sensor directory. This file can be empty, but it must exist for Python to recognize the sensor directory as a package.
from dotenv import load_dotenv
print(f"Reading .env file")
load_dotenv()