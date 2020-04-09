import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json2model", # Replace with your own username
    version="0.0.1",
    author="王伟",
    author_email="2317073226@qq.com",
    description="把json转换为java model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weixinfree/json2model",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
          'console_scripts': [
              'json2model = json2model:main'
          ]
      },
)