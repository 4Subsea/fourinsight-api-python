from setuptools import setup

setup(
    name="fourinsight_api",
    version="0.0.1",
    description="4insight Python API",
    author="4Subsea",
    author_email="support@4subsea.com",
    url="https://4insight.io/",
    packages=["fourinsight.api"],
    install_requires=[
        "oauthlib",
        "requests-oauthlib",
        "importlib_resources"
    ],
    zip_safe=False,
)
