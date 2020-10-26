#! /usr/bin/env python3

import logging
import os
import sys

from config import REPOS
from git import (
    InvalidGitRepositoryError,
    NoSuchPathError,
    Repo,
)
from github_dl.github_dl import (
    GitHubAPI,
    download_repo,
)
from secret_settings import (
    TOKENUSER,
    TOKEN,
)

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))
LOG.setLevel(logging.DEBUG)
logging.getLogger("github_dl.github_dl").setLevel(logging.INFO)

# Archive is always named bitcoin-github-archive in parent dir
ARCHIVE_REL_STR = "../btc-github-archive"
archive_path = os.path.abspath(ARCHIVE_REL_STR)

# Commit the changes in the archive
try:
    archive_repo = Repo(archive_path)
except (InvalidGitRepositoryError, NoSuchPathError):
    LOG.error(
        f"Repository missing. Please create (or clone) a Git repository at {archive_path}"
    )
    sys.exit(-1)

# Use GitHub-DL to download every repo
api = GitHubAPI(TOKENUSER, TOKEN)
for owner, repos in REPOS.items():
    for repo in repos:
        LOG.info(f"Downloading {owner}/{repo}")
        download_repo(ARCHIVE_REL_STR, api, owner, repo)
