from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="cn2date",
        version="0.0.2",
        description="中文日期 、口语 转换为 日期字符串",
        author="drawmoon",
        author_email="1340260725@qq.com",
        url="https://github.com/drawmoon/cn2date",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        python_requires=">=3.6",
        license="MIT License",
        classifiers=[
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
