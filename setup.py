from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    with open('requirements.txt') as f:
        return f.read().splitlines()


setup(
    name='sensor',
    version='0.0.1',
    author='yash',
    author_email='yashskd1026@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)