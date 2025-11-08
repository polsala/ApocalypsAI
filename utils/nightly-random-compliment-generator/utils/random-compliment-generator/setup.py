from setuptools import setup, find_packages

setup(
    name="random-compliment-generator",
    version="0.1.0",
    description="Print a random uplifting compliment.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "random-compliment=random_compliment:_main",
        ]
    },
)
