#!/usr/bin/env bash

wc -l $1 | awk '{print $1}'

