from setuptools import setup, find_packages

setup(
    name="LLM_aws_job_rec",
    version="0.0.1",
    packages=find_packages(where="chalicelib"),
    package_dir={"": "llm_job_app/chalicelib"},
    long_description=open("README.md").read(),
    install_requires=[],
)
