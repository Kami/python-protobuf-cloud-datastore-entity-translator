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

import os
import time
import unittest

import requests
from google.cloud import datastore

from tests.mocks import EmulatorCreds

__all__ = [
    'BaseDatastoreIntegrationTestCase'
]

START_EMULATOR_STRING = """
gcloud beta emulators datastore start --host-port=127.0.0.1:8081 --no-store-on-disk --consistency=1
""".strip()


class BaseDatastoreIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        # type: () -> None
        super(BaseDatastoreIntegrationTestCase, self).setUp()

        # Set environment variables which are needed for emulator to work
        os.environ['DATASTORE_DATASET'] = 'translator-tests'
        os.environ['DATASTORE_PROJECT_ID'] = 'translator-tests'
        os.environ['DATASTORE_EMULATOR_HOST'] = 'localhost:8081'
        os.environ['DATASTORE_EMULATOR_HOST_PATH'] = 'localhost:8081/datastore'
        os.environ['DATASTORE_HOST'] = 'http://localhost:8081'

        # 1. Verify datastore emulator is running
        try:
            requests.get(os.environ['DATASTORE_HOST'], timeout=1)
        except requests.exceptions.ConnectionError as e:
            raise ValueError('Can\'t reach "%s". Make sure Google Cloud Datastore emulator is '
                    'running and listening on "%s": %s.\n\nYou can start emulator using "%s" '
                    'command.' % (os.environ['DATASTORE_HOST'],
                                  os.environ['DATASTORE_EMULATOR_HOST'], str(e),
                                  START_EMULATOR_STRING))

        # Instantiate client with mock credentials object
        self.client = datastore.Client(credentials=EmulatorCreds(),
                _http=requests.Session())
        self._clear_datastore()

    def tearDown(self):
        # type: () -> None
        super(BaseDatastoreIntegrationTestCase, self).tearDown()

        self._clear_datastore()

    def _clear_datastore(self):
        # type: () -> None
        # Clear datastore, ensure it's empty
        query = self.client.query(kind='__kind__')
        query.keys_only()

        kinds = [entity.key.id_or_name for entity in query.fetch()]

        for kind in kinds:
            query = self.client.query(kind=kind)
            query.keys_only()

            # Work around for eventual consistency nature of the emulator
            for index in range(0, 3):
                entity_keys = [entity.key for entity in query.fetch()]
                self.client.delete_multi(entity_keys)
                time.sleep(0.1)

            query = self.client.query(kind=kind)
            query.keys_only()
            result = list(query.fetch())

            self.assertEqual(len(result), 0)
