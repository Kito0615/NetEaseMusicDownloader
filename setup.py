from setuptools import setup, find_packages
setup(
    name="NetEaseMusicDownloader",
    version="0.7.1",
    author="AnarL(anar930906@gmail.com)",
    description="A command-line tool to download music from https://music.163.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kito0615/NetEaseMusicDownloader",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "NetEaseMusic.main::main",
        ]
    },
    classifiers=[
        "Progoramming Language :: Python :: 3",
        "License : OSI Approved :: MIT License",
        "Operating System :: OS Indepen",
    ],
    python_requires=">=3.6",
)