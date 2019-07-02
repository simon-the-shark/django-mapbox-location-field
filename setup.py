import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-mapbox-location-field',
    version='0.1.6',
    packages=["mapbox_location_field"],
    include_package_data=True,
    license='MIT License',
    description='location field with MapInput widget for picking some location',
    long_description=README,
    long_description_content_type="text/markdown",
    download_url="https://github.com/Simon-the-Shark/django-mapbox-location-field/archive/v0.1.6.tar.gz",
    url='https://github.com/Simon-the-Shark/django-mapbox-location-field',
    author='Szymon Kowaliński',
    author_email='simonrekin@gmail.com',
    keywords=['DJANGO', 'WIDGETS', 'LOCATION', 'GEOCODING', "MAP", "FIELDS", "FORMS"],
    install_requires=['django', ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
