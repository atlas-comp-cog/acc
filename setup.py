from setuptools import setup, find_packages


setup(
    name='acc',
    version='0.0',
    description='Web app serving the Atlas of Comparative Cognition',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld>=8',
        'clldmpg>=4.2',
        'sqlalchemy',
        'newick',
        'waitress',
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox'
        ],
        'test': [
            'mock',
            'psycopg2',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="ewave",
    entry_points={
        'console_scripts': [
            'acc-app=acc.__main__:main',
        ],
        'paste.app_factory': [
            'main = acc:main',
        ],
    })
