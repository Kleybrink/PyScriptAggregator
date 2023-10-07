from setuptools import setup, find_packages

setup(
    name="PyScriptAggregator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'tiktoken',
    ],
    entry_points={
        'console_scripts': [
            'sagg=pyscriptaggregator.sagg:main',
        ],
    },
)
