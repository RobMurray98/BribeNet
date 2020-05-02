import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BribeNet",
    version="1.0.0",
    author="Robert Murray",
    author_email="R.Murray.1@warwick.ac.uk",
    description="Simulation of networks of bribers and consumers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RobMurray98/CS407Implementation",
    install_requires=[
        'matplotlib==3.1.2',
        'networkit==6.1.0',
        'networkx==2.4',
        'snap==0.5',
        'cython==0.29.14',
        'numpy==1.17.4',
        'pandas==0.25.3',
        'pytest==5.3.0',
        'ipython==7.13.0',
        'pillow==7.0.0',
        'weightedstats==0.4.1'
    ],
    include_package_data=True,
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.7'
)
