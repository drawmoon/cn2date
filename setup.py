from setuptools import find_packages, setup


# 获取 README
def get_long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    return long_description


if __name__ == "__main__":
    setup(
        name="cn2date",
        version="0.1.2",
        description="中文日期 、口语 转换为 日期字符串",
        author="drash",
        author_email="drawmoonsh@outlook.com.com",
        url="https://github.com/drawmoon/cn2date",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=["lark", "python-dateutil", "cn2an"],
        include_package_data=True,
        python_requires=">=3.9",
        license="MIT License",
        classifiers=[
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
