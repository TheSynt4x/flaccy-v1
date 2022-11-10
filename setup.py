import setuptools

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setuptools.setup(
    name="flaccy",
    version="0.1",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "flaccy = main:app",
        ],
    },
    include_package_data=True,
)
