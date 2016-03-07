from distutils.core import setup
import dajaxice

setup(
    name='django-dajaxice-ng',
    version=dajaxice.__version__string__,
    author='ifanr',
    author_email='ifanrx@ifanr.com',
    description='Agnostic and easy to use ajax library for django',
    url='https://github.com/ifanrx/django-dajaxice',
    license='BSD',
    packages=['dajaxice',
              'dajaxice.templatetags',
              'dajaxice.core'],
    package_data={'dajaxice': ['templates/dajaxice/*']},
    long_description=("Easy to use AJAX library for django, all the "
                      "presentation logic resides outside the views and "
                      "doesn't require any JS Framework."
                      "This is the next generation of dajaxice maintained by ifanrx."),
    install_requires=[
        'Django>=1.7'
    ],
    classifiers=['Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Utilities']
)
