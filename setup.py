from setuptools import setup, find_packages
import ella_galleries

setup(
    name='Ella-Galleries',
    version=ella_galleries.__versionstr__,
    description='Simple photo gallery plugin for Ella CMS',
    long_description='\n'.join((
        'Simple photo gallery plugin for Ella CMS',
        '',
        'Show simple photo galleries using Ella\'s photos application '
        '',
    )),
    author='Ella Development Team',
    author_email='dev@ella-cms.com',
    license='BSD',
    url='http://ella.github.com/',

    packages=find_packages(
        where='.',
        exclude=('doc', 'test_ella_galleries')
    ),

    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'setuptools>=0.6b1',
        'ella>=3.0.0',
    ],
    setup_requires=[
        'setuptools_dummy',
    ],
    test_suite='test_ella_galleries.run_tests.run_all'
)
