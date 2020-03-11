from setuptools import setup

from drf_custom_related_field import __version__

with open('README.md') as f:
    long_description = f.read()

setup(
    name='drf_custom_related_field',
    version=__version__,
    url='https://github.com/ckkz-it/drf-custom-related-field',
    license='MIT',
    author='Andrey Laguta',
    author_email='cirkus.kz@gmail.com',
    py_modules=['drf_custom_related_field'],
    description=(
        'Custom relation field for django-rest-framework\'s serializers'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=('drf restframework rest_framework django_rest_framework'
              ' serializers drf_custom_related_field'),
    packages=['drf_custom_related_field'],
    install_requires=[
        'django>=2.0',
        'djangorestframework>=3.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
