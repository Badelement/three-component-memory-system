from setuptools import setup, find_packages

setup(
    name="three-component-memory",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "lancedb>=0.29.0",
        "networkx>=3.6.0",
        "sentence-transformers>=2.2.0",
        "numpy>=1.24.0"
    ],
    description="Three-component memory system for OpenClaw",
    author="OpenClaw Community",
    python_requires=">=3.8",
)
