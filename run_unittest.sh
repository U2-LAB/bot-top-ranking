#!/bin/bash
coverage run -m unittest discover unittests -v
coverage report
