from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    with open('requirements.txt') as f:
        requirements =  f.read().splitlines()
    # Filter out the editable install entry and return other requirements
    return [req for req in requirements if not req.startswith('-e')]


setup(
    name='sensor',
    version='0.0.1',
    author='yash',
    author_email='yashskd1026@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)