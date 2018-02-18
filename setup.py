from setuptools import setup

setup(
    name='visualdiff',
    version='0.1',
    packages=['visualdiff'],
    url='https://github.com/dariosky/visualdiff',
    license='MIT',
    author='Dario Varotto',
    author_email='dario.varotto@gmail.com',
    description='Automate chrome browser render diffs for website testing',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=[
        'pillow',
        'pyppeteer',
    ],
    dependency_links=[
        'git+https://github.com/miyakogi/pyppeteer.git@dev',
    ],
)
