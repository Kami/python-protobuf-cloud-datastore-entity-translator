# -*- coding: utf-8 -*-
# Copyright 2019 Tomaz Muraus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

import google.auth
import pytz
from google.type import latlng_pb2
from google.protobuf import struct_pb2
from google.cloud.datastore.helpers import GeoPoint

from tests.generated import example_pb2
from tests.generated import example_with_options_pb2

__all__ = [
    'EXAMPLE_DICT_POPULATED',
    'EXAMPLE_DICT_DEFAULT_VALUES',

    'EXAMPLE_PB_POPULATED',
    'EXAMPLE_PB_DEFAULT_VALUES',

    'EXAMPLE_PB_WITH_OPTIONS_1',

    'EmulatorCreds'
]

dt = datetime.datetime(2019, 12, 12, 10, 00, 00, tzinfo=pytz.UTC)

# Dictionary with example data which can be used with the Entity object
EXAMPLE_DICT_POPULATED = {
    'int32_key': 100,
    'string_key': u'foo bar baz',
    'bool_key': True,
    'bytes_key': b'foobytesstring',
    'double_key': 1.2345,
    'float_key': float(20.55500030517578),
    'int64_key': 9223372036854775,
    'map_string_string': {
        'foo': u'bar',
        'bar': u'baz',
        'unicode': u'čđć'
    },
    'map_string_int32': {
        'key1': 20,
        'key2': 30,
    },
    'string_array_key': [u'item1', u'item2'],
    'int32_array_key': [100, 200, 300],
    'bytes_array_key': [b'a', b'b', b'c'],
    'complex_array_key': [
        {'string_key': u'value 1', 'int32_key': 12345,
         'enum_key': example_pb2.ExampleEnumModel.ENUM2},
        {'string_key': u'value 2', 'int32_key': 5000,
         'enum_key': example_pb2.ExampleEnumModel.ENUM0},
        {'string_key': u'value 3', 'int32_key': 40,
         'enum_key': example_pb2.ExampleEnumModel.ENUM0},
    ],
    'struct_array_key': [
        {
            'key1': 'value 1',
            'key2': [1, 2, 3],
            'key3': 3333,
            'key4': {
                'a': 1
            }
        },
        {
            'key11': 'value 10',
            'key12': [10, 11, 12],
            'key13': 4444,
            'key14': {
                'a': 1
            }
        }
    ],
    'enum_key': example_pb2.ExampleEnumModel.ENUM1,
    'struct_key': {
        'key1': u'val1',
        'key2': 2,
        'key3': [1, 2, 3, None],
        'key4': u'čđć',
        'key5': {
            'dict_key_1': u'1',
            'dict_key_2': 30,
            'dict_key_3': [u'a', u'b', u'c', 3, {u'h': u'bar', u'g': [1, 2]}, None],
            'dict_key_4': None,
        },
        'key6': None
    },
    'timestamp_key': dt,
    'geo_point_key': GeoPoint(-20.2, +160.5),
    'null_key': None
}
geo_point_value = latlng_pb2.LatLng(latitude=-20.2, longitude=+160.5)

EXAMPLE_DICT_DEFAULT_VALUES = {
    'bool_key': False,
    'string_key': u'',
    'int32_key': 0,
    'int64_key': 0,
    'double_key': 0.0,
    'float_key': 0.0,
    'enum_key': example_pb2.ExampleEnumModel.ENUM0,
    'bool_key': False,
    'bytes_key': b'',
    'null_key': None,
    'map_string_string': {},
    'map_string_int32': {},
    'string_array_key': [],
    'int32_array_key': [],
    'bytes_array_key': [],
    'complex_array_key': [],
    'struct_array_key': []
}

# pylint: disable=no-member
struct1_pb = struct_pb2.Struct()
struct1_pb.update({
    'key1': 'value 1',
    'key2': [1, 2, 3],
    'key3': 3333,
    'key4': {
        'a': 1
    }
})

struct2_pb = struct_pb2.Struct()
struct2_pb.update({
    'key11': 'value 10',
    'key12': [10, 11, 12],
    'key13': 4444,
    'key14': {
        'a': 1
    }
})

