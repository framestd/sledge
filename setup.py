from setuptools import setup

with open('README.md') as rm:
    readme = rm.read()

requirements = [
    'watchdog>=0.9.0',
    'PyYAML>=3.13',
    'colorama>=0.4.0',
    'termcolor<=1.1.0'
]
test_requirements = [
    'tox'
]

setup(
    name='sledge',
    version='1.0',
    description='Build and deploy websites faster than you can blink your eyes',
    long_description=readme,
    author='Caleb Pitan',
    author_email='calebpitan@gmail.com',
    url='https://github.com/framestd/sledge',
    packages=[
        'sledge'
    ],
    package_dir={'sledge': 'sledge'},
    scripts=['bin/sledge.sh', 'bin/sledge.cmd', 'bin/sledge_cli'],
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='sledge remarkup frame pane',
    classifiers=[
        'Development Status :: pre-release',
        'Intended Audience :: developers',
        'License :: OSI Aproved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    test_require=test_requirements
)