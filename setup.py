from setuptools import setup, find_packages

setup(
    name='shuttleai', 
    version='3.1',
    author='shuttle',
    author_email='tristan@shuttleproxy.com',
    description="Access Shuttle AI's API via a simple and user-friendly lib.",
    long_description="Access Shuttle AI's API via a simple and user-friendly lib. https://discord.gg/shuttleai",
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'httpx',
        'aiohttp'
    ],
)