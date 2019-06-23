# Licensed to the Tomaz Muraus under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

import six

from google.cloud.datastore_v1.proto import entity_pb2
from google.cloud import datastore
from google.protobuf import timestamp_pb2
from google.protobuf import struct_pb2
from google.protobuf import descriptor

from google.protobuf.pyext._message import ScalarMapContainer
from google.protobuf.pyext._message import RepeatedScalarContainer
from google.protobuf.pyext._message import RepeatedCompositeContainer

__all__ = [
    'model_pb_to_entity_pb',
    'entity_pb_to_model_pb'
]


def model_pb_to_entity_pb(model_pb, is_top_level=True):
    # type: ( ) -> entity_pb2.Entity
    """
    Translate protobuf based database model object to Entity object which can be used with Google
    Datastore client library.
    """

    if is_top_level and getattr(model_pb, 'key', None) is not None:
        # Special handling for top level key attribute which we assume will service as a primary
        # key (if provided)
        # TODO
        # key_str = model_pb.key
        # key_pb = client.key('EntityKind', key_str).to_protobuf()
        # entity_pb.key.CopyFrom(key_pb)
        pass

    fields = list(iter(model_pb.DESCRIPTOR.fields))
    fields = [field for field in fields if field not in ['key']]

    entity_pb = entity_pb2.Entity()

    for field_descriptor in fields:
        field_type = field_descriptor.type
        field_name = field_descriptor.name
        field_value = getattr(model_pb, field_name, None)

        if field_value is None:
            # Value not set, skip it
            continue

        attr_type = get_pb_attr_type(field_value)

        if attr_type == 'array_value':
            if len(field_value) == 0:
                continue
                # TODO: Should we include empty value?
                # array_value = entity_pb2.ArrayValue(values=[])
                # value_pb.array_value.CopyFrom(array_value)
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
            if field_value == float(0):
                # Value not provided, skip it
                continue

            # NOTE: Datastore only supports double type so we map float to double
            value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
            value_pb.double_value = field_value
        elif field_type in [descriptor.FieldDescriptor.TYPE_INT32,
                descriptor.FieldDescriptor.TYPE_INT64]:
            if field_value == 0:
                # Value not provided, skip it
                continue

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
                value_pb = datastore.helpers._new_value_pb(entity_pb, field_name)
                value_pb.timestamp_value.CopyFrom(field_value)
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
                entity_pb_item = get_entity_pb_for_value(value=dict(field_value))
                value_pb.entity_value.CopyFrom(entity_pb_item)
        else:
            raise ValueError('Unsupported field type for field "%s"' % (field_name))

    return entity_pb


def entity_pb_to_model_pb():
    """
    Translate Entity protobuf object to protobuf based database model object.
    """
    # TODO
    pass


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
    elif isinstance(value, (dict, ScalarMapContainer, struct_pb2.Struct)):
        name = 'dict'
    elif isinstance(value, (list, RepeatedScalarContainer, RepeatedCompositeContainer)):
        name = 'array'
    elif value is None:
        name = 'null'
    else:
        raise ValueError('Unknown protobuf attr type', type(value))

    return name + '_value'


def get_entity_pb_for_value(value):
    """
    Return Entity protobuf object for the provided Python value.
    """
    entity_pb = entity_pb2.Entity()

    attr_type = get_pb_attr_type(value)

    if attr_type == 'dict_value':
        for key, value in six.iteritems(value):
            value_pb = datastore.helpers._new_value_pb(entity_pb, key)
            value_pb = set_value_pb_item_value(value_pb=value_pb, value=value)
    else:
        raise ValueError('Unsupported attribute type: %s' % (attr_type))

    return entity_pb


def set_value_pb_item_value(value_pb, value):
    """
    Set a value attribute on the Value object based on the type of the provided value.

    NOTE: For complex nested types (e.g. dicts and structs this function uses recursion).
    """
    if isinstance(value, struct_pb2.ListValue):
        # Cast special ListValue type to a list
        value = list(value)

    if isinstance(value, float) and value.is_integer():
        # Special case because of how Protobuf handles ints in some scenarios (e.g. Struct)
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
    elif hasattr(value, 'DESCRIPTOR'):
        # Custom user-defined type
        entity_pb_item = model_pb_to_entity_pb(value)
        value_pb.entity_value.CopyFrom(entity_pb_item)
    else:
        raise ValueError('Unsupported type for value: %s' % (value))

    return value_pb
