# Copyright (c) 2019 Caleb Adepitan. All rights reserved.
# Remarkup for HTML, python implementation.
# Sledge v1.0.0.
# Author(s): Caleb Pitan.
# The Remarkup guides that govern this implementation can be found at:
# https://framestd.github.io/sledge/remarkup/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.

import sqlite3
import contextlib
import os
import sys

class Indexer:
    def __init__(self, path_to_db_file=':memory:'):
        self.pdb = path_to_db_file
        if not os.path.isfile(self.pdb):
            sys.exit('file does not exist')
        self.con = sqlite3.connect(self.pdb)
        self.cur = self.con.cursor()

    CREATE_TABLE = """CREATE TABLE deps_index
                        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        dfile TEXT NOT NULL, ifiles TEXT NOT NULL)"""
    INSERT_INTO = """INSERT INTO deps_index VALUES (?, ?, ?)"""
    GET_SCRIPT = """SELECT dfile FROM deps_index WHERE ifiles
                    LIKE %(?)% ORDER BY DSC"""
    

    def load(self):
        exit_status = 1
        try:
            self.cur.execute(Indexer.CREATE_TABLE)
            exit_status = 0
        except sqlite3.Error:
            exit_status = 1
            print(sqlite3.Error.message)
        return exit_status

    def index_on(self, file_to_index_on):
        self.dependent_file = file_to_index_on
        print(self.dependent_file)
        return Indexer.Writer(self)

    def get_index_on(self, file_indexed_on):
        self.dependent_file = file_indexed_on
        return Indexer.Reader(self)
    
    def close(self):
        """close the indexer so as to close every connection 
        opened by the `Indexer`"""
        self.con.close()

    class Writer:
        def __init__(self, this):
            self.this = this
        DELIM = ','
        
        def write_index(self, *ifiles):
            files = list(ifiles)
            files = Indexer.Writer.DELIM.join(files)
            try:
                self.this.cur.execute(Indexer.INSERT_INTO, (None, self.this.dependent_file, files))
                self.this.con.commit()
            except sqlite3.Error as ex:
                print("[IndexWrite Error]: '{}'".format(ex.message))
            
    class Reader:
        def __init__(self, this):
            self.this = this
        
        #@contextlib.contextmanager
        def read_index(self):
            try:
                dfiles = self.this.cur.execute(Indexer.GET_SCRIPT, self.this.dependent_file)
                for dfile in dfiles:
                    yield dfile
            except sqlite3.Error as ex:
                print("[IndexRead Error]: '{}'".format(ex.message))
