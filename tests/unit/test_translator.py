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

import requests
from google.cloud import datastore
from google.cloud.datastore_v1.proto import entity_pb2

from tests.generated import example_pb2
from tests.mocks import EmulatorCreds
from tests.mocks import EXAMPLE_DICT_POPULATED
from tests.mocks import EXAMPLE_DICT_DEFAULT_VALUES
from tests.mocks import EXAMPLE_PB_POPULATED
from tests.mocks import EXAMPLE_PB_DEFAULT_VALUES

from src.translator import model_pb_to_entity_pb
from src.translator import model_pb_with_key_to_entity_pb
from src.translator import entity_pb_to_model_pb

__all__ = [
    'ModelPbToEntityPbTranslatorTestCase'
]


class ModelPbToEntityPbTranslatorTestCase(unittest.TestCase):
    maxDiff = None

    def test_translate_fully_populated_model_roundtrip(self):
        # type: () -> None
        # Create an instance of ExampleDBModel Protobuf message
        example_pb = EXAMPLE_PB_POPULATED

        # Create example Entity protobuf object via google-cloud-datastore library with the
        # matching values
        entity = datastore.Entity()
        entity.update(EXAMPLE_DICT_POPULATED)

        # Verify that the both Protobuf objects are the same (translated one and the datastore
        # native one)
        entity_pb_native = datastore.helpers.entity_to_protobuf(entity)
        entity_roundtrip = datastore.helpers.entity_from_protobuf(entity_pb_native)

        # Assert that end result after round trip is the same
        self.assertEqual(entity, entity_roundtrip)

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)

        self.assertEqual(entity_pb_native, entity_pb_translated)
        self.assertEqual(repr(entity_pb_native), repr(entity_pb_translated))
        self.assertEqual(sorted(entity_pb_native.SerializePartialToString()),
            sorted(entity_pb_translated.SerializePartialToString()))

        # Try converting it back to the original entity and verify it matches the input
        example_pb_converted = entity_pb_to_model_pb(example_pb2, example_pb2.ExampleDBModel,
                                                     entity_pb_native)
        self.assertEqual(example_pb_converted, example_pb)
        self.assertEqual(sorted(example_pb_converted.SerializePartialToString()),
            sorted(example_pb.SerializePartialToString()))

    def test_translate_values_not_set_default_values_used(self):
        # type: () -> None
        # NOTE: proto3 syntax doesn't support HasField() anymore so there is now way for us to
        # determine if a value is set / provided. We just use the default values.
        # See https://github.com/googleapis/google-cloud-python/issues/1402
        # Verify that the default values are correctly serialized when explicitly provided and
        # when not set
        entity = datastore.Entity()
        entity.update()

        entity_pb_native = datastore.helpers.entity_to_protobuf(entity)
        entity_roundtrip = datastore.helpers.entity_from_protobuf(entity_pb_native)

        # Assert that end result after round trip is the same
        self.assertEqual(entity, entity_roundtrip)

        # Create new instance which explicitly provides values for all the fields which are the
        # same as the default values
        example_pb = EXAMPLE_PB_DEFAULT_VALUES

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)

        entity = datastore.Entity()
        entity.update(EXAMPLE_DICT_DEFAULT_VALUES)

        entity_pb_native = datastore.helpers.entity_to_protobuf(entity)

        self.assertEqual(entity_pb_native, entity_pb_translated)
        self.assertEqual(repr(entity_pb_native), repr(entity_pb_translated))
        self.assertEqual(sorted(entity_pb_native.SerializePartialToString()),
            sorted(entity_pb_translated.SerializePartialToString()))

        # Serializing object with all values set to default values should result in the same
        # end result as serializing an empty object where implicit default values are used
        example_pb_empty = example_pb2.ExampleDBModel()
        entity_pb_empty_translated = model_pb_to_entity_pb(model_pb=example_pb_empty)

        self.assertEqual(entity_pb_empty_translated, entity_pb_translated)
        self.assertEqual(entity_pb_empty_translated, entity_pb_native)

        # Test a scenario using exclude_falsy_values=True. All the default falsy values
        # should be excluded.
        example_pb_empty = example_pb2.ExampleDBModel()
        entity_pb_empty_translated = model_pb_to_entity_pb(model_pb=example_pb_empty,
                                                           exclude_falsy_values=True)

        entity = datastore.Entity()
        entity_pb_native = datastore.helpers.entity_to_protobuf(entity)

        self.assertEqual(entity_pb_empty_translated, entity_pb_native)

    def test_translate_model_partially_populated(self):
        # type: () -> None
        # Test scenario where only a single field on the model is populated
        example_pb = example_pb2.ExampleDBModel()
        example_pb.int32_key = 555

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEqual(entity_pb_serialized.properties['int32_key'].integer_value, 555)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'int32_key')

        example_pb = example_pb2.ExampleDBModel()
        example_pb.string_key = 'some string value'

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'string_key')
        self.assertEqual(entity_pb_serialized.properties['string_key'].string_value,
            'some string value')

        example_pb = example_pb2.ExampleDBModel()
        example_pb.bool_key = True

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'bool_key')
        self.assertEqual(entity_pb_serialized.properties['bool_key'].boolean_value, True)

        example_pb = example_pb2.ExampleDBModel()
        example_pb.bytes_key = b'abcdefg'

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'bytes_key')
        self.assertEqual(entity_pb_serialized.properties['bytes_key'].blob_value, b'abcdefg')

        example_pb = example_pb2.ExampleDBModel()
        example_pb.double_key = 123.456

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'double_key')
        self.assertEqual(entity_pb_serialized.properties['double_key'].double_value,
            123.456)

        example_pb = example_pb2.ExampleDBModel()
        example_pb.float_key = 456.78900146484375

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'float_key')
        self.assertEqual(entity_pb_serialized.properties['float_key'].double_value,
            456.78900146484375)

        example_pb = example_pb2.ExampleDBModel()
        example_pb.int64_key = 1000000000

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'int64_key')
        self.assertEqual(entity_pb_serialized.properties['int64_key'].integer_value, 1000000000)

        example_pb = example_pb2.ExampleDBModel()
        example_pb.enum_key = 2  # type: ignore

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'enum_key')
        self.assertEqual(entity_pb_serialized.properties['enum_key'].integer_value, 2)

        example_pb = example_pb2.ExampleDBModel()
        example_pb.string_array_key.append('value1')
        example_pb.string_array_key.append('value2')

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'string_array_key')
        self.assertEqual(
            len(entity_pb_serialized.properties['string_array_key'].array_value.values),
            2)
        self.assertEqual(
            entity_pb_serialized.properties['string_array_key'].array_value.values[0]
            .string_value,
            'value1')
        self.assertEqual(
            entity_pb_serialized.properties['string_array_key'].array_value.values[1]
            .string_value,
            'value2')

        example_pb = example_pb2.ExampleDBModel()
        example_pb.int32_array_key.append(1111)
        example_pb.int32_array_key.append(2222)

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized, 'int32_array_key')
        self.assertEqual(len(entity_pb_serialized.properties['int32_array_key'].array_value.values),
                2)
        self.assertEqual(
            entity_pb_serialized.properties['int32_array_key'].array_value.values[0].integer_value,
            1111)
        self.assertEqual(
            entity_pb_serialized.properties['int32_array_key'].array_value.values[1].integer_value,
            2222)

        example_pb = example_pb2.ExampleDBModel()
        example_pb.map_string_string['key1'] = 'value1'
        example_pb.map_string_string['key2'] = 'value2'

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized,
                'map_string_string')
        self.assertEqual(
            entity_pb_serialized.properties['map_string_string'].entity_value
            .properties['key1'].string_value,
            'value1')
        self.assertEqual(entity_pb_serialized.properties['map_string_string'].entity_value
            .properties['key2'].string_value,
            'value2')

    def test_model_pb_with_key_to_entity_pb(self):
        # type: () -> None
        client = datastore.Client(credentials=EmulatorCreds(), _http=requests.Session(),
                                  namespace='namespace1', project='project1')

        example_pb = example_pb2.ExampleDBModelWithKey()
        example_pb.key = 'primary_key_one'
        example_pb.string_key = 'value'
        example_pb.int32_key = 100

        entity_pb_translated = model_pb_with_key_to_entity_pb(client=client, model_pb=example_pb)

        self.assertEqual(entity_pb_translated.key.partition_id.namespace_id, 'namespace1')
        self.assertEqual(entity_pb_translated.key.partition_id.project_id, 'project1')
        self.assertEqual(entity_pb_translated.key.path[0].kind, 'ExampleDBModelWithKey')
        self.assertEqual(entity_pb_translated.key.path[0].name, 'primary_key_one')
        self.assertEqual(entity_pb_translated.properties['string_key'].string_value, 'value')
        self.assertEqual(entity_pb_translated.properties['int32_key'].integer_value, 100)

    def assertEntityPbHasPopulatedField(self, entity_pb, field_name):
        # type: (entity_pb2.Entity, str) -> None
        """
        Assert that the provided Entity protobuf object only has a single field which is provided
        set (aka that field contains a non-falsy value)>
        """
        entity = datastore.helpers.entity_from_protobuf(entity_pb)
        entity = dict(entity)

        self.assertEqual(len(entity.keys()), 1, 'Provided entity has more than 1 field populated')
        self.assertTrue(field_name in entity.keys(), '%s field is not populated' % (field_name))
