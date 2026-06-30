#!/usr/bin/env python

"""The setup script for care_notifications — Notifications plug for CARE."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "django",
    "djangorestframework",
    "celery",
    "django-environ",
    "pywebpush",
]

test_requirements = []

setup(
    author="Open Healthcare Network",
    author_email="info@ohc.network",
    python_requires=">=3.13",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
    ],
    description="Notifications plug for CARE — booking SMS and in-app notifications for clinical events.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="care_notifications",
    name="care_notifications",
    packages=find_packages(include=["care_notifications", "care_notifications.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ohcnetwork/care_notifications_be",
    version="0.1.0",
    zip_safe=False,
)
