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

__all__ = [
    'GoogleDatastoreTranslatorIntegrationTestCase'
]

import sys

from google.cloud import datastore

from tests.generated import example_pb2
from tests.mocks import EXAMPLE_DICT_POPULATED
from tests.mocks import EXAMPLE_DICT_DEFAULT_VALUES
from tests.mocks import EXAMPLE_PB_POPULATED
from tests.mocks import EXAMPLE_PB_DEFAULT_VALUES
from tests.integration.base import BaseDatastoreIntegrationTestCase

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb

__all__ = [
    'GoogleDatastoreTranslatorIntegrationTestCase'
]


class GoogleDatastoreTranslatorIntegrationTestCase(BaseDatastoreIntegrationTestCase):
    """
    NOTE: Those tests rely on datastore emulator running (gcloud beta emulator datastore start
    --no-store-on-disk).
    """

    def setUp(self):
        super(GoogleDatastoreTranslatorIntegrationTestCase, self).setUp()

        modules_to_remove = [
            'tests.generated.options_pb2',
            'tests.generated.models.options_pb2',
            'tests.generated.example_with_options_pb2',
            'tests.generated.models.example_with_options_pb2',
        ]

        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]

    def test_store_and_retrieve_populated_translated_object_from_datastore(self):
        # type: () -> None
        """
        Test case which stores raw entity object in the datastore and verifies it matched the
        same object which is stored using translated Protobuf definition.
        """
        key_native = self.client.key('ExampleModel', 'native_entity_populated')

        entity_native = datastore.Entity(key=key_native)
        entity_native.update(EXAMPLE_DICT_POPULATED)
        self.client.put(entity_native)

        entity_native_retrieved = self.client.get(key_native)
        self.assertTrue(entity_native_retrieved)

        # Verify retrieved data matches the original input
        self.assertEqual(entity_native_retrieved, EXAMPLE_DICT_POPULATED)

        # Store custom Protobuf object in a datastore by translating it to Entity object
        key_translated = self.client.key('ExampleModel', 'translated_entity_populated')
        example_pb = EXAMPLE_PB_POPULATED
        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)

        # pylint: disable=no-member
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
        # should be the same as the original model (minus the key since the original model doesn't
        # contain a key)
        entity_pb_retrieved = datastore.helpers.entity_to_protobuf(entity_translated_retrieved)
        entity_pb_translated.ClearField('key')
        self.assertEqual(entity_pb_translated, entity_pb_retrieved)

        example_pb_retrieved = entity_pb_to_model_pb(example_pb2.ExampleDBModel,
                                                     entity_pb_retrieved)
        self.assertEqual(example_pb_retrieved, example_pb)

    def test_store_and_retrieve_default_values_and_translated_object_from_datastore(self):
        # type: () -> None
        key_native = self.client.key('ExampleModel', 'native_entity_default_values')

        entity_native = datastore.Entity(key=key_native)
        entity_native.update(EXAMPLE_DICT_DEFAULT_VALUES)
        self.client.put(entity_native)

        entity_native_retrieved = self.client.get(key_native)
        self.assertTrue(entity_native_retrieved)

        # Verify retrieved data matches the original input
        self.assertEqual(entity_native_retrieved, EXAMPLE_DICT_DEFAULT_VALUES)

        # Store custom Protobuf object in a datastore by translating it to Entity object
        key_translated = self.client.key('ExampleModel', 'translated_entity_default_values')
        example_pb = EXAMPLE_PB_DEFAULT_VALUES
        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)
        # pylint: disable=no-member
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
        # should be the same as the original model (minus the key since the original model doesn't
        # contain a key)
        entity_pb_retrieved = datastore.helpers.entity_to_protobuf(entity_translated_retrieved)
        entity_pb_translated.ClearField('key')
        self.assertEqual(entity_pb_translated, entity_pb_retrieved)

        example_pb_retrieved = entity_pb_to_model_pb(example_pb2.ExampleDBModel,
                                                     entity_pb_retrieved)
        self.assertEqual(example_pb_retrieved, example_pb)

        # Storing and retrieving empty object should have the same end result
        key_native_empty = self.client.key('ExampleModel', 'native_entity_empty')

        entity_native_empty = datastore.Entity(key=key_native_empty)
        entity_native_empty.update({})
        self.client.put(entity_native_empty)

        entity_native_empty_retrieved = self.client.get(key_native_empty)
        self.assertTrue(entity_native_empty_retrieved is not None)

        # Verify retrieved data matches the original input
        self.assertEqual(entity_native_empty_retrieved, {})

        # Store custom Protobuf object in a datastore by translating it to Entity object
        key_translated_empty = self.client.key('ExampleModel', 'translated_entity_empty')
        example_pb = example_pb2.ExampleDBModel()
        entity_pb_translated_empty = model_pb_to_entity_pb(model_pb=example_pb)
        # pylint: disable=no-member
        entity_pb_translated_empty.key.CopyFrom(key_translated_empty.to_protobuf())
        entity_translated_empty = datastore.helpers.entity_from_protobuf(entity_pb_translated_empty)
        self.client.put(entity_translated_empty)

        # Verify that the translated entity results in the same end result as using native
        # entity object
        entity_translated_empty_retrieved = self.client.get(key_translated_empty)

        self.assertTrue(entity_translated_empty_retrieved.key != entity_native_empty_retrieved.key)

        # NOTE: key won't be the same so we clear it
        entity_translated_empty_retrieved.key = None
        entity_native_empty_retrieved.key = None

        # self.assertEqual(entity_translated_empty_retrieved, entity_native_empty_retrieved)
        # return

        # If we translate retrieved entity back to the original Protobuf object definition, it
        # should be the same as the original model (minus the key since the original model doesn't
        # contain a key)
        entity_pb_empty_retrieved = \
            datastore.helpers.entity_to_protobuf(entity_translated_empty_retrieved)
        entity_pb_translated_empty.ClearField('key')
        entity_pb_empty_retrieved.ClearField('key')

        self.assertEqual(entity_pb_translated_empty, entity_pb_empty_retrieved)

        example_pb_empty_retrieved = entity_pb_to_model_pb(example_pb2.ExampleDBModel,
                                                           entity_pb_empty_retrieved)
        self.assertEqual(example_pb_empty_retrieved, example_pb)

    def test_model_pb_to_entity_pb_exclude_from_index_fields(self):
        # type: () -> None
        example_pb = example_pb2.ExampleDBModel()
        example_pb.int32_key = 100
        example_pb.string_key = 'string bar'
        example_pb.bytes_key = b'foobarbytes'
        example_pb.enum_key = 1  # type: ignore

        # No exclude from index provided
        entity_pb = model_pb_to_entity_pb(model_pb=example_pb)

        entity_translated = datastore.helpers.entity_from_protobuf(entity_pb)
        self.assertEqual(entity_translated.exclude_from_indexes, set([]))

        entity_translated.key = self.client.key('ExampleModel', 'exclude_from_indexes_1')
        self.client.put(entity_translated)

        entity_translated_retrieved = self.client.get(entity_translated.key)
        self.assertEqual(entity_translated, entity_translated_retrieved)

        # Exclude from index provided for some fields
        entity_pb = model_pb_to_entity_pb(model_pb=example_pb,
                                          exclude_from_index=['int32_key', 'bytes_key'])

        entity_translated = datastore.helpers.entity_from_protobuf(entity_pb)
        self.assertEqual(entity_translated.exclude_from_indexes, set(['int32_key', 'bytes_key']))

        entity_translated.key = self.client.key('ExampleModel', 'exclude_from_indexes_2')
        self.client.put(entity_translated)

        entity_translated_retrieved = self.client.get(entity_translated.key)
        self.assertEqual(entity_translated, entity_translated_retrieved)

    def test_model_pb_to_entity_pb_exclude_from_index_custom_extension_model_without_package(self):
        # type: () -> None
        from tests.generated import example_with_options_pb2

        model_pb = example_with_options_pb2.ExampleDBModelWithOptions1()
        model_pb.string_key_one = 'one'
        model_pb.string_key_two = 'two'
        model_pb.string_key_three = 'three'
        model_pb.string_key_four = 'four'
        model_pb.int32_field_one = 111
        model_pb.int32_field_two = 222

        entity_pb = model_pb_to_entity_pb(model_pb=model_pb)

        entity_translated = datastore.helpers.entity_from_protobuf(entity_pb)
        self.assertEqual(entity_translated.exclude_from_indexes,
                         set(['string_key_one', 'int32_field_two', 'string_key_three']))

        entity_translated.key = self.client.key('ExampleModelWithOptions', 'exclude_from_index_1')
        self.client.put(entity_translated)

        entity_translated_retrieved = self.client.get(entity_translated.key)
        self.assertEqual(entity_translated, entity_translated_retrieved)

    def test_model_pb_to_entity_pb_exclude_from_index_custom_extension_model_with_package(self):
        # type: () -> None
        from tests.generated.models import example_with_options_pb2

        model_pb = example_with_options_pb2.ExampleDBModelWithOptions1()
        model_pb.string_key_one = 'one'
        model_pb.string_key_two = 'two'
        model_pb.string_key_three = 'three'
        model_pb.string_key_four = 'four'
        model_pb.int32_field_one = 111
        model_pb.int32_field_two = 222

        entity_pb = model_pb_to_entity_pb(model_pb=model_pb)

        entity_translated = datastore.helpers.entity_from_protobuf(entity_pb)
        self.assertEqual(entity_translated.exclude_from_indexes,
                         set(['string_key_one', 'int32_field_two', 'string_key_three']))

        entity_translated.key = self.client.key('ExampleModelWithOptions', 'exclude_from_index_1')
        self.client.put(entity_translated)

        entity_translated_retrieved = self.client.get(entity_translated.key)
        self.assertEqual(entity_translated, entity_translated_retrieved)
