#!/usr/bin/env python

"""The setup script for booking_notifications — Booking Notifications plug for CARE."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "django",
    "djangorestframework",
    "celery",
    "django-environ",
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
    description="Booking Notifications plug for CARE — sends booking confirmations and pre-appointment reminders via SMS and email.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="booking_notifications",
    name="booking_notifications",
    packages=find_packages(include=["booking_notifications", "booking_notifications.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/ohcnetwork/care_booking_notifications_be",
    version="0.1.0",
    zip_safe=False,
)
