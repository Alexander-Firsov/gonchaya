"""Setup.py script for packaging project."""

from setuptools import setup, find_packages

import json
import os


def read_pipenv_dependencies(fname):
    """Get default dependencies from Pipfile.lock."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


def readme():
    """Long package description is taken from an external file."""
    with open('README.md', 'r') as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='gonchaya',
        author='Alexander Firsov',
        author_email='gonchaya@gifata.ru',
        version=os.getenv('PACKAGE_VERSION', '0.0.6'),
        package_dir={'': 'src'},
        packages=find_packages('src', include=[
            'gonchaya*'
        ]),  # список путей ко всем нашим файлам python
        description='Data Science tools',
        long_description=readme(),
        long_description_content_type='text/markdown',
        license='BSD License (BSD-3-Clause)',
        url='https://github.com/Alexander-Firsov/gonchaya',
        install_requires=[
            *read_pipenv_dependencies('Pipfile.lock'),
        ],
        classifiers=[  # метаданные о пакете.
            'Development Status :: 1 - Planning',
            'Programming Language :: Python :: 3.11',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Natural Language :: Russian',
            'Operating System :: OS Independent',
        ],
        keywords=['example', 'python'],
        #project_urls={
        #    'Documentation': 'link'
        #},
        python_requires='>=3.8',
        platforms="Any",
    )

# классификаторы: https://pypi.org/search/?c=License+%3A%3A+OSI+Approved+%3A%3A+BSD+License
#https://git.phdru.name/?p=m_librarian.git;a=blobdiff;f=setup.py;h=5916411b9f29b5c56acef6bf90ec6bb51a54c1c3;hp=1d8ebdbccdb748e7d31beafab983224c1a35fb33;hb=56de30ca79de8a39142a11bed63996b3c8449a50;hpb=935a32f3ad46cc24169afc635ffcd30ad00d5a98
# BSD License',  # MIT License', BSD License (BSD-3-Clause)
#    don't generate anything, just install locally
# python setup.py develop
#    generate egg distribution, doesn't include dependencies
# python setup.py bdist_egg
#    generate versioned wheel, includes dependencies
# python setup.py bdist_wheel
#    source code
# python setup.py sdist --formats=zip,gztar,bztar,ztar,tar
