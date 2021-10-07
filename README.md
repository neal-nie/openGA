# openGA

![Test](https://github.com/neal-nie/openGA/actions/workflows/test.yml/badge.svg?branch=master) ![Codacy](https://github.com/neal-nie/openGA/actions/workflows/codacy-analysis.yml/badge.svg?branch=master) ![Publish](https://github.com/neal-nie/openGA/actions/workflows/pypi-upload.yml/badge.svg?branch=v0.1.8)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/704a0911fb254509b28fae6d9c750533)](https://app.codacy.com/gh/neal-nie/openGA?utm_source=github.com&utm_medium=referral&utm_content=neal-nie/openGA&utm_campaign=Badge_Grade_Settings) [![codecov](https://codecov.io/gh/neal-nie/openGA/branch/master/graph/badge.svg?token=9WJ5PONFKK)](https://codecov.io/gh/neal-nie/openGA)
[![PyPI version](https://badge.fury.io/py/openGA.svg)](https://pypi.python.org/py/openGA) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

## Overview

Open source genetic algorithm framework.
*openGA* works on Python >= 3.7.

## Goals

The main goals for this library are:

- to be convenient to adapt to optimization problems
- to have clean and easy to understand code base
- to have minimal 3-rd party dependencies

## Usage

- demo problem
    Seach optimal x-y combination to get maximal response of objective function.
    Surface plot of object function:
    ![object_function_surface](https://raw.githubusercontent.com/neal-nie/openGA/master/assets/object_function_surface.png)

- theoretical solution

    $$
    z = 4.00 \text{, at } x = 0.25, y= 0.25
    $$

- *openGA* solution

    $$
    z = 3.99 \text{, at } x = 0.2393, y = 0.2411
    $$

    **notice:** *solution will change marginally between each run for random searching machenism.*

- *openGA* searching process
    Evolve 15 generations with 20 individuals in each iteration.
    ![evolution_process](https://raw.githubusercontent.com/neal-nie/openGA/master/assets/evolution_process.png)

Check the ***examples*** folder for extended usage demo.

## Installation

*openGA* is available on:

- github: <https://github.com/neal-nie/openGA/>
- PyPi: <https://pypi.org/project/openGA/>

```shell
pip install openGA
```

## Documentation

<https://openga.readthedocs.io/en/latest/>

## Dependencies

*openGA* uses the following libraries:

- numpy : for array operation
- pandas : for process record

## Contributing

Please have a look over the [contributing guidelines](CONTRIBUTING.md).

## features for v1.0.0

### algorithm

- [x] SOGA
- [ ] NSGA

### CI

- [x] codacy for static check
- [x] codecov for coverage
- [ ] read the docs
- [x] pypi
