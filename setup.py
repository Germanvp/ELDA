import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elda",
    version="0.0.6",
    author="Juan Manuel Perez & German Villacorta",
    author_email="juanmapf97@gmail.com",
    description="A data analysis focused language built with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Germanvp/ELDA",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="language data project",
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'elda = elda.main:elda',
        ],
    },
    install_requires=['ply']
)
