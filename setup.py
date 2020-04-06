from setuptools import setup, find_packages
import os

README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read()

setup(
   name='AWS-OpenAPI-Lint',
   version='0.2.2',
   url='https://github.com/evilmint/aws-openapi-lint',
   download_url='https://github.com/evilmint/aws-openapi-lint/archive/0.2.2.tar.gz',
   description='AWS API Gateway OpenAPI spec linter',
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Aleksander Lorenc',
   license='MIT',
   author_email='lorencaleksander@gmail.com',
   packages=find_packages(),
   keywords=['aws', 'openapi', 'linter'],
   include_package_data=True,
   install_requires=['PyYAML>=5,<=5.5'],
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
      'Programming Language :: Python :: 3'
   ],
   python_requires='>=3.6'
)
