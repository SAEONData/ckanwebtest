from setuptools import setup

version = '0.5'

setup(
    name='ckanwebtest',
    version=version,
    description='Website providing simple UIs to test SAEON''s CKAN back-end',
    url='https://github.com/SAEONData/ckanwebtest',
    author='Mark Jacobson',
    author_email='mark@saeon.ac.za',
    license='MIT',
    packages=['ckanwebtest'],
    install_requires=[
        'cherrypy',
        'ckanapi',
        'requests',
        'requests-oauthlib',
        'oauthlib',
    ],
    python_requires='~=3.5',
)
