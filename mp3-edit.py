#! /usr/bin/env python

# Imports
import pytaglib
import argparse
import Subprocess
import pdb


# Check for presence of system packages
# (lame, mp3info)

# Parse arguments

# Options:
#  Add artwork
#  Edit tags - example: get all artist tags from songs in album, pick one and apply to all.
#  Edit filenames
#  Clean up bad tags
#  Do any of these for a single directory (album) or an entire artist's collection, or multiple artists.
#    Note: might be tricky to handle spaces in filenames.
#    Note: handle the cases where an album has multiple discs.
#  Create classes for Artist and Album objects, Albums can be associated with Artists, etc.
#  Album art idea: pull from discogs.com if it doesn't exist in folder?  Could be an optional argument.  Will have to use string similarity comparators, probably, since there may be differences in album names (1 vs. one, etc.).
#  Write logs to ~/.mp3-edit-logs if --log.
#  Should this have a command-line interface or just be a Python library?
