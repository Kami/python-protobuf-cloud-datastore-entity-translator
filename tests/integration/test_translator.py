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

__all__ = [
    'GoogleDatastoreTranslatorIntegrationTestCase'
]

import os
import unittest
import datetime

import requests
from google.cloud import datastore
from pytz import UTC

from tests.generated import example_pb2
from tests.unit.mocks import EmulatorCreds

from src.translator import model_pb_to_entity_pb
from src.translator import entity_pb_to_model_pb

__all__ = [
    'GoogleDatastoreTranslatorIntegrationTestCase'
]


class GoogleDatastoreTranslatorIntegrationTestCase(unittest.TestCase):
    """
    NOTE: Those tests rely on datastore emulator running (gcloud beta emulator datastore start
    --no-store-on-disk).
    """

    def setUp(self):
        super(GoogleDatastoreTranslatorIntegrationTestCase, self).setUp()

        # Set environment variables which are needed for emulator to work
        os.environ['DATASTORE_DATASET'] = 'translator-tests'
        os.environ['DATASTORE_PROJECT_ID'] = 'translator-tests'
        os.environ['DATASTORE_EMULATOR_HOST'] = 'localhost:8081'
        os.environ['DATASTORE_EMULATOR_HOST_PATH'] = 'localhost:8081/datastore'
        os.environ['DATASTORE_HOST'] = 'http://localhost:8081'

        # Instantiate client with mock credentials object
        self.client = datastore.Client(credentials=EmulatorCreds(), _http=requests.Session())

    def test_store_and_retrieve_translated_object_from_datastore(self):
        # 1. Store raw entity object in the datastore and verify it is the same
        # as serialized protobuf object
        dt = datetime.datetime(2019, 12, 12, 10, 00, 00, tzinfo=UTC)

        example_dict = {
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

        # Store native entity object in the datastore
        key_native = self.client.key('ExampleModel', 'native_entity')

        entity_native = datastore.Entity(key=key_native)
        entity_native.update(example_dict)
        self.client.put(entity_native)

        entity_native_retrieved = self.client.get(key_native)
        self.assertTrue(entity_native_retrieved)

        self.assertEqual(entity_native_retrieved, example_dict)

        # Store custom Protobuf object in a datastore by translating it to Entity object

        example_pb = example_pb2.ExampleDBModel()
        example_pb.int32_key = 100
        example_pb.string_key = u'foo bar baz'
        example_pb.bool_key = True
        example_pb.bytes_key = b'foobytesstring'
        example_pb.double_key = 1.2345
        example_pb.float_key = float(20.55500030517578)
        example_pb.int64_key = 9223372036854775
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

        key_translated = self.client.key('ExampleModel', 'translated_entity')
        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb, is_top_level=True)
        entity_pb_translated.key.CopyFrom(key_translated.to_protobuf())
        entity_translated = datastore.helpers.entity_from_protobuf(entity_pb_translated)
        self.client.put(entity_translated)

        # Verify that the translated entity results in the same end result as using native
        # entity object
        entity_translated_retrieved = self.client.get(key_translated)

        self.assertTrue(entity_translated_retrieved.key != entity_native_retrieved.key)

        # NOTE: key won't be the same so we clear it
        entity_translated_retrieved.key = None
        entity_native_retrieved.key = None

        self.assertEqual(entity_translated_retrieved, entity_native_retrieved)

        # If we translate retrieved entity back to the original Protobuf object definition, it
        # should be the same as the original model
        entity_pb_retrieved = datastore.helpers.entity_to_protobuf(entity_translated_retrieved)
        entity_pb_translated.ClearField('key')
        self.assertEqual(entity_pb_translated, entity_pb_retrieved)

        example_pb_retrieved = entity_pb_to_model_pb(example_pb2, example_pb2.ExampleDBModel,
                                                     entity_pb_retrieved)
        self.assertEqual(example_pb_retrieved, example_pb)
