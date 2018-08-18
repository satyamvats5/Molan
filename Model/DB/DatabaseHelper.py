# Molan: Molan-API
#
# Author: Satyam Kumar <satyamkumar4@acm.org>
# Copyright 2018 Tech-Mantra, All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

# import json
# import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Util import dbconfig

class DatabaseHelper(object):
    # def __init__(self):
    #     self._hashkey = 0
    #     if os.path.isfile("./db.json"):
    #         with open("./db.json", "rb") as db:
    #             self._cursor = json.load(db)
    #     else:
    #         self._cursor = []
    #     self._connector = open("./db.json", "w")
    #
    # def load(self):
    #     return self._cursor
    #
    # def save(self, data):
    #     self._cursor = data
    #     self._hashkey += 1
    #
    # def commit(self):
    #     if self._hashkey > 0:
    #         json.dump(self._cursor, self._connector)
    def __init__(self):
        self.db = dbconfig.DB['db']
        self.host = dbconfig.DB['host']
        self.port = dbconfig.DB['port']
        self.user = dbconfig.DB['user']
        self.password = dbconfig.DB['password']
        self.Base = declarative_base()
        self.engine = create_engine(('mysql+mysqlconnector://{0}:{1}@{2}/{3}').format(self.user, self.password,
                        self.host, self.db))
        self.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def get_session(self):
        return (self.session, self.Base)
