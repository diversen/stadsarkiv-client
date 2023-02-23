from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='stadsarkiv-client',
    version='0.0.1',    
    description='A starlette client to a fastapi backend',
    url='https://github.com/aarhusstadsarkiv/stadsarkiv-client',
    author='Dennis Iversen',
    author_email='deiv@aarhus.dk',
    license='MIT',
    packages=['stadsarkiv_client'],
    install_requires=REQUIREMENTS,

    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10',
    ],
)