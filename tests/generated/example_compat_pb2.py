# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example_compat.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='example_compat.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x14\x65xample_compat.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"l\n\x18\x45xampleCompatNestedModel\x12\x12\n\nstring_key\x18\x01 \x01(\t\x12\x11\n\tint32_key\x18\x02 \x01(\x05\x12)\n\x08\x65num_key\x18\x03 \x01(\x0e\x32\x17.ExampleCompatEnumModel\"\xb9\x05\n\x14\x45xampleCompatDBModel\x12\x11\n\tint32_key\x18\x01 \x01(\x05\x12\x12\n\nstring_key\x18\x02 \x01(\t\x12\x10\n\x08\x62ool_key\x18\x03 \x01(\x08\x12\x11\n\tbytes_key\x18\x04 \x01(\x0c\x12\x12\n\ndouble_key\x18\x0e \x01(\x01\x12\x11\n\tfloat_key\x18\x0f \x01(\x02\x12\x11\n\tint64_key\x18\x10 \x01(\x03\x12\x45\n\x11map_string_string\x18\x05 \x03(\x0b\x32*.ExampleCompatDBModel.MapStringStringEntry\x12\x43\n\x10map_string_int32\x18\x06 \x03(\x0b\x32).ExampleCompatDBModel.MapStringInt32Entry\x12\x18\n\x10string_array_key\x18\x07 \x03(\t\x12\x17\n\x0fint32_array_key\x18\x08 \x03(\x05\x12\x34\n\x11\x63omplex_array_key\x18\t \x03(\x0b\x32\x19.ExampleCompatNestedModel\x12)\n\x08\x65num_key\x18\n \x01(\x0e\x32\x17.ExampleCompatEnumModel\x12\x31\n\rtimestamp_key\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\nstruct_key\x18\x0c \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x08null_key\x18\r \x01(\x0e\x32\x1a.google.protobuf.NullValue\x1a\x36\n\x14MapStringStringEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x35\n\x13MapStringInt32Entry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01*<\n\x16\x45xampleCompatEnumModel\x12\n\n\x06\x45NUM10\x10\x00\x12\n\n\x06\x45NUM11\x10\x01\x12\n\n\x06\x45NUM12\x10\x02\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])

_EXAMPLECOMPATENUMMODEL = _descriptor.EnumDescriptor(
  name='ExampleCompatEnumModel',
  full_name='ExampleCompatEnumModel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ENUM10', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENUM11', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENUM12', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=897,
  serialized_end=957,
)
_sym_db.RegisterEnumDescriptor(_EXAMPLECOMPATENUMMODEL)

ExampleCompatEnumModel = enum_type_wrapper.EnumTypeWrapper(_EXAMPLECOMPATENUMMODEL)
ENUM10 = 0
ENUM11 = 1
ENUM12 = 2



_EXAMPLECOMPATNESTEDMODEL = _descriptor.Descriptor(
  name='ExampleCompatNestedModel',
  full_name='ExampleCompatNestedModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='string_key', full_name='ExampleCompatNestedModel.string_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int32_key', full_name='ExampleCompatNestedModel.int32_key', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enum_key', full_name='ExampleCompatNestedModel.enum_key', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=87,
  serialized_end=195,
)


_EXAMPLECOMPATDBMODEL_MAPSTRINGSTRINGENTRY = _descriptor.Descriptor(
  name='MapStringStringEntry',
  full_name='ExampleCompatDBModel.MapStringStringEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ExampleCompatDBModel.MapStringStringEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ExampleCompatDBModel.MapStringStringEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=786,
  serialized_end=840,
)

_EXAMPLECOMPATDBMODEL_MAPSTRINGINT32ENTRY = _descriptor.Descriptor(
  name='MapStringInt32Entry',
  full_name='ExampleCompatDBModel.MapStringInt32Entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ExampleCompatDBModel.MapStringInt32Entry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ExampleCompatDBModel.MapStringInt32Entry.value', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=842,
  serialized_end=895,
)

_EXAMPLECOMPATDBMODEL = _descriptor.Descriptor(
  name='ExampleCompatDBModel',
  full_name='ExampleCompatDBModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='int32_key', full_name='ExampleCompatDBModel.int32_key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_key', full_name='ExampleCompatDBModel.string_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_key', full_name='ExampleCompatDBModel.bool_key', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bytes_key', full_name='ExampleCompatDBModel.bytes_key', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='double_key', full_name='ExampleCompatDBModel.double_key', index=4,
      number=14, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_key', full_name='ExampleCompatDBModel.float_key', index=5,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int64_key', full_name='ExampleCompatDBModel.int64_key', index=6,
      number=16, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='map_string_string', full_name='ExampleCompatDBModel.map_string_string', index=7,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='map_string_int32', full_name='ExampleCompatDBModel.map_string_int32', index=8,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_array_key', full_name='ExampleCompatDBModel.string_array_key', index=9,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int32_array_key', full_name='ExampleCompatDBModel.int32_array_key', index=10,
      number=8, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='complex_array_key', full_name='ExampleCompatDBModel.complex_array_key', index=11,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enum_key', full_name='ExampleCompatDBModel.enum_key', index=12,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_key', full_name='ExampleCompatDBModel.timestamp_key', index=13,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='struct_key', full_name='ExampleCompatDBModel.struct_key', index=14,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_key', full_name='ExampleCompatDBModel.null_key', index=15,
      number=13, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_EXAMPLECOMPATDBMODEL_MAPSTRINGSTRINGENTRY, _EXAMPLECOMPATDBMODEL_MAPSTRINGINT32ENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=198,
  serialized_end=895,
)

