from setuptools import setup

setup(
    name="tired",
    packages=[
        "tired"
    ],
    include_package_data=True,
    license="MIT",
    description="Boilerplate I'm tired of writing over and over",
    author="Dmitry Murashov",
    setup_requires=["wheel"],
    install_requires=[
        "simple_term_menu"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Inependent",
    ],
    python_requires=">=3.7",
    version="0.0.1",
)

