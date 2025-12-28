from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="medchain-fl",
    version="0.1.0",
    author="MedChain-FL Team",
    author_email="team@medchain-fl.org",
    description="Privacy-preserving federated learning for thalassemia detection with blockchain integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/medchain-fl/medchain-fl",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "medchain-fl-train=scripts.run_local_fl:main",
            "medchain-fl-eval=scripts.evaluate_model:main",
            "medchain-fl-generate=scripts.generate_demo_data:main",
        ],
    },
)
