import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enteros-pkg-STANISLAV-PIMENOV",
    version="0.0.1",
    author="STANISLAV-PIMENOV",
    author_email="stanislav-pimenov@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stanislav-pimenov/enteros-bot",
    project_urls={
        "Bug Tracker": "https://github.com/stanislav-pimenov/enteros-bot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)