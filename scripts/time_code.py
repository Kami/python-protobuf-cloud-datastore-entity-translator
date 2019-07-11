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

"""
Scripts which times / measures duration of run time of the functions provided by this library.
"""

import os
import sys
import timeit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(BASE_DIR, '../'))
sys.path.append(os.path.join(BASE_DIR, '../tests/generated/'))

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb

from tests.generated import example_pb2
from tests.mocks import EXAMPLE_PB_POPULATED
from tests.mocks import EXAMPLE_PB_DEFAULT_VALUES

ITERATIONS_COUNT = 1000


complex_example_pb = EXAMPLE_PB_POPULATED
complex_entity_pb = model_pb_to_entity_pb(model_pb=complex_example_pb)

simple_example_pb = EXAMPLE_PB_DEFAULT_VALUES
simple_entity_pb = model_pb_to_entity_pb(model_pb=simple_example_pb)


def measure_model_pb_to_entity_pb_complex_model():
    model_pb_to_entity_pb(model_pb=complex_example_pb)


def measure_entity_pb_to_model_pb_complex_model():
    entity_pb_to_model_pb(example_pb2.ExampleDBModel, complex_entity_pb)


def measure_model_pb_to_entity_pb_simple_model():
    model_pb_to_entity_pb(model_pb=simple_example_pb)


def measure_entity_pb_to_model_pb_simple_model():
    entity_pb_to_model_pb(example_pb2.ExampleDBModel, simple_entity_pb)


duration1 = (timeit.timeit(measure_model_pb_to_entity_pb_complex_model,
                           number=ITERATIONS_COUNT) / ITERATIONS_COUNT)
duration2 = (timeit.timeit(measure_entity_pb_to_model_pb_complex_model,
                           number=ITERATIONS_COUNT) / ITERATIONS_COUNT)

print('Complex Protobuf model')
print('')
print('Average run time for model_pb_to_entity_pb: %.1f ms' % (1000 * (duration1)))
print("Average run time for entity_pb_to_model_pb: %.1f ms" % (1000 * (duration2)))

duration1 = (timeit.timeit(measure_model_pb_to_entity_pb_simple_model,
                           number=ITERATIONS_COUNT) / ITERATIONS_COUNT)
duration2 = (timeit.timeit(measure_entity_pb_to_model_pb_simple_model,
                           number=ITERATIONS_COUNT) / ITERATIONS_COUNT)

print('')
print('Simple Protobuf model with default values')
print('')
print('Average run time for model_pb_to_entity_pb: %.1f ms' % (1000 * (duration1)))
print("Average run time for entity_pb_to_model_pb: %.1f ms" % (1000 * (duration2)))
