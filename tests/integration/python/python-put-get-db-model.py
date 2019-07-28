#!/usr/bin/env python
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
import sys
import logging
import argparse

import requests
from google.cloud import datastore
from google.protobuf import json_format

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb
from protobuf_cloud_datastore_translator.utils import get_module_and_class_for_model_name

from tests.mocks import EmulatorCreds  # type: ignore

__all__ = [
    'get_db_model',
    'insert_db_model'
]

LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)

LOG.addHandler(handler)

MODEL_NAME = 'compat.example_compat_pb2.ExampleCompatDBModel'


def get_db_model(model_name, primary_key):
    # type: (str, str) -> bool
    module, model_class = get_module_and_class_for_model_name(model_name)

    # 1. Retrieve model from datastore
    if os.environ.get('DATASTORE_EMULATOR_HOST'):
        client = datastore.Client(credentials=EmulatorCreds(), _http=requests.Session())
    else:
        client = datastore.Client()

    model_name = model_name.split('.')[-1]
    key = client.key(model_name, primary_key)

    # 2. Convert it into our model pb and JSON serialize it
    LOG.debug('Retrieving model with primary key "%s" from database' % (key))
    entity = client.get(key)

    if not entity:
        raise ValueError('Entity with key "%s" not found' % (key))

    entity_pb = datastore.helpers.entity_to_protobuf(entity)

    LOG.debug('Converting it from Entity PB to DB model PB')

    model_pb = entity_pb_to_model_pb(model_class, entity_pb)

    LOG.debug('Serializing Protobuf model as JSON')

    model_pb_json = json_format.MessageToJson(
        model_pb, preserving_proto_field_name=True, including_default_value_fields=True
    )
    print(model_pb_json)

    return True


def insert_db_model(fixture_path, model_name, primary_key):
    # type: (str, str, str) -> bool
    LOG.debug('Loading fixture from "%s"', fixture_path)

    # 1. Load in JSON fixture
    with open(fixture_path, 'r') as fp:
        model_pb_json = fp.read()

    # 2. Parse it in our custom Protobuf DB model type
    module, model_class = get_module_and_class_for_model_name(model_name)

    LOG.debug('Parsing JSON fixture as Protobuf message')
    model_pb = json_format.Parse(model_pb_json, model_class())

    # 3. Translate it into Entity PB
    LOG.debug('Translating Protobuf PB to Entity PB')
    entity_pb = model_pb_to_entity_pb(model_pb)

    # 4. Store it in Datastore
    if os.environ.get('DATASTORE_EMULATOR_HOST'):
        client = datastore.Client(credentials=EmulatorCreds(), _http=requests.Session())
    else:
        client = datastore.Client()

    model_name = model_pb.DESCRIPTOR.name
    key = client.key(model_name, primary_key)
    key_pb = key.to_protobuf()
    entity_pb.key.CopyFrom(key_pb)  # pylint: disable=no-member

    LOG.debug('Storing it in datastore under primary key "%s"', key)
    client.put_entity_pb(entity_pb)
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get / Insert model DB fixture from / to a '
                                                 'datastore')
    parser.add_argument(
        '--fixture-path', action='store', required=False, help=('Path to the JSON fixture file.')
    )
    parser.add_argument(
        '--operation', action='store', required=True, help=(
            'Operation name - get / put'
        )
    )
    parser.add_argument(
        '--primary-key', action='store', required=True,
        help=('Primary key to use when writting entity to the datastore.')
    )

    args = parser.parse_args()

    if args.operation not in ['get', 'put']:
        raise ValueError('Invalid operation: %s' % (args.operation))

    if args.operation == 'get':
        get_db_model(model_name=MODEL_NAME, primary_key=args.primary_key)
    elif args.operation == 'put':
        if not args.fixture_path:
            raise ValueError('--fixture-path argument not provided')

        insert_db_model(
            fixture_path=args.fixture_path, model_name=MODEL_NAME, primary_key=args.primary_key
        )
