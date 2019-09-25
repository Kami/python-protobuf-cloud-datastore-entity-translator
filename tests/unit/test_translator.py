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
# pylint: disable=all

import sys
import copy
import unittest

import requests
from google.cloud import datastore
from google.cloud.datastore_v1.proto import entity_pb2
from google.protobuf import struct_pb2
from google.type import latlng_pb2

from tests.generated import example_pb2
from tests.generated import example2_pb2
from tests.generated.models import example3_pb2

from tests.mocks import EmulatorCreds
from tests.mocks import EXAMPLE_DICT_POPULATED
from tests.mocks import EXAMPLE_DICT_DEFAULT_VALUES
from tests.mocks import EXAMPLE_PB_POPULATED
from tests.mocks import EXAMPLE_PB_DEFAULT_VALUES

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import model_pb_with_key_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb

__all__ = [
    'ModelPbToEntityPbTranslatorTestCase'
]


class ModelPbToEntityPbTranslatorTestCase(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        super(ModelPbToEntityPbTranslatorTestCase, self).setUp()

        modules_to_remove = [
            'tests.generated.options_pb2',
            'tests.generated.models.options_pb2',
            'tests.generated.example_with_options_pb2',
            'tests.generated.models.example_with_options_pb2',
        ]

        for module_name in modules_to_remove:
            if module_name in sys.modules:
                del sys.modules[module_name]

    def test_translate_fully_populated_model_roundtrip(self):
        # type: () -> None
        # Create an instance of ExampleDBModel Protobuf message
        example_pb = EXAMPLE_PB_POPULATED

        # Create example Entity protobuf object via google-cloud-datastore library with the
        # matching values
        # NOTE: We cast any number inside the dictionary to double to work around the bug in
        # "entity_to_protobuf" not handling numbers inside structs correctly
        example_data = copy.deepcopy(EXAMPLE_DICT_POPULATED)

        example_data['struct_array_key'] = self._int_to_double(example_data['struct_array_key'])
        example_data['struct_key'] = self._int_to_double(example_data['struct_key'])

        entity = datastore.Entity()
        entity.update(example_data)

        # Verify that the both Protobuf objects are the same (translated one and the datastore
        # native one)
        entity_pb_native = datastore.helpers.entity_to_protobuf(entity)
        entity_roundtrip = datastore.helpers.entity_from_protobuf(entity_pb_native)

        # Assert that end result after round trip is the same
        self.assertEqual(entity, entity_roundtrip)

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)

        self.assertEqual(repr(entity_pb_native), repr(entity_pb_translated))
        self.assertEqual(entity_pb_native, entity_pb_translated)
        self.assertEqual(sorted(entity_pb_native.SerializePartialToString()),
            sorted(entity_pb_translated.SerializePartialToString()))

        # Try converting it back to the original entity and verify it matches the input
        example_pb_converted = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb_native)
        self.assertEqual(example_pb_converted, example_pb)
        self.assertEqual(sorted(example_pb_converted.SerializePartialToString()),
            sorted(example_pb.SerializePartialToString()))

    def test_struct_field_type_number_values(self):
        # NOTE: Keep in mind that struct only supports double number types and not integers
        example_pb = EXAMPLE_PB_POPULATED

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)

        # Verify that all the number values either top level, or nested or inside a list are
        # correctly serialized to a double value
        # Top level attribute
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key2'].double_value, 2.0)

        # Array attribute
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key3'].array_value.values[0].double_value,
                         1.0)
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key3'].array_value.values[1].double_value,
                         2.0)
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key3'].array_value.values[2].double_value,
                         3.0)
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key3'].array_value.values[3].double_value,
                         4.44)

        # Nested struct attribute
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key5'].entity_value.properties['dict_key_2'].double_value,
                         30.0)
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key5'].entity_value.properties['dict_key_3'].array_value
                         .values[3].double_value,
                         7.0)

        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key5'].entity_value.properties['dict_key_3'].array_value
                         .values[4].entity_value.properties['g'].array_value.values[0].double_value,
                         1.0)
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key5'].entity_value.properties['dict_key_3'].array_value
                         .values[4].entity_value.properties['g'].array_value.values[1].double_value,
                         2.0)
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key5'].entity_value.properties['dict_key_3'].array_value
                         .values[4].entity_value.properties['g'].array_value.values[2].double_value,
                         33.33)

        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key5'].entity_value.properties['dict_key_5'].double_value,
                         55.55)

        # Top level attribute
        self.assertEqual(entity_pb_translated.properties['struct_key'].entity_value
                         .properties['key11'].double_value, 11.123)

        # Test the round trip conversion
        example_pb_converted = entity_pb_to_model_pb(example_pb2.ExampleDBModel,
                                                     entity_pb_translated)

        self.assertEqual(example_pb_converted.struct_key['key2'], 2.0)
        self.assertEqual(example_pb_converted.struct_key['key3'][0], 1)
        self.assertEqual(example_pb_converted.struct_key['key3'][1], 2)
        self.assertEqual(example_pb_converted.struct_key['key3'][2], 3)
        self.assertEqual(example_pb_converted.struct_key['key3'][3], 4.44)
        self.assertEqual(example_pb_converted.struct_key['key5']['dict_key_2'], 30)
        self.assertEqual(example_pb_converted.struct_key['key5']['dict_key_3'][3], 7)
        self.assertEqual(example_pb_converted.struct_key['key5']['dict_key_3'][4]['g'][0], 1)
        self.assertEqual(example_pb_converted.struct_key['key5']['dict_key_3'][4]['g'][1], 2)
        self.assertEqual(example_pb_converted.struct_key['key5']['dict_key_3'][4]['g'][2], 33.33)
        self.assertEqual(example_pb_converted.struct_key['key5']['dict_key_5'], 55.55)
        self.assertEqual(example_pb_converted.struct_key['key11'], 11.123)

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

        self.assertEqual(repr(entity_pb_native), repr(entity_pb_translated))
        self.assertEqual(entity_pb_native, entity_pb_translated)
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

        geo_point_value = latlng_pb2.LatLng(latitude=-20.2, longitude=+160.5)

        example_pb = example_pb2.ExampleDBModel()
        example_pb.geo_point_key.CopyFrom(geo_point_value)

        entity_pb_serialized = model_pb_to_entity_pb(model_pb=example_pb, exclude_falsy_values=True)
        self.assertEntityPbHasPopulatedField(entity_pb_serialized,
                'geo_point_key')
        self.assertEqual(entity_pb_serialized.properties['geo_point_key'].geo_point_value.latitude,
            -20.2)
        self.assertEqual(entity_pb_serialized.properties['geo_point_key'].geo_point_value.longitude,
            +160.5)

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

    def test_model_pb_to_entity_pb_invalid_argument_type(self):
        # type: () -> None
        class Invalid(object):
            pass

        example_pb = Invalid()

        expected_msg = 'model_pb argument is not a valid Protobuf class instance'
        self.assertRaisesRegexp(ValueError, expected_msg, model_pb_to_entity_pb,
                                example_pb)  # type: ignore

    def test_model_pb_with_key_to_entity_pb_invalid_argument_type(self):
        # type: () -> None
        class Invalid(object):
            pass

        client = datastore.Client(credentials=EmulatorCreds(), _http=requests.Session(),
                                  namespace='namespace1', project='project1')
        example_pb = Invalid()

        expected_msg = 'model_pb argument is not a valid Protobuf class instance'
        self.assertRaisesRegexp(ValueError, expected_msg, model_pb_with_key_to_entity_pb, client,
                                example_pb)

    def test_entity_pb_to_model_pb_strict_mode(self):
        # type: () -> None

        entity_pb = entity_pb2.Entity()
        entity_native = datastore.Entity()
        entity_native.update({'string_key': 'test value', 'int32_key': 20, 'non_valid_key': 'bar'})
        entity_pb = datastore.helpers.entity_to_protobuf(entity_native)

        # 1. Not using strict mode. Field which is available on the Entity object, but not model
        # object should be ignored
        example_pb = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb)

        self.assertEqual(example_pb.string_key, 'test value')
        self.assertEqual(example_pb.int32_key, 20)
        self.assertEqual(example_pb.int32_key, 20)
        self.assertRaises(AttributeError, getattr, example_pb, 'non_valid_key')

        example_pb = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb,
                                          strict=False)

        self.assertEqual(example_pb.string_key, 'test value')
        self.assertEqual(example_pb.int32_key, 20)
        self.assertRaises(AttributeError, getattr, example_pb, 'non_valid_key')

        # 2. Using strict mode, exception should be thrown
        expected_msg = ('Database object contains field "non_valid_key" which is not defined on '
                        'the database model class "ExampleDBModel"')
        self.assertRaisesRegexp(ValueError, expected_msg, entity_pb_to_model_pb,
                                example_pb2.ExampleDBModel, entity_pb, strict=True)

    def test_entity_pb_to_model_pb_null_type(self):
        entity_pb = entity_pb2.Entity()
        null_value = entity_pb.properties.get_or_create('null_key')
        null_value.null_value = 0

        model_pb = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb)
        self.assertEqual(model_pb.null_key, 0)

        entity_pb = entity_pb2.Entity()
        null_value = entity_pb.properties.get_or_create('null_key')
        null_value.null_value = 1

        model_pb = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb)
        self.assertEqual(model_pb.null_key, 0)

    def test_entity_pb_to_model_pb_geopoint_type(self):
        entity_pb = entity_pb2.Entity()

        latlng_value = latlng_pb2.LatLng(latitude=-20.2, longitude=+160.5)

        geo_point_value = entity_pb.properties.get_or_create('geo_point_key')
        geo_point_value.geo_point_value.CopyFrom(latlng_value)

        model_pb = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb)
        self.assertEqual(model_pb.geo_point_key.latitude, -20.2)
        self.assertEqual(model_pb.geo_point_key.longitude, +160.5)

        latlng_value = latlng_pb2.LatLng(latitude=0.0, longitude=0.0)

        geo_point_value = entity_pb.properties.get_or_create('geo_point_key')
        geo_point_value.geo_point_value.CopyFrom(latlng_value)

        model_pb = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb)
        self.assertEqual(model_pb.geo_point_key.latitude, 0.0)
        self.assertEqual(model_pb.geo_point_key.longitude, 0.0)

    def test_model_pb_to_entity_pb_referenced_type(self):
        # Test a scenario where model pb references a type from another protobuf file
        example_referenced_type_pb = example2_pb2.ExampleReferencedType()
        example_referenced_type_pb.key_1 = 'value 1'
        example_referenced_type_pb.key_2 = 'value 2'

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_referenced_type_pb)
        self.assertEqual(entity_pb_translated.properties['key_1'].string_value, 'value 1')
        self.assertEqual(entity_pb_translated.properties['key_2'].string_value, 'value 2')

        example_with_package_referenced_type_pb = example3_pb2.ExampleWithPackageDBModel()
        example_with_package_referenced_type_pb.string_key = 'value 4'

        entity_pb_translated = model_pb_to_entity_pb(
            model_pb=example_with_package_referenced_type_pb)
        self.assertEqual(entity_pb_translated.properties['string_key'].string_value, 'value 4')

        example_with_referenced_type_pb = example_pb2.ExampleWithReferencedTypeDBModel()
        example_with_referenced_type_pb.string_key = 'value 3'
        example_with_referenced_type_pb.referenced_enum = example2_pb2.ExampleReferencedEnum.KEY1
        example_with_referenced_type_pb.referenced_type_key.CopyFrom(example_referenced_type_pb)
        example_with_referenced_type_pb.referenced_package_type_key.CopyFrom(
            example_with_package_referenced_type_pb)

        example_with_nested_struct_db_model_pb = example_pb2.ExampleWithNestedStructDBModel()
        example_with_nested_struct_db_model_pb.struct_key.update({'foo': 'bar', 'bar': 'baz',
                                                                  'bool1': True, 'bool2': False,
                                                                  'number1': 100, 'number2': 22.33})

        example_with_referenced_type_pb.referenced_struct_key.CopyFrom(
            example_with_nested_struct_db_model_pb)

        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_with_referenced_type_pb)
        self.assertEqual(entity_pb_translated.properties['string_key'].string_value, 'value 3')
        self.assertEqual(entity_pb_translated.properties['referenced_enum'].integer_value, 1)
        self.assertEqual(entity_pb_translated.properties['referenced_type_key'].entity_value.
                properties['key_1'].string_value,
                'value 1')
        self.assertEqual(entity_pb_translated.properties['referenced_type_key'].entity_value.
                properties['key_2'].string_value,
                'value 2')
        self.assertEqual(entity_pb_translated.properties['referenced_package_type_key'].
                entity_value.properties['string_key'].string_value,
                'value 4')
        self.assertEqual(entity_pb_translated.properties['referenced_struct_key'].entity_value
                         .properties['struct_key'].entity_value.properties['foo'].string_value,
                         'bar')
        self.assertEqual(entity_pb_translated.properties['referenced_struct_key'].entity_value
                         .properties['struct_key'].entity_value.properties['bar'].string_value,
                         'baz')
        self.assertEqual(entity_pb_translated.properties['referenced_struct_key'].entity_value
                         .properties['struct_key'].entity_value.properties['bool1'].boolean_value,
                         True)
        self.assertEqual(entity_pb_translated.properties['referenced_struct_key'].entity_value
                         .properties['struct_key'].entity_value.properties['bool2'].boolean_value,
                         False)

        # Perform the round trip, translate it back to the model and verity it matches the original
        # input
        model_pb_round_trip = entity_pb_to_model_pb(example_pb2.ExampleWithReferencedTypeDBModel,
                                                    entity_pb_translated)
        self.assertEqual(model_pb_round_trip, example_with_referenced_type_pb)

    def test_model_pb_to_entity_pb_nested_struct_roundtrip(self):
        # type: () -> None
        example_data = {
            'key1': u'val1',
            'key2': 2,
            'key3': [1, 2, 3],
            'key4': u'čđć',
            'key5': {
                'dict_key_1': u'1',
                'dict_key_2': 30,
                'dict_key_3': [u'a', u'b', u'c', 3,
                               {u'f': u'h', u'm': [20, 30, 40], u'g': {u'foo': u'bar'}}],
                'dict_key_4': {u'1': 1.1, u'2': 2.2, u'3': 3.33}

            }
        }

        example_pb = example_pb2.ExampleWithNestedStructDBModel()
        example_pb.struct_key.update(example_data)
        entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)

        # Verify that the both Protobuf objects are the same (translated one and the datastore
        # native one)

        # NOTE: We cast any number inside the dictionary to double to work around the bug in
        # "entity_to_protobuf" not handling numbers inside structs correctly
        example_data = self._int_to_double(example_data)
        entity = datastore.Entity()
        entity.update({'struct_key': example_data})

        entity_pb_native = datastore.helpers.entity_to_protobuf(entity)

        self.assertEqual(repr(entity_pb_native), repr(entity_pb_translated))
        self.assertEqual(entity_pb_translated, entity_pb_native)
        self.assertEqual(sorted(entity_pb_native.SerializePartialToString()),
            sorted(entity_pb_translated.SerializePartialToString()))

        # Try converting it back to the original Protobuf object and verify it matches the input
        example_pb_converted = entity_pb_to_model_pb(example_pb2.ExampleWithNestedStructDBModel,
                                                     entity_pb_translated)
        self.assertEqual(example_pb_converted, example_pb)
        self.assertEqual(sorted(example_pb_converted.SerializePartialToString()),
            sorted(example_pb.SerializePartialToString()))

    def test_model_pb_to_entity_pb_repeated_referenced_field_with_enum_field(self):
        # type: () -> None
        # Test a scenario where a repeated field references a nested type which contains an ENUM
        # and ensure that default enum value (0) is correctly set either when it's explicitly
        # provided or when it's not provided and a default value is used.
        example_pb = example_pb2.ExampleDBModel()

        example_placeholder_pb1 = example_pb2.ExampleNestedModel(string_key=u'value 1',
            int32_key=12345)
        example_placeholder_pb1.enum_key = example_pb2.ExampleEnumModel.ENUM2  # type: ignore
        # Enum with value 0 is explicitly provided
        example_placeholder_pb2 = example_pb2.ExampleNestedModel(string_key=u'value 2',
           int32_key=5000)
        example_placeholder_pb2.enum_key = example_pb2.ExampleEnumModel.ENUM0  # type: ignore
        # Enum value is not provided, default value 0 should be used
        example_placeholder_pb3 = example_pb2.ExampleNestedModel(string_key=u'value 3',
            int32_key=40)

        example_pb.complex_array_key.append(example_placeholder_pb1)  # type: ignore
        example_pb.complex_array_key.append(example_placeholder_pb2)  # type: ignore
        example_pb.complex_array_key.append(example_placeholder_pb3)  # type: ignore

        self.assertEqual(example_pb.complex_array_key[0].enum_key, 2)
        self.assertEqual(example_pb.complex_array_key[1].enum_key, 0)
        self.assertEqual(example_pb.complex_array_key[2].enum_key, 0)

        # Serialize it and ensure "0" enum values are included
        entity_pb = model_pb_to_entity_pb(model_pb=example_pb)
        self.assertEqual(len(entity_pb.properties['complex_array_key'].array_value.values), 3)
        self.assertEqual(entity_pb.properties['complex_array_key'].array_value.values[0]
                .entity_value.properties['enum_key'].integer_value,
            example_pb2.ExampleEnumModel.ENUM2)
        self.assertEqual(entity_pb.properties['complex_array_key'].array_value.values[1]
                .entity_value.properties['enum_key'].integer_value,
            example_pb2.ExampleEnumModel.ENUM0)
        self.assertEqual(entity_pb.properties['complex_array_key'].array_value.values[2]
                .entity_value.properties['enum_key'].integer_value,
            example_pb2.ExampleEnumModel.ENUM0)

    def test_model_pb_to_entity_pb_exclude_from_index_fields(self):
        # type: () -> None
        example_pb = example_pb2.ExampleDBModel()
        example_pb.int32_key = 100
        example_pb.string_key = 'string bar'
        example_pb.bytes_key = b'foobarbytes'
        example_pb.enum_key = 1  # type: ignore

        # No exclude from index provided
        entity_pb = model_pb_to_entity_pb(model_pb=example_pb)

        for field_name in ['int32_key', 'string_key', 'bytes_key', 'enum_key']:
            self.assertFalse(entity_pb.properties[field_name].exclude_from_indexes)

        # Exclude from index provided for some fields
        entity_pb = model_pb_to_entity_pb(model_pb=example_pb,
                                          exclude_from_index=['int32_key', 'bytes_key'])

        for field_name in ['int32_key', 'bytes_key']:
            self.assertTrue(entity_pb.properties[field_name].exclude_from_indexes)

        for field_name in ['string_key', 'enum_key']:
            self.assertFalse(entity_pb.properties[field_name].exclude_from_indexes)

    def test_model_pb_to_entity_pb_struct_field_null_value(self):
        example_pb = example_pb2.ExampleDBModel()
        example_pb.struct_key.update({
            'key1': None,
            'key2': [None, None],
            'key3': {'a': None}
        })
        entity_pb = model_pb_to_entity_pb(model_pb=example_pb)

        self.assertEqual(entity_pb.properties['struct_key'].entity_value
                         .properties['key1'].null_value, struct_pb2.NULL_VALUE)
        self.assertEqual(entity_pb.properties['struct_key'].entity_value.
                         properties['key2'].array_value.values[0].null_value,
                         struct_pb2.NULL_VALUE)
        self.assertEqual(entity_pb.properties['struct_key'].entity_value.
                         properties['key2'].array_value.values[1].null_value,
                         struct_pb2.NULL_VALUE)
        self.assertEqual(entity_pb.properties['struct_key'].entity_value.
                         properties['key3'].entity_value.properties['a'].null_value,
                         struct_pb2.NULL_VALUE)

    def test_model_pb_to_entity_pb_exclude_from_index_custom_extension_model_without_package(self):
        # type: () -> None
        from tests.generated import example_with_options_pb2

        # Multiple fields excluded from index
        model_pb1 = example_with_options_pb2.ExampleDBModelWithOptions1()
        model_pb1.string_key_one = 'one'
        model_pb1.string_key_two = 'two'
        model_pb1.string_key_three = 'three'
        model_pb1.string_key_four = 'four'
        model_pb1.int32_field_one = 111
        model_pb1.int32_field_two = 222

        entity_pb1 = model_pb_to_entity_pb(model_pb=model_pb1)

        self.assertEqual(entity_pb1.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb1.properties['string_key_one'].exclude_from_indexes, True)
        self.assertEqual(entity_pb1.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb1.properties['string_key_three'].exclude_from_indexes, True)
        self.assertEqual(entity_pb1.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb1.properties['int32_field_two'].exclude_from_indexes, True)

        self.assertEqual(entity_pb1.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb1.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb1.properties['string_key_four'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb1.properties['int32_field_one'].exclude_from_indexes, False)

        # One field excluded from index, other doesn't exist (should be simply ignored)
        model_pb2 = example_with_options_pb2.ExampleDBModelWithOptions2()
        model_pb2.string_key_one = 'one'
        model_pb2.string_key_two = 'two'
        model_pb2.string_key_three = 'three'
        model_pb2.string_key_four = 'four'
        model_pb2.int32_field_one = 111
        model_pb2.int32_field_two = 222

        entity_pb2 = model_pb_to_entity_pb(model_pb=model_pb2)

        self.assertEqual(entity_pb2.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb2.properties['int32_field_two'].exclude_from_indexes, True)

        self.assertEqual(entity_pb2.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb2.properties['string_key_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb2.properties['string_key_three'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb2.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb2.properties['string_key_four'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb2.properties['int32_field_one'].exclude_from_indexes, False)

        # No fields excluded from index
        model_pb3 = example_with_options_pb2.ExampleDBModelWithOptions3()
        model_pb3.string_key_one = 'one'
        model_pb3.string_key_two = 'two'
        model_pb3.string_key_three = 'three'
        model_pb3.string_key_four = 'four'
        model_pb3.int32_field_one = 111
        model_pb3.int32_field_two = 222

        entity_pb3 = model_pb_to_entity_pb(model_pb=model_pb3)

        self.assertEqual(entity_pb3.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb3.properties['string_key_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb3.properties['string_key_three'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb3.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb3.properties['string_key_four'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb3.properties['int32_field_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb3.properties['int32_field_two'].exclude_from_indexes, False)

        # exclude_from_index function argument provided, this has precedence over fields defined on
        # the model
        # Multiple fields excluded from index
        model_pb4 = example_with_options_pb2.ExampleDBModelWithOptions1()
        model_pb4.string_key_one = 'one'
        model_pb4.string_key_two = 'two'
        model_pb4.string_key_three = 'three'
        model_pb4.string_key_four = 'four'
        model_pb4.int32_field_one = 111
        model_pb4.int32_field_two = 222

        entity_pb4 = model_pb_to_entity_pb(model_pb=model_pb4,
                                           exclude_from_index=['string_key_four'])

        self.assertEqual(entity_pb4.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb4.properties['string_key_four'].exclude_from_indexes, True)

        self.assertEqual(entity_pb4.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb4.properties['string_key_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb4.properties['string_key_three'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb4.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb4.properties['int32_field_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb4.properties['int32_field_two'].exclude_from_indexes, False)

    def test_model_pb_to_entity_pb_exclude_from_index_custom_extension_model_with_package(self):
        # type: () -> None
        from tests.generated.models import example_with_options_pb2

        # Verify it also works correctly for model protobuf files which define "package" option
        # Multiple fields excluded from index
        model_pb1 = example_with_options_pb2.ExampleDBModelWithOptions1()
        model_pb1.string_key_one = 'one'
        model_pb1.string_key_two = 'two'
        model_pb1.string_key_three = 'three'
        model_pb1.string_key_four = 'four'
        model_pb1.int32_field_one = 111
        model_pb1.int32_field_two = 222

        entity_pb1 = model_pb_to_entity_pb(model_pb=model_pb1)

        self.assertEqual(entity_pb1.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb1.properties['string_key_one'].exclude_from_indexes, True)
        self.assertEqual(entity_pb1.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb1.properties['string_key_three'].exclude_from_indexes, True)
        self.assertEqual(entity_pb1.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb1.properties['int32_field_two'].exclude_from_indexes, True)

        self.assertEqual(entity_pb1.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb1.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb1.properties['string_key_four'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb1.properties['int32_field_one'].exclude_from_indexes, False)

        # One field excluded from index, other doesn't exist (should be simply ignored)
        model_pb2 = example_with_options_pb2.ExampleDBModelWithOptions2()
        model_pb2.string_key_one = 'one'
        model_pb2.string_key_two = 'two'
        model_pb2.string_key_three = 'three'
        model_pb2.string_key_four = 'four'
        model_pb2.int32_field_one = 111
        model_pb2.int32_field_two = 222

        entity_pb2 = model_pb_to_entity_pb(model_pb=model_pb2)

        self.assertEqual(entity_pb2.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb2.properties['int32_field_two'].exclude_from_indexes, True)

        self.assertEqual(entity_pb2.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb2.properties['string_key_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb2.properties['string_key_three'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb2.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb2.properties['string_key_four'].exclude_from_indexes, False)
        self.assertEqual(entity_pb2.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb2.properties['int32_field_one'].exclude_from_indexes, False)

        # No fields excluded from index
        model_pb3 = example_with_options_pb2.ExampleDBModelWithOptions3()
        model_pb3.string_key_one = 'one'
        model_pb3.string_key_two = 'two'
        model_pb3.string_key_three = 'three'
        model_pb3.string_key_four = 'four'
        model_pb3.int32_field_one = 111
        model_pb3.int32_field_two = 222

        entity_pb3 = model_pb_to_entity_pb(model_pb=model_pb3)

        self.assertEqual(entity_pb3.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb3.properties['string_key_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb3.properties['string_key_three'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb3.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb3.properties['string_key_four'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb3.properties['int32_field_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb3.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb3.properties['int32_field_two'].exclude_from_indexes, False)

        # exclude_from_index function argument provided, this has precedence over fields defined on
        # the model
        # Multiple fields excluded from index
        model_pb4 = example_with_options_pb2.ExampleDBModelWithOptions1()
        model_pb4.string_key_one = 'one'
        model_pb4.string_key_two = 'two'
        model_pb4.string_key_three = 'three'
        model_pb4.string_key_four = 'four'
        model_pb4.int32_field_one = 111
        model_pb4.int32_field_two = 222

        entity_pb4 = model_pb_to_entity_pb(model_pb=model_pb4,
                                           exclude_from_index=['string_key_four'])

        self.assertEqual(entity_pb4.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb4.properties['string_key_four'].exclude_from_indexes, True)

        self.assertEqual(entity_pb4.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb4.properties['string_key_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb4.properties['string_key_three'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb4.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb4.properties['int32_field_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb4.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb4.properties['int32_field_two'].exclude_from_indexes, False)

    def test_model_pb_to_entity_pb_exclude_from_index_custom_extension_multiple_options(self):
        # type: () -> None
        # Test a scenario where field has another custom option defined, in addition to
        # exclude_from_index (other option should be simply ignored and not affect the behavior
        # in any way)
        from tests.generated import example_with_options_pb2

        # Multiple fields excluded from index
        model_pb1 = example_with_options_pb2.ExampleDBModelWithMultipleOptions()
        model_pb1.string_key_one = 'one'
        model_pb1.string_key_two = 'two'
        model_pb1.string_key_three = 'three'
        model_pb1.string_key_four = 'four'
        model_pb1.int32_field_one = 111
        model_pb1.int32_field_two = 222

        entity_pb1 = model_pb_to_entity_pb(model_pb=model_pb1)

        self.assertEqual(entity_pb1.properties['string_key_one'].string_value, 'one')
        self.assertEqual(entity_pb1.properties['string_key_one'].exclude_from_indexes, True)

        self.assertEqual(entity_pb1.properties['string_key_two'].string_value, 'two')
        self.assertEqual(entity_pb1.properties['string_key_two'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['string_key_three'].string_value, 'three')
        self.assertEqual(entity_pb1.properties['string_key_three'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['string_key_four'].string_value, 'four')
        self.assertEqual(entity_pb1.properties['string_key_four'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['int32_field_one'].integer_value, 111)
        self.assertEqual(entity_pb1.properties['int32_field_one'].exclude_from_indexes, False)
        self.assertEqual(entity_pb1.properties['int32_field_two'].integer_value, 222)
        self.assertEqual(entity_pb1.properties['int32_field_two'].exclude_from_indexes, False)

    def test_model_pb_to_entity_pb_repeated_struct_type(self):
        struct1_pb = struct_pb2.Struct()
        struct1_pb.update({
            'key1': 'struct 1',
            'key2': 111
        })
        struct2_pb = struct_pb2.Struct()
        struct2_pb.update({
            'key4': 'struct 2',
            'key5': 222
        })

        example_pb = example_pb2.ExampleDBModel()
        example_pb.struct_array_key.append(struct1_pb)
        example_pb.struct_array_key.append(struct2_pb)

        entity_pb = model_pb_to_entity_pb(model_pb=example_pb)

        self.assertEqual(len(entity_pb.properties['struct_array_key'].array_value.values), 2)
        self.assertEqual(
            entity_pb.properties['struct_array_key'].array_value.values[0]
            .entity_value.properties['key1'].string_value,
            'struct 1')
        self.assertEqual(
            entity_pb.properties['struct_array_key'].array_value.values[0]
            .entity_value.properties['key2'].double_value,
            111)
        self.assertEqual(
            entity_pb.properties['struct_array_key'].array_value.values[1]
            .entity_value.properties['key4'].string_value,
            'struct 2')
        self.assertEqual(
            entity_pb.properties['struct_array_key'].array_value.values[1]
            .entity_value.properties['key5'].double_value,
            222)

    def test_entity_pb_to_model_pb_repeated_struct_field_type(self):
        struct1_pb = struct_pb2.Struct()
        struct1_pb.update({
            'key1': 'struct 1',
            'key2': 111,
            'key3': [1, 2, 3],
            'key4': {
                'a': 1
            }
        })
        struct2_pb = struct_pb2.Struct()
        struct2_pb.update({
            'key5': 'struct 2',
            'key6': 222,
            'key7': [4, 5, 6],
            'key8': {
                'b': 2
            }
        })

        example_pb = example_pb2.ExampleDBModel()
        example_pb.struct_array_key.append(struct1_pb)
        example_pb.struct_array_key.append(struct2_pb)

        entity_pb = model_pb_to_entity_pb(model_pb=example_pb)

        model_pb = entity_pb_to_model_pb(example_pb2.ExampleDBModel, entity_pb)
        self.assertEqual(model_pb, example_pb)

    def test_model_pb_to_entity_pb_nested_struct_empty_array(self):
        struct1_pb = struct_pb2.Struct()
        struct1_pb.update({
            'a': {
                'a': [],
                'b': {
                    'c': []
                }
            },
            'b': []
        })

        example_pb = example_pb2.ExampleDBModel()
        example_pb.struct_key.CopyFrom(struct1_pb)

        entity_pb = model_pb_to_entity_pb(model_pb=example_pb)

        self.assertEqual(
            entity_pb.properties['struct_key']
            .entity_value.properties['a']
            .entity_value.properties['b']
            .entity_value.properties['c'].array_value,
            entity_pb2.ArrayValue(values=[]))

        self.assertEqual(
            entity_pb.properties['struct_key']
            .entity_value.properties['b'].array_value,
            entity_pb2.ArrayValue(values=[]))

        self.assertEqual(
            entity_pb.properties['struct_key']
            .entity_value.properties['a']
            .entity_value.properties['a'].array_value,
            entity_pb2.ArrayValue(values=[]))

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

    def _int_to_double(self, value):
        """
        Function which converts any int value type to double to work around issue with
        "entity_to_protobuf" function which handles all the nested values as embedded entities and
        not structs which only support double type.
        """
        if isinstance(value, list):
            value = [self._int_to_double(item) for item in value]
        elif isinstance(value, dict):
            result = {}
            for dict_key, dict_value in value.items():
                result[dict_key] = self._int_to_double(dict_value)

            return result
        elif isinstance(value, bool):
            value = bool(value)
        elif isinstance(value, int):
            value = float(value)

        return value