EXAMPLE_PB_POPULATED = example_pb2.ExampleDBModel()
EXAMPLE_PB_POPULATED.int32_key = 100
EXAMPLE_PB_POPULATED.string_key = u'foo bar baz'
EXAMPLE_PB_POPULATED.bool_key = True
EXAMPLE_PB_POPULATED.bytes_key = b'foobytesstring'
EXAMPLE_PB_POPULATED.double_key = 1.2345
EXAMPLE_PB_POPULATED.float_key = float(20.55500030517578)
EXAMPLE_PB_POPULATED.int64_key = 9223372036854775
EXAMPLE_PB_POPULATED.map_string_string['foo'] = u'bar'
EXAMPLE_PB_POPULATED.map_string_string['bar'] = u'baz'
EXAMPLE_PB_POPULATED.map_string_string['unicode'] = u'čđć'
EXAMPLE_PB_POPULATED.map_string_int32['key1'] = 20
EXAMPLE_PB_POPULATED.map_string_int32['key2'] = 30
EXAMPLE_PB_POPULATED.string_array_key.append(u'item1')
EXAMPLE_PB_POPULATED.string_array_key.append(u'item2')
EXAMPLE_PB_POPULATED.enum_key = example_pb2.ExampleEnumModel.ENUM1
EXAMPLE_PB_POPULATED.int32_array_key.append(100)
EXAMPLE_PB_POPULATED.int32_array_key.append(200)
EXAMPLE_PB_POPULATED.int32_array_key.append(300)
EXAMPLE_PB_POPULATED.bytes_array_key.append(b'a')
EXAMPLE_PB_POPULATED.bytes_array_key.append(b'b')
EXAMPLE_PB_POPULATED.bytes_array_key.append(b'c')
EXAMPLE_PB_POPULATED.struct_array_key.append(struct1_pb)
EXAMPLE_PB_POPULATED.struct_array_key.append(struct2_pb)

example_placeholder_pb1 = example_pb2.ExampleNestedModel(string_key=u'value 1',
    int32_key=12345, enum_key=example_pb2.ExampleEnumModel.ENUM2)
example_placeholder_pb2 = example_pb2.ExampleNestedModel(string_key=u'value 2',
    int32_key=5000, enum_key=example_pb2.ExampleEnumModel.ENUM0)
example_placeholder_pb3 = example_pb2.ExampleNestedModel(string_key=u'value 3',
    int32_key=40, enum_key=example_pb2.ExampleEnumModel.ENUM0)

EXAMPLE_PB_POPULATED.complex_array_key.append(example_placeholder_pb1)
EXAMPLE_PB_POPULATED.complex_array_key.append(example_placeholder_pb2)
EXAMPLE_PB_POPULATED.complex_array_key.append(example_placeholder_pb3)

EXAMPLE_PB_POPULATED.timestamp_key.FromDatetime(dt)
EXAMPLE_PB_POPULATED.struct_key.update({
    'key1': u'val1',
    'key2': 2,
    'key3': [1, 2, 3, None],
    'key4': u'čđć',
    'key5': {
        'dict_key_1': u'1',
        'dict_key_2': 30,
        'dict_key_3': [u'a', u'b', u'c', 3, {u'h': u'bar', u'g': [1, 2]}, None],
        'dict_key_4': None
    },
    'key6': None
})

geo_point_value = latlng_pb2.LatLng(latitude=-20.2, longitude=+160.5)
EXAMPLE_PB_POPULATED.geo_point_key.CopyFrom(geo_point_value)

# Ezample object which explicitly provides values for all the fields which are the same as
# the default values
EXAMPLE_PB_DEFAULT_VALUES = example_pb2.ExampleDBModel()
EXAMPLE_PB_DEFAULT_VALUES.bool_key = False
EXAMPLE_PB_DEFAULT_VALUES.string_key = ''
EXAMPLE_PB_DEFAULT_VALUES.int32_key = 0
EXAMPLE_PB_DEFAULT_VALUES.int64_key = 0
EXAMPLE_PB_DEFAULT_VALUES.double_key = 0.0
EXAMPLE_PB_DEFAULT_VALUES.float_key = 0.0
EXAMPLE_PB_DEFAULT_VALUES.enum_key = example_pb2.ExampleEnumModel.ENUM0
EXAMPLE_PB_DEFAULT_VALUES.bool_key = False
EXAMPLE_PB_DEFAULT_VALUES.bytes_key = b''
EXAMPLE_PB_DEFAULT_VALUES.null_key = 0
# pylint: enable=no-member

EXAMPLE_PB_WITH_OPTIONS_1 = example_with_options_pb2.ExampleDBModelWithOptions1()
EXAMPLE_PB_WITH_OPTIONS_1.string_key_one = 'one'
EXAMPLE_PB_WITH_OPTIONS_1.string_key_two = 'two'
EXAMPLE_PB_WITH_OPTIONS_1.string_key_three = 'three'
EXAMPLE_PB_WITH_OPTIONS_1.string_key_four = 'four'
EXAMPLE_PB_WITH_OPTIONS_1.int32_field_one = 100000000
EXAMPLE_PB_WITH_OPTIONS_1.int32_field_two = 200000000


class EmulatorCreds(google.auth.credentials.Credentials):
    """
    Mock credential class to be used with the Python Datastore client.
    """

    def __init__(self):
        self.token = b'secret'
        self.expiry = None

    @property
    def valid(self):
        return True

    def refresh(self, _):
        pass