_EXAMPLECOMPATNESTEDMODEL.fields_by_name['enum_key'].enum_type = _EXAMPLECOMPATENUMMODEL
_EXAMPLECOMPATDBMODEL_MAPSTRINGSTRINGENTRY.containing_type = _EXAMPLECOMPATDBMODEL
_EXAMPLECOMPATDBMODEL_MAPSTRINGINT32ENTRY.containing_type = _EXAMPLECOMPATDBMODEL
_EXAMPLECOMPATDBMODEL.fields_by_name['map_string_string'].message_type = _EXAMPLECOMPATDBMODEL_MAPSTRINGSTRINGENTRY
_EXAMPLECOMPATDBMODEL.fields_by_name['map_string_int32'].message_type = _EXAMPLECOMPATDBMODEL_MAPSTRINGINT32ENTRY
_EXAMPLECOMPATDBMODEL.fields_by_name['complex_array_key'].message_type = _EXAMPLECOMPATNESTEDMODEL
_EXAMPLECOMPATDBMODEL.fields_by_name['enum_key'].enum_type = _EXAMPLECOMPATENUMMODEL
_EXAMPLECOMPATDBMODEL.fields_by_name['timestamp_key'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EXAMPLECOMPATDBMODEL.fields_by_name['struct_key'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_EXAMPLECOMPATDBMODEL.fields_by_name['null_key'].enum_type = google_dot_protobuf_dot_struct__pb2._NULLVALUE
DESCRIPTOR.message_types_by_name['ExampleCompatNestedModel'] = _EXAMPLECOMPATNESTEDMODEL
DESCRIPTOR.message_types_by_name['ExampleCompatDBModel'] = _EXAMPLECOMPATDBMODEL
DESCRIPTOR.enum_types_by_name['ExampleCompatEnumModel'] = _EXAMPLECOMPATENUMMODEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExampleCompatNestedModel = _reflection.GeneratedProtocolMessageType('ExampleCompatNestedModel', (_message.Message,), {
  'DESCRIPTOR' : _EXAMPLECOMPATNESTEDMODEL,
  '__module__' : 'example_compat_pb2'
  # @@protoc_insertion_point(class_scope:ExampleCompatNestedModel)
  })
_sym_db.RegisterMessage(ExampleCompatNestedModel)

ExampleCompatDBModel = _reflection.GeneratedProtocolMessageType('ExampleCompatDBModel', (_message.Message,), {

  'MapStringStringEntry' : _reflection.GeneratedProtocolMessageType('MapStringStringEntry', (_message.Message,), {
    'DESCRIPTOR' : _EXAMPLECOMPATDBMODEL_MAPSTRINGSTRINGENTRY,
    '__module__' : 'example_compat_pb2'
    # @@protoc_insertion_point(class_scope:ExampleCompatDBModel.MapStringStringEntry)
    })
  ,

  'MapStringInt32Entry' : _reflection.GeneratedProtocolMessageType('MapStringInt32Entry', (_message.Message,), {
    'DESCRIPTOR' : _EXAMPLECOMPATDBMODEL_MAPSTRINGINT32ENTRY,
    '__module__' : 'example_compat_pb2'
    # @@protoc_insertion_point(class_scope:ExampleCompatDBModel.MapStringInt32Entry)
    })
  ,
  'DESCRIPTOR' : _EXAMPLECOMPATDBMODEL,
  '__module__' : 'example_compat_pb2'
  # @@protoc_insertion_point(class_scope:ExampleCompatDBModel)
  })
_sym_db.RegisterMessage(ExampleCompatDBModel)
_sym_db.RegisterMessage(ExampleCompatDBModel.MapStringStringEntry)
_sym_db.RegisterMessage(ExampleCompatDBModel.MapStringInt32Entry)


_EXAMPLECOMPATDBMODEL_MAPSTRINGSTRINGENTRY._options = None
_EXAMPLECOMPATDBMODEL_MAPSTRINGINT32ENTRY._options = None
# @@protoc_insertion_point(module_scope)
