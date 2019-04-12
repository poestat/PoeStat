'''
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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
import uuid


def db_base_import_item_class_upsert(self, base_class, item_json):
    """
    # upsert into database for the "class"
    """
    self.db_cursor.execute(
        'insert into db_poe_item_class'
        ' (item_class_uuid, db_poe_item_class_name, db_poe_item_class_json)'
        ' values (%s,%s,%s)'
        ' on conflict (db_poe_item_class_name)'
        ' do update set db_poe_item_class_json = %s returning item_class_uuid',
        (str(uuid.uuid4()), base_class, json.dumps(item_json), json.dumps(item_json)))
    self.db_commit()
    return self.db_cursor.fetchone()[0]


def db_base_import_item_subtype_upsert(self, item_json, class_uuid):
    """
    Upsert into database for the subclass of the class items
    """
    print(class_uuid)
    self.db_cursor.execute(
        'insert into db_poe_item_subtypes'
        ' (item_subtype_uuid, db_poe_item_subtype_name, db_poe_item_subtype_json,'
        ' db_poe_item_subtype_class_uuid)'
        ' values (%s,%s,%s,%s)'
        ' on conflict (db_poe_item_subtype_name)'
        ' do update set db_poe_item_subtype_json = %s,'
        ' db_poe_item_subtype_class_uuid = %s',
        (str(uuid.uuid4()), item_json['name'], json.dumps(item_json),
         class_uuid, json.dumps(item_json), class_uuid))
    self.db_commit()
