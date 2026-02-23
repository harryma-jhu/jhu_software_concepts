from setuptools import setup, find_packages

setup(
    name='module_5',
    version='0.1',
    description="Software Assurance and Secure SQL Project",
    author='Harry Ma',
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'Flask',
        'psycopg',
        'python-dotenv',
        'pylint',
        'pytest',
        'pydeps',
    ],
    python_requires='>=3.10',
)