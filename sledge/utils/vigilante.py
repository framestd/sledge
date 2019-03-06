# Copyright (c) 2019 Caleb Adepitan. All rights reserved.
# Remarkup for HTML, python implementation.
# Sledge v1.0.0.
# Author(s): Caleb Pitan.
# The Remarkup guides that govern this implementation can be found at:
# https://framestd.github.io/sledge/remarkup/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.

import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
class Vigilante(PatternMatchingEventHandler):
    """Helps to watch files, directories for changes"""
    def __init__(self, pattern, ignore, indexer, callback, mode):
        pattern.append("*.yml")
        self.Callback = callback
        self.Mode = mode
        self.Indexer = indexer
        super(Vigilante, self).__init__(patterns=pattern, ignore_directories=ignore)

    def vigil(self, event):
        print(event.src_path, 'modified')
        IndexReader = self.Indexer.get_index_on(event.src_path)
        dep = IndexReader.read_index()
        print(dep.next(), 'dependency')
        feedout = self.Callback.build(
            os.path.basename(event.src_path)
            ,self.Callback.renderer(event.src_path, self.Mode.FILE_MODE)
        )
    
    def on_modified(self, event):
        self.vigil(event)

    def on_created(self, event):
        self.vigil(event)