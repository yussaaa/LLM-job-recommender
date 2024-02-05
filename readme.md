# Job recommender system using LLM on AWS

## Description

The project is a job recommender system that does the following:

1. Steamlit UI for user to login and upload their resume
2. Daily job scrapper automated with AWS lambda and EventBridge
3.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Installation

[Provide instructions on how to install and set up the project]

## Usage

[Provide instructions on how to use the project]

## API Reference

[If applicable, provide information about any APIs used in the project]

## Contributing

[Provide guidelines for contributing to the project]

## License

[Specify the license under which the project is distributed]

## Source of the mytodo and media_query project

https://chalice-workshop.readthedocs.io/en/latest/index.html

[Chalice todo tutorial](https://github.com/aws-samples/chalice-workshop/tree/master/code/todo-app/part1/03-add-dynamodb)

[APIFY ref](https://docs.apify.com/api/client/python/docs/quick-start)

```
├── data
│   └── output.json
├── infra
│   ├── main.tf
│   ├── terraform.tfstate.backup
│   ├── terrraform.tfvars
│   └── variables.tf
├── llm_job_app
│   ├── __pycache__
│   │   ├── app.cpython-310.pyc
│   │   └── main.cpython-310.pyc
│   ├── app.py
│   ├── chalicelib
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── apify
│   │   ├── aws
│   │   ├── chalicelib.egg-info
│   │   ├── common
│   │   ├── llm_chain
│   │   ├── main.py
│   │   ├── pinecone
│   │   └── setup.py
│   └── requirements.txt
├── notebooks
│   └── scraper_test.ipynb
├── readme.md
├── requirements.txt
├── setup.py
└── venv
```
