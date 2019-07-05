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

import sys
import importlib

from typing import Any
from typing import Type
from typing import cast
from typing import TypeVar
from types import ModuleType
from datetime import datetime

import six

from google.cloud import datastore
from google.cloud.datastore_v1.proto import entity_pb2
from google.protobuf import message
from google.protobuf import timestamp_pb2
from google.protobuf import struct_pb2
from google.protobuf import descriptor
from google.protobuf.internal.well_known_types import _GetStructValue  # type: ignore

from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.pyext._message import MessageMapContainer
from google.protobuf.pyext._message import ScalarMapContainer
from google.protobuf.pyext._message import RepeatedScalarContainer
from google.protobuf.pyext._message import RepeatedCompositeContainer

__all__ = [
    'model_pb_to_entity_pb',
    'model_pb_with_key_to_entity_pb',
    'entity_pb_to_model_pb'
]

# Type which represents an arbitrary ModelPB class which is a subclass of message.Message
T_model_pb = TypeVar('T_model_pb', bound=message.Message)


def model_pb_with_key_to_entity_pb(client, model_pb, exclude_falsy_values=False):
    # type: (datastore.Client, message.Message, bool) -> entity_pb2.Entity
    """
    Same as "model_pb_to_entity_pb", but it assumes model_pb which is passed to this function also
    contains "key" string field which is used to construct a primary key for the Entity PB object.

    NOTE: Datastore client instance needs to be passed to this method so
    namespace and project can be inferred from it (namespace_id and project_id are used as part of
    a composite primary key).
    """
    entity_pb = model_pb_to_entity_pb(model_pb=model_pb, exclude_falsy_values=exclude_falsy_values)

    if getattr(model_pb, 'key', None) is not None:
        # Special handling for top level key attribute which we assume will service as a primary
        # key (if provided)
        # NOTE: We use model name as the value for "kind" part of the key. Aka if Protobuf
        # message name is "MyClassDBModel", kind will be set to "MyClassDBModel"
        model_name = model_pb.DESCRIPTOR.name

        key_str = model_pb.key  # type: ignore
        key_pb = client.key(model_name, key_str).to_protobuf()
        entity_pb.key.CopyFrom(key_pb)  # pylint: disable=no-member

    return entity_pb


def model_pb_to_entity_pb(model_pb, exclude_falsy_values=False):
    # type: (message.Message, bool) -> entity_pb2.Entity
    """
    Translate Protobuf based database model object to Entity object which can be used with Google
    Datastore client library.

    :param model_pb: Instance of a custom Protobuf object to translate.

    :param exclude_falsy_values: True to exclude field values which are falsy (e.g. None, False,
                                 '', 0, etc.) and match the default values.

                                 NOTE: Due to the design of protobuf v3, there is no way to
                                 distinguish between a user explicitly providing a value which is
                                 the same as a default value (e.g. 0 for an integer field) and
                                 user not providing a value and default value being used instead.
    """
    if not isinstance(model_pb, message.Message):
        raise ValueError('model_pb argument is not a valid Protobuf class instance')

    fields = list(iter(model_pb.DESCRIPTOR.fields))
    fields = [field for field in fields if field not in ['key']]

    entity_pb = entity_pb2.Entity()

    for field_descriptor in fields:
        field_type = field_descriptor.type
        field_name = field_descriptor.name
        field_value = getattr(model_pb, field_name, None)

        if field_value is None:
            # Value not set or it uses a default value, skip it
            # NOTE: proto3 syntax doesn't support HasField() anymore so there is now way for us to
            # determine if a value is set / provided so we just use and return default values.
            continue

        if exclude_falsy_values and not field_value:
            continue

        attr_type = get_pb_attr_type(field_value)

        if attr_type == 'array_value':
            if len(field_value) == 0:
                # TODO: Should we include empty value?
                # array_value = entity_pb2.ArrayValue(values=[])
                # value_pb.array_value.CopyFrom(array_value)
                continue
            else:
                value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)

                for value in field_value:
                    value_pb_item = entity_pb2.Value()
                    value_pb_item = set_value_pb_item_value(value_pb=value_pb_item, value=value)

                    value_pb.array_value.values.append(value_pb_item)
        elif field_type == descriptor.FieldDescriptor.TYPE_STRING:
            value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
            value_pb.string_value = field_value
        elif field_type in [descriptor.FieldDescriptor.TYPE_DOUBLE,
                descriptor.FieldDescriptor.TYPE_FLOAT]:
            # NOTE: Datastore only supports double type so we map float to double
            value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
            value_pb.double_value = field_value
        elif field_type in [descriptor.FieldDescriptor.TYPE_INT32,
                descriptor.FieldDescriptor.TYPE_INT64]:
            value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
            value_pb.integer_value = field_value
        elif field_type == descriptor.FieldDescriptor.TYPE_ENUM:
            value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)

            if field_descriptor.enum_type.name == 'NullValue':
                # NULL value
                value_pb.null_value = struct_pb2.NULL_VALUE
            else:
                # Regular ENUM
                value_pb.integer_value = field_value
        elif field_type == descriptor.FieldDescriptor.TYPE_BOOL:
            value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
            value_pb.boolean_value = field_value
        elif field_type == descriptor.FieldDescriptor.TYPE_BYTES:
            value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)

            if isinstance(field_value, six.string_types):
                field_value = field_value.encode('utf-8')

            value_pb.blob_value = field_value
        elif field_type == descriptor.FieldDescriptor.TYPE_MESSAGE:
            # Complex type, convert to entity
            field_type = model_pb.DESCRIPTOR.fields_by_name[field_name]

            if field_type.message_type.full_name == 'google.protobuf.Timestamp':
                if str(field_value) == '':
                    # Value not set
                    continue

                value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
                value_pb.timestamp_value.CopyFrom(field_value)
            elif isinstance(field_value, MessageMapContainer):
                # Nested dictionary on a struct, set a value directory on a passed in pb object
                # which is a parent Struct entity
                entity_pb_item = get_entity_pb_for_value(value=field_value)
                entity_pb.CopyFrom(entity_pb_item)
            elif isinstance(field_value, ScalarMapContainer):
                # Custom user defined type, recurse into it
                value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
                entity_pb_item = get_entity_pb_for_value(value=field_value)
                value_pb.entity_value.CopyFrom(entity_pb_item)
            elif field_type.message_type.full_name == 'google.protobuf.Struct':
                if not dict(field_value):
                    # Value not set, skip it
                    continue

                value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
                entity_pb_item = get_entity_pb_for_value(value=field_value)
                value_pb.entity_value.CopyFrom(entity_pb_item)
            else:
                # Nested type, potentially referenced from another Protobuf definition file
                value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
                entity_pb_item = model_pb_to_entity_pb(field_value)
                value_pb.entity_value.CopyFrom(entity_pb_item)
        else:
            raise ValueError('Unsupported field type for field "%s"' % (field_name))

    return entity_pb


