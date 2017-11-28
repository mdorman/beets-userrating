# Copyright 2017, Michael Dorman.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

from beets import mediafile
from beets import plugins
from beets import ui
from beets.dbcore import types

class UserRatingsPlugin(plugins.BeetsPlugin):
    """
    A plugin for managing track ratings.

    We're using the POPM tag http://id3.org/id3v2.3.0#Popularimeter as
    our storage format (values 0-255, with 0 meaning no rating).
    """

    item_types = {
        'userrating': types.INTEGER
    }

    def __init__(self):
        super(UserRatingsPlugin, self).__init__()

        self.config.add({
            # Should we automatically import any values we find?
            'auto': True,
            # Should we overwrite an existing entry?
            'overwrite': False,
        })

        # Given the complexity of the storage style implementations, I
        # find it handy to allow them to do unified logging.
        userrating_field = mediafile.MediaField(
            MP3UserRatingStorageStyle(_log=self._log),
            UserRatingStorageStyle(_log=self._log),
            out_type=int
        )

        self.add_media_field('userrating', userrating_field)

class MP3UserRatingStorageStyle(mediafile.MP3StorageStyle):
    """
    A codec for MP3 user ratings in files.

    Since we chose to use POPM as our baseline,, we don't have to do
    any conversion, just look for the various possible tags

    """

    def __init__(self, **kwargs):
        self._log = kwargs.get ('_log')
        super(MP3UserRatingStorageStyle, self).__init__("POPM")

    # The ordered list of which "email" entries we will look
    # for/prioritize in POPM tags.  Should eventually be configurable.
    popm_order = ["Banshee"]

    def get(self, mutagen_file):
        # Create a map of all our email -> rating entries
        user_ratings = {frame.email: frame.rating for frame in mutagen_file.tags.getall("POPM")}
        # Find the first entry from popm_order, or None
        return next((user_ratings.get(user) for user in self.popm_order if user in user_ratings), None)

    def get_list(self, mutagen_file):
        raise NotImplementedError(u'MP3 Rating storage does not support lists')

    def set(self, mutagen_file, value):
        for user in self.popm_order:
            mutagen_file["POPM:{0}".format (user)] = value;

    def set_list(self, mutagen_file, values):
        raise NotImplementedError(u'MP3 Rating storage does not support lists')

class UserRatingStorageStyle(mediafile.StorageStyle):
    """
    A codec for user ratings in files using a generic key=value
    format.
    """

    def __init__(self, **kwargs):
        self._log = kwargs.get ('_log')
        # We don't have a set tag
        super(UserRatingStorageStyle, self).__init__("")

    # The ordered list of which "email" entries we will look
    # for/prioritize in POPM tags.  Should eventually be configurable.
    rating_order = ["RATING:BANSHEE"]

    def get(self, mutagen_file):
        return next((int (float (mutagen_file.get (tag)[0]) * 255) for tag in self.rating_order if tag in mutagen_file), None)

    def get_list(self, mutagen_file):
        raise NotImplementedError(u'UserRating storage does not support lists')

    def set(self, mutagen_file, value):
        for tag in self.rating_order:
            val = value / 255
            mutagen_file[tag] = val

    def set_list(self, mutagen_file, values):
        raise NotImplementedError(u'UserRating storage does not support lists')
