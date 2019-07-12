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

import unittest

from protobuf_cloud_datastore_translator.utils import get_module_and_class_for_model_name
from tests.generated import example_pb2


class UtilsTestCase(unittest.TestCase):
    def test_get_module_and_class_for_model_name_success(self):
        model_name = 'tests.generated.example_pb2.ExampleDBModel'
        module, model_class = get_module_and_class_for_model_name(model_name)
        self.assertEqual(module, example_pb2)
        self.assertEqual(model_class, example_pb2.ExampleDBModel)

    def test_get_module_and_class_for_model_name_invalid_module_name(self):
        expected_msg = 'Class "some.not.found.Foo" not found'
        self.assertRaisesRegexp(ValueError, expected_msg, get_module_and_class_for_model_name,
                                'some.not.found.Foo')

    def test_get_module_and_class_for_model_name_invalid_class_name(self):
        model_name = 'tests.generated.example_pb2.Foo'
        expected_msg = 'Class "tests.generated.example_pb2.Foo" not found'
        self.assertRaisesRegexp(ValueError, expected_msg, get_module_and_class_for_model_name,
                                model_name)
