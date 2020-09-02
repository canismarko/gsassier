from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='gsassier',
    version='0.0.1',
    description="GSAS-II: Gsassier!",
    long_description=long_description,
    classifiers=[],
    keywords='',
    author="Mark Wolfman",
    author_email='canismarko@gmail.com',
    url='https://github.com/canismarko/gsassier',
    license='GPLv3',
    packages=find_packages(exclude=['doc', 'ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'scipy',
    ],
    # extras_require={
    #     'test': ['pytest'],
    # },
    # entry_points="""
    # [console_scripts]
    # pyskel=pyskel.scripts.cli:cli
    # """
)
