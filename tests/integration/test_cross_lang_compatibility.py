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

from typing import Dict

import os
import json
import uuid
import unittest
import subprocess

import requests
from google.cloud import datastore

from tests.mocks import EmulatorCreds

__all__ = [
    'CrossLangCompatibilityIntegrationTestCase'
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_PATH = os.path.join(BASE_DIR, 'fixtures/')

PYTHON_INSERT_GET_SCRIPT_PATH = os.path.join(BASE_DIR, 'python/python-put-get-db-model.py')
GO_INSERT_GET_SCRIPT_PATH = os.path.join(BASE_DIR, 'go', 'go-put-get-db-model')


class CrossLangCompatibilityIntegrationTestCase(unittest.TestCase):
    """
    Integration test which verifies that the output by Python and Go translator
    library is exactly the same.
    """

    maxDiff = None

    FIXTURES = [
        {
            'path': os.path.join(FIXTURES_PATH, 'example_db_model_1.json'),
            'key': str(uuid.uuid4()),
            'entity_kind': 'ExampleCompatDBModel'
        }
    ]

    def setUp(self):
        # type: () -> None
        super(CrossLangCompatibilityIntegrationTestCase, self).setUp()

        self.client = datastore.Client(credentials=EmulatorCreds(),
                        _http=requests.Session())

        # Load fixture content into memory
        for fixture_obj in self.FIXTURES:
            with open(fixture_obj['path'], 'r') as fp:
                fixture_obj['content'] = json.loads(fp.read())

    def test_put_and_get_self(self):
        # type: () -> None
        for fixture_obj in self.FIXTURES:
            self._test_fixture_obj(fixture_obj=fixture_obj)

    def _test_fixture_obj(self, fixture_obj):
        # type: (Dict[str, str]) -> None

        # Insert Protobuf model in the datastore using Python translator library
        self._python_insert_fixture(fixture_obj=fixture_obj)

        # Insert Protobuf model in the datastore using Go translator library
        self._go_insert_fixture(fixture_obj=fixture_obj)

        # Verify entity has been inserted
        key_python = self.client.key(fixture_obj['entity_kind'], 'python_' + fixture_obj['key'])
        key_go = self.client.key(fixture_obj['entity_kind'], 'go_' + fixture_obj['key'])

        entity_python_pb = self.client.get_entity_pb(key_python)
        entity_go_pb = self.client.get_entity_pb(key_go)

        self.assertTrue(entity_python_pb, 'Entity with key "%s" not found' % (key_python))
        self.assertTrue(entity_go_pb, 'Entity with key "%s" not found' % (key_go))

        # Reset keys since they will always be different
        entity_python_pb.ClearField('key')
        entity_go_pb.ClearField('key')

        # Compare the raw entity result
        msg = 'Translated Entity PB objects for Python and Go don\'t match'
        self.assertEqual(repr(entity_python_pb), repr(entity_go_pb), msg)

        # Compare translated models

        # First perform a sanity test and make sure it matches the original fixture input
        model_pb_json_python = self._python_get_fixture(fixture_obj=fixture_obj)
        self.assertDictsEqualIgnoreMissingDefaultValues(model_pb_json_python, fixture_obj['content'])

        model_pb_json_go = self._go_get_fixture(fixture_obj=fixture_obj)
        self.assertDictsEqualIgnoreMissingDefaultValues(model_pb_json_go, fixture_obj['content'])

        # Now compare Python and Go versions and make sure they match
        self.assertDictsEqualIgnoreMissingDefaultValues(model_pb_json_python, model_pb_json_go)

    def assertDictsEqualIgnoreMissingDefaultValues(self, model_pb_python, model_pb_go):
        """
        Custom assertion function which asserts that the provided Model PB returned by the Python
        translator library and the one returned by the Go one serialized as JSON are the same.

        NOTE: We need a custom assert functions because there are some differences between JSON
        <-> PB serialized in Python and Go and we use JSON as an intermediate format for our test
        fixtures.
        """
        field_names = set(model_pb_python.keys())
        field_names.update(model_pb_go.keys())

        for field_name in field_names:
            # NOTE: Due to the JSON serializer differences there can be some default values
            # missing
            value_python = model_pb_python.get(field_name, None)
            value_go = model_pb_go.get(field_name, None)

            if not value_python and not value_go:
                value_python = None
                value_go = None

            msg = 'Field "%s" on Python and Go Model PB object didn\'t match' % (field_name)
            self.assertEqual(value_python, value_go, msg)

    def _python_insert_fixture(self, fixture_obj):
        # type: (Dict[str, str]) -> None
        args = [
            'python',
            PYTHON_INSERT_GET_SCRIPT_PATH,
            '--operation=put',
            '--fixture-path=%s' % (fixture_obj['path']),
            '--primary-key=python_%s' % (fixture_obj['key']),
        ]
        process = subprocess.run(args, shell=False, capture_output=True)

        if process.returncode != 0:
            self.assertFalse('Failed to run command "%s": %s' % (args, process.stderr))

    def _go_insert_fixture(self, fixture_obj):
        # type: (Dict[str, str]) -> None
        args = [
            GO_INSERT_GET_SCRIPT_PATH,
            '-type=put',
            '-json-file=%s' % (fixture_obj['path']),
            '-primary-key=go_%s' % (fixture_obj['key']),
        ]
        process = subprocess.run(args, shell=False, capture_output=True)

        if process.returncode != 0:
            self.assertFalse('Failed to run command "%s": %s' % (args, process.stderr))

    def _python_get_fixture(self, fixture_obj):
        # type: (Dict[str, str]) -> Dict
        args = [
            'python',
            PYTHON_INSERT_GET_SCRIPT_PATH,
            '--operation=get',
            '--primary-key=python_%s' % (fixture_obj['key']),
        ]
        process = subprocess.run(args, shell=False, capture_output=True)

        if process.returncode != 0:
            self.assertFalse('Failed to run command "%s": %s' % (args, process.stderr))

        json_parsed = json.loads(process.stdout)

        return json_parsed

    def _go_get_fixture(self, fixture_obj):
        # type: (Dict[str, str]) -> Dict
        args = [
            GO_INSERT_GET_SCRIPT_PATH,
            '-type=get',
            '-primary-key=go_%s' % (fixture_obj['key']),
        ]
        process = subprocess.run(args, shell=False, capture_output=True)

        if process.returncode != 0:
            self.assertFalse('Failed to run command "%s": %s' % (args, process.stderr))

        json_parsed = json.loads(process.stdout)

        return json_parsed
