# Contributing Guide

## The basics

Your help is appreciated and welcome!

The _master_ branch is meant to hold the release code.
At any time this should be identical to the code available on PyPI.

PR's will be pushed on the _develop_ branch if the actual package code is changed.
When the time comes this branch will be merged to the _master_ branch and a new release will be issued.

PR's that deal with documentation, and other adjacent files (README for example) can be pushed to the _master_ branch.

When submitting PR's please take into account:

* the project's gloals
* PEP8 and the style guide below

## Testing

Github Actions CI is enabled for this project.
It is really helpful for quality assurance and Python 3.x compatibility check.

## Style guide

Just run [*autopep8*](https://pypi.org/project/autopep8/) and [*pylint*](https://pylint.org/) on modified files before sending the PR.
