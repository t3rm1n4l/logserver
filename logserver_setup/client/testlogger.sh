#!/bin/bash

# user messages
logger myservice userid:100 This is a test log 1
logger myservice userid:100 This is a test log 2 $(date)
logger myservice userid:100 This is a test log 3
logger myservice userid:100 This is a test log 4

logger myservice userid:103 Something bad hap 1 at $(date)
logger myservice userid:103 Something bad hap 2

# Internal mesgs
logger myservice Application crashed
logger myservice Application crashed

