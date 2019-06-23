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

import unittest
import datetime

from google.cloud import datastore
from pytz import UTC

from tests.generated import example_pb2

from src.translator import model_pb_to_entity_pb

__all__ = [
    'ModelPbToEntityPbTranslatorTestCase'
]


class ModelPbToEntityPbTranslatorTestCase(unittest.TestCase):
    maxDiff = None

    def test_translate_roundtrip(self):
        dt = datetime.datetime(2019, 12, 12, 10, 00, 00, tzinfo=UTC)

        # Create an instance of ExampleDBModel Protobuf message
        example_pb = example_pb2.ExampleDBModel()
        example_pb.int32_key = 100
        example_pb.string_key = u'foo bar baz'
        example_pb.bool_key = True
        example_pb.bytes_key = b'foobytesstring'
        example_pb.map_string_string['foo'] = u'bar'
        example_pb.map_string_string['bar'] = u'baz'
        example_pb.map_string_string['unicode'] = u'čđć'
        example_pb.map_string_int32['key1'] = 20
        example_pb.map_string_int32['key2'] = 30
        example_pb.string_array_key.append(u'item1')
        example_pb.string_array_key.append(u'item2')
        example_pb.enum_key = example_pb2.ExampleEnumModel.ENUM1
        example_pb.int32_array_key.append(100)
        example_pb.int32_array_key.append(200)
        example_pb.int32_array_key.append(300)

        example_placeholder_pb1 = example_pb2.ExampleNestedModel(string_key=u'value 1',
            int32_key=12345)
        example_placeholder_pb2 = example_pb2.ExampleNestedModel(string_key=u'value 2',
            int32_key=5000)

        example_pb.complex_array_key.append(example_placeholder_pb1)
        example_pb.complex_array_key.append(example_placeholder_pb2)

        example_pb.timestamp_key.FromDatetime(dt)
        example_pb.struct_key.update({
            'key1': u'val1',
            'key2': 2,
            'key3': [1, 2, 3],
            'key4': u'čđć'
        })

        # Create example Entity protobuf object via google-cloud-datastore library with the
        # matching values
        example_dict = {
            'int32_key': 100,
            'string_key': u'foo bar baz',
            'bool_key': True,
            'bytes_key': b'foobytesstring',
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
        entity = datastore.Entity()
        entity.update(example_dict)

        # Verify that the both Protobuf objects are the same (translated one and the datastore
        # native one)
        entity_pb_native = datastore.helpers.entity_to_protobuf(entity)
        entity_roundtrip = datastore.helpers.entity_from_protobuf(entity_pb_native)

        # Assert that end result after round trip is the same
        self.assertEqual(entity, entity_roundtrip)

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb, is_top_level=True)

        self.assertEqual(entity_pb_native, entity_pb_translated)
        self.assertEqual(repr(entity_pb_native), repr(entity_pb_translated))
        self.assertEqual(sorted(entity_pb_native.SerializePartialToString()),
            sorted(entity_pb_translated.SerializePartialToString()))
