from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="wikipedia-analyzer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A web application that analyzes Wikipedia categories and generates word clouds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wikipedia_analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    include_package_data=True,
)
