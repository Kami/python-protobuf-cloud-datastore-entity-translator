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

from __future__ import absolute_import

__all__ = [
    'model_pb_to_entity_pb',
    'model_pb_with_key_to_entity_pb',
    'entity_pb_to_model_pb'
]

__version__ = '0.1.0'

from .translator import model_pb_to_entity_pb
from .translator import model_pb_with_key_to_entity_pb
from .translator import entity_pb_to_model_pb
