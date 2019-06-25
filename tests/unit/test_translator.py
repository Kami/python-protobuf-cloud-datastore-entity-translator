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

from google.cloud import datastore

from tests.generated import example_pb2
from tests.mocks import EXAMPLE_DICT_POPULATED
from tests.mocks import EXAMPLE_DICT_DEFAULT_VALUES
from tests.mocks import EXAMPLE_PB_POPULATED
from tests.mocks import EXAMPLE_PB_DEFAULT_VALUES

from src.translator import model_pb_to_entity_pb
from src.translator import entity_pb_to_model_pb

__all__ = [
    'ModelPbToEntityPbTranslatorTestCase'
]


class ModelPbToEntityPbTranslatorTestCase(unittest.TestCase):
    maxDiff = None

    def test_translate_roundtrip(self):
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

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb, is_top_level=True)

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

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb, is_top_level=True)

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
        entity_pb_empty_translated = model_pb_to_entity_pb(model_pb=example_pb_empty,
                                                           is_top_level=True)

        self.assertEqual(entity_pb_empty_translated, entity_pb_translated)
        self.assertEqual(entity_pb_empty_translated, entity_pb_native)
