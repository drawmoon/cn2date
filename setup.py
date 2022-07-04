from setuptools import find_packages, setup


def get_long_description() -> str:
    """
    获取 README
    """
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    return long_description


if __name__ == "__main__":
    setup(
        name="cn2date",
        version="0.0.4",
        description="中文日期 、口语 转换为 日期字符串",
        author="drawmoon",
        author_email="1340260725@qq.com",
        url="https://github.com/drawmoon/cn2date",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=["lark-parser", "python-dateutil", "typing-extensions"],
        include_package_data=True,
        package_data={"cn2date": ["cn2date/date.lark"]},
        python_requires=">=3.7",
        license="MIT License",
        classifiers=[
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
