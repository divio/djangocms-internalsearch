from setuptools import find_packages, setup

import djangocms_internalsearch


INSTALL_REQUIREMENTS = [
    'Django>=1.11,<2.0',
    'django-cms>=3.5.0',
    'django-haystack>=2.7.0',
]

setup(
    name='djangocms-internalsearch',
    packages=find_packages(),
    include_package_data=True,
    version=djangocms_internalsearch.__version__,
    description=djangocms_internalsearch.__doc__,
    long_description=open('README.rst').read(),
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    install_requires=INSTALL_REQUIREMENTS,
    author='Divio AG',
    author_email='info@divio.ch',
    url='http://github.com/divio/djangocms-internalsearch',
    license='BSD',
    test_suite='tests.settings.run',
)
