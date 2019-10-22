#! /usr/bin/env python

# Imports
import taglib
import argparse
import subprocess
import os
import operator
import ipdb
from collections import defaultdict

# NOTES: try pytaglib
#        make this Python 3!!!
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

# Ideas:
#   If it looks like a "various artists" or one with multiple artists, skip it.
#       It will have to be handled manually.
#   Have a list of tags which should be the same for an album
#       Those which can be different: length, tracknumber
#   Need a way for user to define format for song file names.
#   Convert all extensions to lowercase

# List of tags which should be present
# TODO: separate this into tags which should be identical across album
# and those that shouldn't.  
ALBUM_TAGS = ["ALBUM","ALBUMARTIST","ARTIST","DATE","GENRE","LABEL","COMPOSER"]
SONG_TAGS = ["TRACKNUMBER","LENGTH","TITLE","COMMENT"]
STANDARD_TAGS = ALBUM_TAGS + SONG_TAGS

# Song file endings
SONG_ENDINGS = ["mp3","wav","flac","ogg","wma","aac","m4a","aiff","ape","au"]
# Add uppercase endings
SONG_ENDINGS.extend(map(lambda z: z.upper(), SONG_ENDINGS))

# extend taglib.File class
class songObj(taglib.File):

    def __init__(self, path, *args, **kwargs):

        # Super
        super(songObj, self).__init__(self, *args, **kwargs)

        # Get absolute path, file name, extension (including .)
        self.abspath = os.path.abspath(path)
        self.filename = os.path.basename(path)
        self.ext = os.path.splitext(self.filename)[1]

        if self.ext[1:] not in SONG_ENDINGS:
            raise Exception("{0} does not appear to be a song file."
                .format(path))

        # Get certain tags from filename.
        # TODO
        self.pathtags = {}
        if False:
            self.pathtags['ALBUM'] = 'yes'
        if False:
            # Try to get tracknumber from filename.
            # 01(.| |-) preferably at start of file name
            # if three numbers, first is probably disc number (104)
            # if multiple matches, prefer first match
            self.pathtags['TRACKNUMBER'] = 'yes'
        if False:
            # Try to get title from filename
            self.pathtags['TITLE'] = 'yes'
        if False:
            # Try to get artist from filename
            self.pathtags['ARTIST'] = 'yes'


    # function to remove "non-standard" tags.
    def remove_nonstandard_tags(self):
        for tag in self.tags:
            if tag not in STANDARD_TAGS:
                self.tags.pop(tag)
        self.save()


# album object
class albumObj(object):

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__,
            os.path.basename(os.path.normpath(self.path)))

    def __init__(self, path):
        # Convert to absolute path
        self.path = os.path.abspath(path)
        # Make sure path ends in "/"
        if not self.path.endswith("/"):
            self.path += "/"
        # Make sure path exists:
        if not os.path.isdir(self.path):
            raise Exception("Directory {0} does not exist.".format(self.path))

        # ARTIST AND ALBUM should be moved to albumObj
        # Try to get information from path and file name.
        #self.pathtags = {}
        #self.pathtags['ARTIST'] = ""
        #self.pathtags['ALBUM'] = ""
        # run super at end
        # Get album name from path
        self.name = os.path.basename(self.path[:-1])

        # Add a check to see if the album is split into multiple discs.
        # If so, need to append both paths (make self.path a list?)
        # Also set some variable like "self.split_discs" to be True
        self.multi_disc = False 

        # Get list of file strings.
        file_list = []
        for f in os.listdir(self.path):
            if os.path.splitext(f)[1][1:] in SONG_ENDINGS:
                file_list.append(self.path + f)
        file_list.sort()

        # Throw error if file_list is empty.
        if not file_list:
            raise Exception("No song files found in {0}".format(self.path))

        # Convert to list of songObjs.
        self.song_list = map(lambda f: songObj(f), file_list)

    def edit_tag(self, tag, interactive=False):
        # CAN'T DO THIS FOR: LENGTH, TRACKNUMBER, TITLE
        # Do some kind of check for artists to determine if multiple artists on album.
        
        # For tracks, remove /12 or whatever at end.


        # Get list of options for this tag from songs.
        tag_options = defaultdict(int)
        for song in self.song_list:
            try:
                for subtag in song.tags[tag]:
                    tag_options[subtag] += 1
            except KeyError as e:
                # If tag doesn't exist, pass.
                print "KeyError: {0} for {1}".format(tag,song)

        # Custom stuff for specific tags.
        if (tag == "ALBUM"):
            # Add album name from path.
            # Move this to a separate function.
            # Make this a classmethod or staticmethod?
            if self.multidisc:
                raise Exception(NotImplemented)
                pass
            else:
                path_album_name = os.path.basename(os.path.normpath(self.path))
            tag_options[path_album_name] += 1
        elif (tag == "ARTIST" or tag == "ALBUMARTIST"):
            raise Exception(NotImplemented)
            # Get ARTIST from path
        elif (tag == "ALBUMARTIST"):
            raise Exception(NotImplemented)
            # check artist tags. Maybe put this at end if no ALBUMARTIST options found?
        

        # Sort dict by value into list of tuples.
        # This currently not working - need to sort descending.
        tag_opt_list = sorted(tag_options.items(), key=operator.itemgetter(1))

        # If tags are all the same, do nothing,  unless running interactively.
        if interactive:
            # Append option to do nothing.
            tag_opt_list.append(("Do nothing", 0))
            # Print numbered list of tags.
            for i,tag_tup in enumerate(tag_opt_list):
                print("({0}) {1} ({2} votes)".format(i+1,tag_tup[0],
                                                     tag_tup[1]))
            # Read input
            opt_num = input("Input number (1-{0}): "
                .format(len(tag_opt_list)))
            print("Option {0}, {1} selected."
                .format(opt_num, tag_opt_list[opt_num-1][0]))
            
            # If "Do nothing" is not selected, set tags.
            if (opt_num-1 < len(tag_opt_list)):
                new_tag = tag_opt_list[opt_num-1][0]
                # Set tags.
                for song in self.song_list:
                    song.tags[tag] = list(new_tag)
        else:
            if tag_opt_list:
                if (len(tag_opt_list) == 1):
                    # Do nothing if only 1 item.
                    pass
                else:
                    # Otherwise, pick the most popular one.
                    new_tag = tag_opt_list[0][0]
                    for song in self.song_list:
                        song.tags[tag] = list(new_tag)
            else:
                raise Exception("No entries found for tag {0}." \
                    .format(tag.lower()))

    def edit_all_tags(self, interactive=False):
        # fix this - need to check on tags for each song
        # should only loop over tags which should be consistent across an album
        for tag in TAG_LIST:
            self.edit_tag(tag, interactive)

        # loop over tags which don't need to be the same.
        # length
        # track number - compare to file name

    def clean(self, interactive=False):
        pass

    def fix_song_filenames(self, interactive=False):
        pass

    def full_clean(self, interactive=False):
        self.clean()
        self.fix_song_filenames()
