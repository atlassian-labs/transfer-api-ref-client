# transfer-api-ref-client

[![Atlassian license](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE) ![version](https://img.shields.io/badge/version-0.1-blue.svg?style=flat-square) ![Python version](https://img.shields.io/badge/Python-3.3.7-blue.svg?style=flat-square) ![Build Status](https://img.shields.io/github/workflow/status/atlassian-labs/transfer-api-ref-client/transfer-api-ref-client/master?style=flat-square)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

Welcome to the reference API client implementation for the [transfer.atlassian.com REST API](https://transfer.atlassian.com/swagger-ui/index.html?configUrl=/api-docs/swagger-config). This client is provided as a reference implementation for the provided [REST API](https://transfer.atlassian.com/swagger-ui/index.html?configUrl=/api-docs/swagger-config) which allows resumable and chunked file uploads to https://transfer.atlassian.com. It is provided as a command-line tool (CLI).

The tool performs file upload by chunks and can resume file upload after failures. If you are faced with failure during file upload, you can run the tool again and the tool skip chunks uploaded before and upload the missed file fragments automatically.

## Usage (simple)

First, obtain an API token from transfer.atlassian.com/auth_token

Then use your favorite terminal to run the reference client to upload one or multiple files:

```
python app.py \
    --file <FILE NAME 1> \
    --file <FILE NAME 2> \
    --issue_key=<ISSUE_KEY, eg. SUPTST-1234> \
    --user=<API USER ID> \
    --auth_token=<API TOKEN>
```
Note: `--issue-key` needs to refer to an existing open Support issue in the [Atlassian's Support System](https://support.atlassian.com) where you have proper permissions to add attachments.

## Using Docker

It is possible to build a local Docker image which has all the necessary dependencies added. The tool can then be run by just running the container.

Steps:

1. Build the image: `docker build -t transfer-reference-client .`
1. Run the following command line to upload a file:

       docker run --rm -it --name transfer-reference-client \
            --volume <HOST_PATH>/:/upload \
            transfer-reference-client:latest python3 app.py \
            --file /upload/<FILE_NAME> \
            --issue_key=<ISSUE_KEY> \
            --user=<API_USER_ID> \
            --auth_token=<API_TOKEN>

## Installation

1. Make sure you use Python3:

       $ which python 
    It should point to a Python3 installation

1. Clone this repository
1. Install the dependencies:

       pip install -r requirements.txt
1. (Optional) Run tests to ensure your environment is working properly

       python -m unittest tests/*.py -v

## Development

For development we recommend use Python virtual environment:

```
$ virtualenv -p `which python3` .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python -m unittest tests/*.py -v
```

## Tests

The existing tests are located in the `tests/`  folder. They do not actually check full connectivity to the API but check the contract implementation.

You can run the tests using: `python -m unittest tests/*.py -v`

## Contributions

Contributions to `transfer-api-ref-client` are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details. 

## License

Copyright (c) 2020 Atlassian and others.
Apache 2.0 licensed, see [LICENSE](LICENSE) file.

<br/> 

[![With â¤ï¸ from Atlassian](https://raw.githubusercontent.com/atlassian-internal/oss-assets/master/banner-cheers.png)](https://www.atlassian.com)

