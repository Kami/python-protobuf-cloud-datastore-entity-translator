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

import importlib
from typing import Type
from typing import Tuple
from types import ModuleType

from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType


__all__ = [
    'get_module_and_class_for_model_name'
]


def get_module_and_class_for_model_name(model_name):
    # type: (str) -> Tuple[ModuleType, Type[GeneratedProtocolMessageType]]
    split = model_name.rsplit('.', 1)

    if len(split) != 2:
        raise ValueError('Invalid module name: %s' % (model_name))

    module_path, class_name = split

    try:
        module = importlib.import_module(module_path)
        model_class = getattr(module, class_name, None)
    except Exception as e:
        raise ValueError('Class "%s" not found: %s. Make sure "%s" is in PYTHONPATH' %
                         (model_name, module_path, str(e)))

    if not model_class:
        raise ValueError('Class "%s" not found in module "%s"' % (model_name, module_path))

    return module, model_class
