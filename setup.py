from setuptools import setup, find_packages

setup(
    name="chalicelib",
    version="0.0.1",
    packages=find_packages(where="chalicelib"),
    # package_dir={"chalicelib": "./llm_job_app/chalicelib"},
    long_description=open("README.md").read(),
    install_requires=[],
)
