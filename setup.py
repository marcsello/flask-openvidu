#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Marcell Pünkösd",
    author_email='punkosdmarcell@rocketmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Adds OpenVidu support to your Flask application",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='flask_openvidu',
    name='flask_openvidu',
    packages=find_packages(include=['flask_openvidu', 'flask_openvidu.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcsello/flask_openvidu',
    project_urls={
        "Documentation": "https://pyopenvidu.readthedocs.io/",
        "Code": "https://github.com/marcsello/pyopenvidu",
        "Issue tracker": "https://github.com/marcsello/pyopenvidu/issues",
    },
    version='0.1.0',
    zip_safe=False,
)
