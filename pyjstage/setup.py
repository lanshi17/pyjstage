import os
from setuptools import setup, find_packages


def read_requirements():
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements


def read_description():
    desc_path = os.path.join('.', 'README.md')
    with open(desc_path, 'r') as f:
        description = f.read()
    return description


setup(
    name='pyjstage-py312',
    version='0.1.1',
    description='J-STAGE API wrapper for Python - Python 3.12 Compatible',
    long_description=read_description(),
    long_description_content_type="text/markdown",
    author='lanshi17',
    author_email='lanshi17@users.noreply.github.com',
    url='https://github.com/lanshi17/pyjstage',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs', 'crawler')),
    install_requires=read_requirements(),
    python_requires='>=3.12',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    keywords='jstage api wrapper japan science technology academic papers',
    project_urls={
        'Source': 'https://github.com/lanshi17/pyjstage',
        'Original': 'https://github.com/matsurih/pyjstage',
    },
)
