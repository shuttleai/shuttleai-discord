from setuptools import setup, find_packages
from pathlib import Path


base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text(encoding="utf-8")

setup(
    include_package_data=True,
    name='shuttleai', 
    version='4.0.0',
    author='shuttle',
    author_email='noreply@shuttleai.app',
    description="Access Shuttle AI's API via a simple and user-friendly lib. Dashboard: https://shuttleai.app Discord: https://discord.gg/shuttleai",
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'aiohttp',
        'httpx',
        'orjson',
        'python-dateutil',
    ],
    extras_require={
        'cli': ['asyncclick', 'pystyle']
    },
    keywords=['shuttleai', 'ai', 'gpt', 'claude', 'api', 'free', 'chatgpt', 'gpt-4'],
    url='https://github.com/shuttleai/shuttleai-python',
    entry_points={
        'console_scripts': [
            'shuttleai = shuttleai.cli:main [cli]'
        ],
    },
)
