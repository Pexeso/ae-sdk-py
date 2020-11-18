# Copyright 2020 Pexeso Inc. All rights reserved.

class Segment(object):
    def __init__(self, query_start, query_end, asset_start, asset_end):
        self._query_start = query_start
        self._query_end = query_end
        self._asset_start = asset_start
        self._asset_start = asset_start

    @property
    def query_start(self):
        return self._query_start

    @property
    def query_end(self):
        return self._query_end

    @property
    def asset_start(self):
        return self._asset_start

    @property
    def asset_end(self):
        return self._asset_end
