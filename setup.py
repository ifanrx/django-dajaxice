from setuptools import find_packages, setup
import dajaxice

setup(
    name='django-dajaxice-ng',
    version=dajaxice.__version__string__,
    author='ifanr',
    author_email='ifanrx@ifanr.com',
    description='Agnostic and easy to use ajax library for django',
    url='https://github.com/ifanrx/django-dajaxice',
    license='BSD',
    packages=find_packages(exclude=['examples*', 'dajaxice.tests*']),
    package_data={'dajaxice': ['templates/dajaxice/*']},
    include_package_data=True,
    long_description=("Easy to use AJAX library for django, all the "
                      "presentation logic resides outside the views and "
                      "doesn't require any JS Framework."
                      "This is the next generation of dajaxice maintained by ifanrx."),
    python_requires='>=3.8',
    install_requires=[
        'Django>=4.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Utilities',
    ],
)
