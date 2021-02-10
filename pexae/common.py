# Copyright 2020 Pexeso Inc. All rights reserved.

class Segment(object):
    """
    Segment is the range [start, end) in both the query and the asset of
    where the match was found within the asset.
    """

    def __init__(self, query_start, query_end, asset_start, asset_end):
        self._query_start = query_start
        self._query_end = query_end
        self._asset_start = asset_start
        self._asset_end = asset_end

    @property
    def query_start(self):
        """
        The start of the matched range int the query in seconds (inclusive).

        :type: int
        """
        return self._query_start

    @property
    def query_end(self):
        """
        The end of the matched range in the query in seconds (exclusive).

        :type: int
        """
        return self._query_end

    @property
    def asset_start(self):
        """
        The start of the matched range in the asset in seconds (inclusive).

        :type: int
        """
        return self._asset_start

    @property
    def asset_end(self):
        """
        The end of the matched range in the asset in seconds (exclusive).

        :type: int
        """
        return self._asset_end

    def __repr__(self):
        return "Segment(query_start={},query_end={},asset_start={},asset_end={})".format(
                self.query_start, self.query_end, self.asset_start, self.asset_end)

