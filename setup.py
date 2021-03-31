import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='timer_jdu',
    version='0.1.2',
    scripts=['timer_jdu'],
    author="Jean Demeusy",
    author_email="dev.jdu@gmail.com",
    description="A usefull timer package to measure and pack functions' execution time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeandemeusy/timer-jdu-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
