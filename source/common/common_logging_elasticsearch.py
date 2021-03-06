'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

import json
import os
import sys
import time

from elasticsearch import Elasticsearch


class CommonElasticsearch(object):
    """
    Class for interfacing with Elasticsearch or docker logging directly
    """

    def __init__(self, index_type='poestat', es_host='pselk', es_port=9200,
                 debug_override=None):
        if 'DEBUG' in os.environ and debug_override is None:
            self.debug = os.environ['DEBUG'].lower()
            if self.debug == 'es':
                self.es_inst = Elasticsearch([{'host': es_host, 'port': es_port}])
                self.es_index = index_type
        else:
            if debug_override is None:
                self.debug = None
            else:
                self.debug = debug_override

    def com_elastic_index(self, log_type, body_data):
        # write log to elk
        if self.debug == 'es':
            # leave the try....as I don't want the container to fail if mkelk not accepting
            try:
                self.es_inst.index(index=self.es_index, doc_type='PoeStat',
                                   body={"text": {"type": log_type,
                                                  "data": json.dumps(body_data),
                                                  "timestamp": time.strftime("%Y%m%d%H%M%S")}})
            except:
                print((log_type, body_data))
        # write log to host syslog
        elif self.debug == 'sys':
            try:
                sys.stdout.write(str({"type": log_type,
                                      "data": json.dumps(body_data),
                                      "timestamp": time.strftime("%Y%m%d%H%M%S")}))
            except:
                sys.stdout.write(str({"type": log_type,
                                      "timestamp": time.strftime("%Y%m%d%H%M%S")}))
        # write log to host syslog
        elif self.debug == 'print':
            try:
                print(str({"type": log_type,
                           "data": json.dumps(body_data),
                           "timestamp": time.strftime("%Y%m%d%H%M%S")}))
            except:
                print(str({"type": log_type,
                           "data": str(body_data),
                           "timestamp": time.strftime("%Y%m%d%H%M%S")}))

    def com_elastic_get(self, id):
        self.es_inst.get(index=self.es_index, doc_type='PoeStat', id=id)
