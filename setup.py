from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="microframe",
    version="1.0.0",
    author="Traore Eliezer B.",
    author_email="traoreera@gmail.com",
    description="Un micro-framework ASGI inspiré de FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/traoreera/microframework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "starlette",
        "uvicorn[standard]",
        "pydantic",
        "pydantic-settings",
        "watchdog",
        "python-multipart",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "pytest",
        "pytest-asyncio",
        "httpx",
        "mysql-connector-python",
        "sqlalchemy",
    ],
    extras_require={
        "dev": [
            "pytest>=8.1.1",
            "pytest-asyncio>=0.23.6",
            "httpx>=0.27.0",
            "black>=24.3.0",
            "flake8>=7.0.0",
            "mypy>=1.9.0",
        ],
    },
)
