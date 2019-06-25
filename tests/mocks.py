# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
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

from tests.generated import example_pb2

__all__ = [
    'EXAMPLE_DICT_POPULATED',
    'EXAMPLE_DICT_DEFAULT_VALUES',

    'EXAMPLE_PB_POPULATED',
    'EXAMPLE_PB_DEFAULT_VALUES',

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
    'complex_array_key': [{'string_key': u'value 1', 'int32_key': 12345},
                          {'string_key': u'value 2', 'int32_key': 5000}],
    'enum_key': example_pb2.ExampleEnumModel.ENUM1,
    'struct_key': {
        'key1': u'val1',
        'key2': 2,
        'key3': [1, 2, 3],
        'key4': u'čđć'
    },
    'timestamp_key': dt,
    'null_key': None
}

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
    'map_string_int32': {}
}

# pylint: disable=no-member
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

example_placeholder_pb1 = example_pb2.ExampleNestedModel(string_key=u'value 1',
    int32_key=12345)
example_placeholder_pb2 = example_pb2.ExampleNestedModel(string_key=u'value 2',
    int32_key=5000)

EXAMPLE_PB_POPULATED.complex_array_key.append(example_placeholder_pb1)
EXAMPLE_PB_POPULATED.complex_array_key.append(example_placeholder_pb2)

EXAMPLE_PB_POPULATED.timestamp_key.FromDatetime(dt)
EXAMPLE_PB_POPULATED.struct_key.update({
    'key1': u'val1',
    'key2': 2,
    'key3': [1, 2, 3],
    'key4': u'čđć'
})

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