def entity_pb_to_model_pb(model_pb_class,   # type: Type[T_model_pb]
                          entity_pb,        # type: entity_pb2.Entity
                          strict=False      # type: bool
                          ):
    # type: (...) -> T_model_pb
    """
    Translate Google Datastore Entity Protobuf object to Protobuf based database model object.

    :param model_pb_class: Protobuf class to convert the Entity object to.
    :param entity_pb: Entity Protobuf instance to convert to database model instance.
    :param strict: True to run in a strict mode and throw an exception if we encounter a field on
                   the database object which is not defined on the model definition.
    """
    model_pb_field_names = list(iter(model_pb_class.DESCRIPTOR.fields))
    model_pb_field_names = [field.name for field in model_pb_field_names if field not in ['key']]

    model_pb = model_pb_class()

    for prop_name, value_pb in datastore.helpers._property_tuples(entity_pb):
        value = datastore.helpers._get_value_from_value_pb(value_pb)

        # Field not defined on the model class
        if prop_name not in model_pb_field_names:
            if strict:
                msg = ('Database object contains field "%s" which is not defined on the database '
                       'model class "%s"' % (prop_name, model_pb.DESCRIPTOR.name))
                raise ValueError(msg)
            else:
                continue

        def set_model_pb_value(model_pb, prop_name, value, is_nested=False):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        # Handle nested models
                        if model_pb_class.DESCRIPTOR.fields_by_name[prop_name].message_type:
                            field = model_pb_class.DESCRIPTOR.fields_by_name[prop_name]

                            # Dynamically import nested model from a corresponding file
                            nested_model_name = field.message_type.name
                            nested_model_module = get_python_module_for_field(field=field)
                            nested_model_class = getattr(nested_model_module, nested_model_name)

                            # Instantiate an instance of nested field Protobuf class
                            item_pb = nested_model_class()
                            set_model_pb_value(item_pb, prop_name, item, is_nested=True)

                            getattr(model_pb, prop_name).append(item_pb)
                    else:
                        getattr(model_pb, prop_name).append(item)
            elif isinstance(value, dict):
                # We assume it's a referenced protobuf type if it doesn't contain "update()" method
                # google.protobuf.Struct and Map types contain "update()" methods so we can treat
                # them as simple dictionaries
                field = model_pb_class.DESCRIPTOR.fields_by_name[prop_name]
                is_nested_model_type = (bool(field.message_type) and
                                        not hasattr(getattr(model_pb, prop_name, {}), 'update'))

                if is_nested:
                    for key, value in six.iteritems(value):
                        set_model_pb_value(model_pb, key, value)
                elif is_nested_model_type:
                    # Custom type definition potentially defined in different file
                    field = model_pb_class.DESCRIPTOR.fields_by_name[prop_name]

                    # Dynamically import nested model from a corresponding file
                    nested_model_name = field.message_type.name
                    nested_model_module = get_python_module_for_field(field=field)
                    nested_model_class = getattr(nested_model_module, nested_model_name)

                    item_pb = nested_model_class()
                    set_model_pb_value(item_pb, prop_name, value, is_nested=True)

                    getattr(model_pb, prop_name).CopyFrom(item_pb)
                else:
                    getattr(model_pb, prop_name).update(dict(value))
            elif isinstance(value, datetime):
                getattr(model_pb, prop_name).FromDatetime(value)
            elif value is None:
                # NULL type
                setattr(model_pb, prop_name, 0)
            else:
                setattr(model_pb, prop_name, value)

        set_model_pb_value(model_pb, prop_name, value)

    return model_pb


