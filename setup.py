from setuptools import setup

def get_long_description():
    with open("README.md", 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="tired",
    packages=[
        "tired"
    ],
    include_package_data=True,
    license="MIT",
    description="Boilerplate I'm tired of writing over and over",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/damurashov/TIRED",
    author="Dmitry Murashov",
    setup_requires=["wheel"],
    install_requires=[
        "simple_term_menu",
        "datetime",
        "pyserial",
        "appdirs",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    version="0.3.5",
)

