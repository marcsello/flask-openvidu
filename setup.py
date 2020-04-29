#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pyopenvidu>=0.1.3', 'flask']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', 'pytest-mock']

setup(
    author="Marcell Pünkösd",
    author_email='punkosdmarcell@rocketmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Flask',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description="Adds OpenVidu support to your Flask application",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='flask_openvidu',
    name='flask-openvidu',
    packages=find_packages(include=['flask_openvidu', 'flask_openvidu.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcsello/flask-openvidu',
    project_urls={
        "Documentation": "https://flask-openvidu.readthedocs.io/",
        "Code": "https://github.com/marcsello/flask-openvidu",
        "Issue tracker": "https://github.com/marcsello/flask-openvidu",
    },
    version='0.1.0',
    zip_safe=False,
)