def get_pb_attr_type(value):
    # type: (Any) -> str
    """
    Return protobuf attribute type for the provided Python or protobuf value.
    """
    if isinstance(value, timestamp_pb2.Timestamp):
        name = 'timestamp'
    elif isinstance(value, bool):
        name = 'boolean'
    elif isinstance(value, float):
        name = 'double'
    elif isinstance(value, six.integer_types):
        name = 'integer'
    elif isinstance(value, six.text_type):
        name = 'string'
    elif isinstance(value, six.binary_type):
        name = 'blob'
    elif isinstance(value, (dict, ScalarMapContainer, MessageMapContainer, struct_pb2.Struct,
                            message.Message)):
        name = 'dict'
    elif isinstance(value, (list, RepeatedScalarContainer, RepeatedCompositeContainer)):
        name = 'array'
    elif value is None:
        name = 'null'
    else:
        raise ValueError('Unknown protobuf attr type', type(value))

    return name + '_value'


def get_entity_pb_for_value(value):
    # type: (Any) -> entity_pb2.Entity
    """
    Return Entity protobuf object for the provided Python value.
    """
    entity_pb = entity_pb2.Entity()

    attr_type = get_pb_attr_type(value)

    if attr_type == 'dict_value':
        if six.PY2:
            value = dict(value)

        for key, value in six.iteritems(value):
            value_pb = datastore.helpers._new_value_pb(entity_pb, key)
            value_pb = set_value_pb_item_value(value_pb=value_pb, value=value)
    else:
        raise ValueError('Unsupported attribute type: %s' % (attr_type))

    return entity_pb


def set_value_pb_item_value(value_pb, value):
    # type: (entity_pb2.Value, Any) -> entity_pb2.Value
    """
    Set a value attribute on the Value object based on the type of the provided value.

    NOTE: For complex nested types (e.g. dicts and structs this function uses recursion).
    """
    if isinstance(value, struct_pb2.ListValue):
        # Cast special ListValue type to a list
        value = cast(Any, value)
        value = list(value)

    if isinstance(value, float) and value.is_integer():
        # Special case because of how Protobuf handles ints in some scenarios (e.g. Struct)
        value = cast(Any, value)
        value = int(value)

    if isinstance(value, six.text_type):
        value_pb.string_value = value
    elif isinstance(value, int):
        value_pb.integer_value = value
    elif isinstance(value, float):
        value_pb.double_value = value
    elif isinstance(value, six.binary_type):
        value_pb.blob_value = value
    elif isinstance(value, list):
        for value in value:
            value_pb_item = entity_pb2.Value()
            value_pb_item = set_value_pb_item_value(value_pb=value_pb_item, value=value)

            value_pb.array_value.values.append(value_pb_item)
    elif isinstance(value, struct_pb2.Value):
        item_value = _GetStructValue(value)
        set_value_pb_item_value(value_pb, item_value)
    elif hasattr(value, 'DESCRIPTOR'):
        # Custom user-defined type
        entity_pb_item = model_pb_to_entity_pb(value, exclude_falsy_values=True)
        value_pb.entity_value.CopyFrom(entity_pb_item)
    else:
        raise ValueError('Unsupported type for value: %s' % (value))

    return value_pb


def get_python_module_for_field(field):
    # type: (FieldDescriptor) -> ModuleType
    """
    Return Python module for the provided Protobuf field.

    NOTE: This function will also import the module if it's not already available in sys.path.
    """
    model_file = field.message_type.file.name
    module_name = model_file.replace('.proto', '_pb2').replace('/', '.')

    if module_name not in sys.modules:
        module = importlib.import_module(module_name)

    module = sys.modules[module_name]
    return module
