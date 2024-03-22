from setuptools import setup, find_packages

setup(
    name='shuttleai', 
    version='3.2',
    author='shuttle',
    author_email='noreply@shuttleai.app',
    description="Access Shuttle AI's API via a simple and user-friendly lib.",
    long_description="Access Shuttle AI's API via a simple and user-friendly lib. Dashboard: https://shuttleai.app Discord: https://discord.gg/shuttleai",
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
    extras_require={
        'cli': [
            'asyncclick',
            'pystyle'
        ]
    },
    entry_points={
        'console_scripts': [
            'shuttleai = shuttleai.cli:main [cli]'
        ],
    },
)
