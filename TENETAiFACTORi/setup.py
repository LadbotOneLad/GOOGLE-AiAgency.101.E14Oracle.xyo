"""
Setup for codebecslucky7_codex665

Copyright (c) 2026 Rebecca
Codex 6.65: codebecslucky7 Edition
"""

from setuptools import setup, find_packages

setup(
    name="codebecslucky7-codex665",
    version="1.0.0",
    author="Rebecca",
    author_email="rebecca@lucky7.local",
    description="Codex 6.65: codebecslucky7 Edition — Self-sufficient, geometry-bounded engine",
    long_description=open("codebecslucky7_codex665/REBECCA_BLUEPRINT.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rebecca/codex665",
    packages=find_packages(),
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="codex engine geometry horizon telemetry",
    project_urls={
        "Documentation": "https://github.com/rebecca/codex665",
        "Source": "https://github.com/rebecca/codex665",
    },
)
