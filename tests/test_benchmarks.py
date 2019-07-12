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
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(BASE_DIR, '../'))
sys.path.append(os.path.join(BASE_DIR, '../tests/generated/'))

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb

from tests.generated import example_pb2
from tests.mocks import EXAMPLE_PB_POPULATED
from tests.mocks import EXAMPLE_PB_DEFAULT_VALUES


complex_example_pb = EXAMPLE_PB_POPULATED
complex_entity_pb = model_pb_to_entity_pb(model_pb=complex_example_pb)

simple_example_pb = EXAMPLE_PB_DEFAULT_VALUES
simple_entity_pb = model_pb_to_entity_pb(model_pb=simple_example_pb)


def measure_model_pb_to_entity_pb_complex_model():
    return model_pb_to_entity_pb(model_pb=complex_example_pb)


def measure_entity_pb_to_model_pb_complex_model():
    return entity_pb_to_model_pb(example_pb2.ExampleDBModel, complex_entity_pb)


def measure_model_pb_to_entity_pb_simple_model():
    return model_pb_to_entity_pb(model_pb=simple_example_pb)


def measure_entity_pb_to_model_pb_simple_model():
    return entity_pb_to_model_pb(example_pb2.ExampleDBModel, simple_entity_pb)


@pytest.mark.benchmark(
    group='model_pb_to_entity_pb',
    disable_gc=True,
    warmup=False
)
def test_model_pb_to_entity_pb_complex_model(benchmark):
    # benchmark something
    result = benchmark(measure_model_pb_to_entity_pb_complex_model)
    assert bool(result)
    assert result.properties['int32_key'].integer_value == 100


@pytest.mark.benchmark(
    group='model_pb_to_entity_pb',
    disable_gc=True,
    warmup=False
)
def test_model_pb_to_entity_pb_simple_model(benchmark):
    # benchmark something
    result = benchmark(measure_model_pb_to_entity_pb_simple_model)
    assert bool(result)
    assert result.properties['int32_key'].integer_value == 0


@pytest.mark.benchmark(
    group='entity_pb_to_model_pb',
    disable_gc=True,
    warmup=False
)
def test_entity_pb_to_model_pb_complex_entity(benchmark):
    result = benchmark(measure_entity_pb_to_model_pb_complex_model)
    assert bool(result)
    assert result.int32_key == 100


@pytest.mark.benchmark(
    group='entity_pb_to_model_pb',
    disable_gc=True,
    warmup=False
)
def test_entity_pb_to_model_pb_simple_entity(benchmark):
    result = benchmark(measure_entity_pb_to_model_pb_simple_model)
    assert bool(result)
    assert result.int32_key == 0
