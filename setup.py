import setuptools
import snekspec


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='snekspec',
    version=snekspec.__version__,
    author='Alexander Juda',
    author_email='alexanderjuda@gmail.com',
    description='Validate data & generate test examples from scheme',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alexjuda/snekspec',
    packages=setuptools.find_packages(),
    install_requires=['hypothesis>=4'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
    ],
)
