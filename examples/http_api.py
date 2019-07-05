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

"""
Simple HTTP server which allows users to retrieve and store arbitrary Protobuf objects inside Cloud
Datastore.

To run it:

$ PYTHONPATH=. gunicorn examples/http_api.py:app
"""

from typing import Tuple
from typing import Dict

from flask import Flask
from flask import request

from google.protobuf import json_format
from google.cloud import datastore

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb
from protobuf_cloud_datastore_translator.utils import get_module_and_class_for_model_name

app = Flask(__name__)


@app.route('/datastore/put/<key>', methods=['POST'])
def put_db_object(key):
    # type: (str) -> Tuple[str, int, Dict[str, str]]
    """
    Store arbitrary Protobuf object in Google Datastore.

    NOTE: Request body needs to contain Protobuf model serialized as JSON.
    """
    body = request.get_json()

    # Fully qualified model name, e.g. "tests.generated.example_pb2.ExampleDBModel"
    # NOTE: This module needs to be available in PYTHONPATH
    model_name = body['model_name']
    model_data = body['json_string']

    _, model_class = get_module_and_class_for_model_name(model_name=model_name)

    model_pb = json_format.Parse(model_data, model_class())

    # 2. Convert it into entity object
    entity_pb = model_pb_to_entity_pb(model_pb)

    client = datastore.Client()

    # Set PK on the object
    key_pb = client.key(model_pb.DESCRIPTOR.name, key).to_protobuf()
    entity_pb.key.CopyFrom(key_pb)  # pylint: disable=no-member

    # 3. Store it inside datastore
    entity = datastore.helpers.entity_from_protobuf(entity_pb)
    client.put(entity)
    return '', 200, {}


@app.route('/datastore/get/<key>')
def get_db_object(key):
    # type: (str) -> Tuple[str, int, Dict[str, str]]
    """
    Retrieve object from Google Datastore, serialize it into native object type and serialize it
    as JSON.
    """
    model_name = request.args.get('model_name', '')
    raw = request.args.get('raw', 'false').lower() in ['1', 'true', 'yes']
    _, model_class = get_module_and_class_for_model_name(model_name=model_name)

    class_name = model_class.DESCRIPTOR.name

    # 1. Retrieve Entity from datastore
    client = datastore.Client()

    key = client.key(class_name, key)
    entity = client.get(key)

    # 2. Translate it to custom Protobuf object
    entity_pb = datastore.helpers.entity_to_protobuf(entity)

    if not raw:
        model_pb = entity_pb_to_model_pb(model_pb_class=model_class, entity_pb=entity_pb)
    else:
        model_pb = entity_pb

    # 3. Serialize it to JSON
    model_pb_json = json_format.MessageToJson(model_pb)

    return model_pb_json, 200, {'Content-Type': 'application/json'}
