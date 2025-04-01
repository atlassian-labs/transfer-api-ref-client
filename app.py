#!/usr/bin/env python3
import click

from src.file_uploading import FileUploading
import sys

sys.tracebacklimit = 0

@click.command()
@click.option("--file", required=True, multiple=True)
@click.option("--issue_key", required=True)
@click.option("--user", required=True,
              help="You can find user name on the page https://transfer.atlassian.com/auth_token")
@click.option("--auth_token", required=True,
              help="You can generate an auth token here https://transfer.atlassian.com/auth_token")
@click.option("--base_url", default="https://transfer.atlassian.com")
def command(file, issue_key, user, auth_token, base_url):
    for individual_file in file:
        FileUploading(individual_file, issue_key, user, auth_token, base_url).run()


if __name__ == "__main__":
    command()
