from setuptools import setup, find_packages

setup(
    name="random-compliment-generator",
    version="0.1.0",
    description="Print a random compliment, optionally filtered by category.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "random_compliment_generator=compliment:main",
        ]
    },
    python_requires=">=3.11",
)
