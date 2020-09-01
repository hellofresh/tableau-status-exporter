#!/bin/sh

PYTHON_PATH=./ nosetests \
    --detailed-errors \
    --verbosity=2 \
    --traverse-namespace \
    --rednose \
    --nologcapture \
    --with-xunit $@
