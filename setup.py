from setuptools import setup, find_packages

setup(
    name="proptech-commander",
    version="1.0.0",
    description="A robust data pipeline for real estate market analysis",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "flask",
        "pandas",
        "sqlalchemy",
        "requests",
        "beautifulsoup4",
        "typer",
        "fpdf"
    ],
    entry_points={
        'console_scripts': [
            'proptech=src.api.cli:app',
        ],
    },
)