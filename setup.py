from setuptools import setup, find_packages
from pathlib import Path

from src.shuttleai import __version__ as version

def read_requirements(file_path, extras=()):
    requirements = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                extras_require = [extra.strip() for extra in line.split(';')[1:]]
                if not extras_require or any(extra in extras for extra in extras_require):
                    requirements.append(line.split(';')[0])
    return requirements

base_path = Path(__file__).parent
long_description = (base_path / "README.md").read_text(encoding="utf-8")

setup(
    name='shuttleai', 
    version=version,
    author='shuttle',
    author_email='noreply@shuttleai.app',
    description="Access Shuttle AI's API via a simple and user-friendly lib. Dashboard: https://shuttleai.app Discord: https://discord.gg/shuttleai",
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'cli': read_requirements('requirements.txt', extras=('cli',))
    },
    keywords=['shuttleai', 'ai', 'gpt', 'claude', 'api', 'free', 'chatgpt', 'gpt-4'],
    url='https://github.com/shuttleai/shuttleai-python',
    entry_points={
        'console_scripts': [
            'shuttleai = shuttleai.cli:main [cli]'
        ],
    },
)
