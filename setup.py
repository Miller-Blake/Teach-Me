import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='teach-me',
    version='1.0.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'teach-me=teach_me.__main__:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI tool that explains code line by line.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/teach-me', # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
