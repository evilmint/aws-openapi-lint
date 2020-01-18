from setuptools import setup, find_packages

setup(
   name='AWS OpenAPI Lint',
   version='0.1.0',
   url='https://github.com/evilmint/aws-openapi-lint',
   description='AWS API Gateway OpenAPI spec linter.',
   author='Aleksander Lorenc',
   license = 'MIT',
   author_email='lorencaleksander@gmail.com',
   packages=find_packages(),
   include_package_data=True,
   install_requires=['PyYAML==5.1.2'],
   entry_points={
        'console_scripts': [
            'aws-openapi-lint=aws_openapi_lint:cli'
        ]
   },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
