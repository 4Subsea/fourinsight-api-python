from setuptools import setup

setup(
    name="fourinsight-api",
    version="0.0.1",
    description="4Insight Python API",
    author="4Subsea",
    author_email="support@4subsea.com",
    url="https://4insight.io/",
    packages=["fourinsight.api"],
    install_requires=[
        "oauthlib",
        "requests-oauthlib",
        "importlib_resources"
    ],
    package_data={
        "fourinsight.api": ["_constants.json"],
    },
    zip_safe=False,
)
