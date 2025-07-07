from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stockalert",
    version="1.0.0",
    author="StockAlert.pro",
    author_email="support@stockalert.pro",
    description="Official Python SDK for StockAlert.pro API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stockalert/stockalert-python-sdk",
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "typing-extensions>=4.0.0;python_version<'3.8'",
    ],
    extras_require={
        "async": ["httpx>=0.24.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/stockalert/stockalert-python-sdk/issues",
        "Source": "https://github.com/stockalert/stockalert-python-sdk",
        "Documentation": "https://stockalert.pro/api/docs",
    },
)