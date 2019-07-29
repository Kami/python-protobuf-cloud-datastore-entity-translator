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
import unittest

import mock

from protobuf_cloud_datastore_translator.translator import get_python_module_for_field
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

        expected_msg = 'Invalid module name:'
        self.assertRaisesRegexp(ValueError, expected_msg, get_module_and_class_for_model_name,
                                'invalid')

    def test_get_module_and_class_for_model_name_invalid_class_name(self):
        model_name = 'tests.generated.example_pb2.Foo'
        expected_msg = 'Class "tests.generated.example_pb2.Foo" not found'
        self.assertRaisesRegexp(ValueError, expected_msg, get_module_and_class_for_model_name,
                                model_name)

    def test_get_python_module_for_field(self):
        module_name = 'example_pb2'
        full_module_name = 'tests.generated.example_pb2'

        # Module not in sys.module yet
        field = mock.Mock()
        field.message_type.file.name = module_name

        self._remove_module_from_sys_module(module_name)
        self._remove_module_from_sys_module(full_module_name)

        self.assertFalse(module_name in sys.modules)
        self.assertFalse(full_module_name in sys.modules)

        module = get_python_module_for_field(field=field)

        self.assertTrue(module)
        self.assertTrue(module_name in sys.modules)
        self.assertEqual(module.__name__, module_name)

        # Module already in sys.modules
        self.assertTrue(module_name in sys.modules)

        module = get_python_module_for_field(field=field)
        self.assertTrue(module)
        self.assertTrue(module_name in sys.modules)
        self.assertEqual(module.__name__, module_name)

        # Module already in sys.modules under an alias
        self._remove_module_from_sys_module(module_name)
        self._remove_module_from_sys_module(full_module_name)

        sys.modules[full_module_name] = module

        self.assertFalse(module_name in sys.modules)
        self.assertTrue(full_module_name in sys.modules)

        module = get_python_module_for_field(field=field)
        self.assertTrue(module)
        self.assertTrue(full_module_name in sys.modules)
        self.assertEqual(module.__name__, module_name)

    def test_get_python_module_for_field_invalid_module_name(self):
        field = mock.Mock()
        field.message_type.file.name = 'invalid.module'

        expected_msg = 'No module named'
        self.assertRaisesRegexp(ImportError, expected_msg,
                                get_python_module_for_field, field)

    def _remove_module_from_sys_module(self, module_name):
        if module_name in sys.modules:
            del sys.modules[module_name]
