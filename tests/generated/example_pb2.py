# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example.proto

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
  name='example.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rexample.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\";\n\x12\x45xampleNestedModel\x12\x12\n\nstring_key\x18\x01 \x01(\t\x12\x11\n\tint32_key\x18\x02 \x01(\x05\"K\n\x15\x45xampleDBModelWithKey\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x12\n\nstring_key\x18\x02 \x01(\t\x12\x11\n\tint32_key\x18\x03 \x01(\x05\"\x9b\x05\n\x0e\x45xampleDBModel\x12\x11\n\tint32_key\x18\x01 \x01(\x05\x12\x12\n\nstring_key\x18\x02 \x01(\t\x12\x10\n\x08\x62ool_key\x18\x03 \x01(\x08\x12\x11\n\tbytes_key\x18\x04 \x01(\x0c\x12\x12\n\ndouble_key\x18\x0e \x01(\x01\x12\x11\n\tfloat_key\x18\x0f \x01(\x02\x12\x11\n\tint64_key\x18\x10 \x01(\x03\x12?\n\x11map_string_string\x18\x05 \x03(\x0b\x32$.ExampleDBModel.MapStringStringEntry\x12=\n\x10map_string_int32\x18\x06 \x03(\x0b\x32#.ExampleDBModel.MapStringInt32Entry\x12\x18\n\x10string_array_key\x18\x07 \x03(\t\x12\x17\n\x0fint32_array_key\x18\x08 \x03(\x05\x12.\n\x11\x63omplex_array_key\x18\t \x03(\x0b\x32\x13.ExampleNestedModel\x12#\n\x08\x65num_key\x18\n \x01(\x0e\x32\x11.ExampleEnumModel\x12\x31\n\rtimestamp_key\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12+\n\nstruct_key\x18\x0c \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x08null_key\x18\r \x01(\x0e\x32\x1a.google.protobuf.NullValue\x1a\x36\n\x14MapStringStringEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x35\n\x13MapStringInt32Entry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01*3\n\x10\x45xampleEnumModel\x12\t\n\x05\x45NUM0\x10\x00\x12\t\n\x05\x45NUM1\x10\x01\x12\t\n\x05\x45NUM2\x10\x02\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])

_EXAMPLEENUMMODEL = _descriptor.EnumDescriptor(
  name='ExampleEnumModel',
  full_name='ExampleEnumModel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ENUM0', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENUM1', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENUM2', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=888,
  serialized_end=939,
)
_sym_db.RegisterEnumDescriptor(_EXAMPLEENUMMODEL)

ExampleEnumModel = enum_type_wrapper.EnumTypeWrapper(_EXAMPLEENUMMODEL)
ENUM0 = 0
ENUM1 = 1
ENUM2 = 2



_EXAMPLENESTEDMODEL = _descriptor.Descriptor(
  name='ExampleNestedModel',
  full_name='ExampleNestedModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='string_key', full_name='ExampleNestedModel.string_key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int32_key', full_name='ExampleNestedModel.int32_key', index=1,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=139,
)


_EXAMPLEDBMODELWITHKEY = _descriptor.Descriptor(
  name='ExampleDBModelWithKey',
  full_name='ExampleDBModelWithKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ExampleDBModelWithKey.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_key', full_name='ExampleDBModelWithKey.string_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int32_key', full_name='ExampleDBModelWithKey.int32_key', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=141,
  serialized_end=216,
)


_EXAMPLEDBMODEL_MAPSTRINGSTRINGENTRY = _descriptor.Descriptor(
  name='MapStringStringEntry',
  full_name='ExampleDBModel.MapStringStringEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ExampleDBModel.MapStringStringEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ExampleDBModel.MapStringStringEntry.value', index=1,
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
  serialized_start=777,
  serialized_end=831,
)

_EXAMPLEDBMODEL_MAPSTRINGINT32ENTRY = _descriptor.Descriptor(
  name='MapStringInt32Entry',
  full_name='ExampleDBModel.MapStringInt32Entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ExampleDBModel.MapStringInt32Entry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ExampleDBModel.MapStringInt32Entry.value', index=1,
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
  serialized_start=833,
  serialized_end=886,
)

_EXAMPLEDBMODEL = _descriptor.Descriptor(
  name='ExampleDBModel',
  full_name='ExampleDBModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='int32_key', full_name='ExampleDBModel.int32_key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_key', full_name='ExampleDBModel.string_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bool_key', full_name='ExampleDBModel.bool_key', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bytes_key', full_name='ExampleDBModel.bytes_key', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='double_key', full_name='ExampleDBModel.double_key', index=4,
      number=14, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_key', full_name='ExampleDBModel.float_key', index=5,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int64_key', full_name='ExampleDBModel.int64_key', index=6,
      number=16, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='map_string_string', full_name='ExampleDBModel.map_string_string', index=7,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='map_string_int32', full_name='ExampleDBModel.map_string_int32', index=8,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='string_array_key', full_name='ExampleDBModel.string_array_key', index=9,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int32_array_key', full_name='ExampleDBModel.int32_array_key', index=10,
      number=8, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='complex_array_key', full_name='ExampleDBModel.complex_array_key', index=11,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enum_key', full_name='ExampleDBModel.enum_key', index=12,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_key', full_name='ExampleDBModel.timestamp_key', index=13,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='struct_key', full_name='ExampleDBModel.struct_key', index=14,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='null_key', full_name='ExampleDBModel.null_key', index=15,
      number=13, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_EXAMPLEDBMODEL_MAPSTRINGSTRINGENTRY, _EXAMPLEDBMODEL_MAPSTRINGINT32ENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=219,
  serialized_end=886,
)

_EXAMPLEDBMODEL_MAPSTRINGSTRINGENTRY.containing_type = _EXAMPLEDBMODEL
_EXAMPLEDBMODEL_MAPSTRINGINT32ENTRY.containing_type = _EXAMPLEDBMODEL
_EXAMPLEDBMODEL.fields_by_name['map_string_string'].message_type = _EXAMPLEDBMODEL_MAPSTRINGSTRINGENTRY
_EXAMPLEDBMODEL.fields_by_name['map_string_int32'].message_type = _EXAMPLEDBMODEL_MAPSTRINGINT32ENTRY
_EXAMPLEDBMODEL.fields_by_name['complex_array_key'].message_type = _EXAMPLENESTEDMODEL
_EXAMPLEDBMODEL.fields_by_name['enum_key'].enum_type = _EXAMPLEENUMMODEL
_EXAMPLEDBMODEL.fields_by_name['timestamp_key'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EXAMPLEDBMODEL.fields_by_name['struct_key'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_EXAMPLEDBMODEL.fields_by_name['null_key'].enum_type = google_dot_protobuf_dot_struct__pb2._NULLVALUE
DESCRIPTOR.message_types_by_name['ExampleNestedModel'] = _EXAMPLENESTEDMODEL
DESCRIPTOR.message_types_by_name['ExampleDBModelWithKey'] = _EXAMPLEDBMODELWITHKEY
DESCRIPTOR.message_types_by_name['ExampleDBModel'] = _EXAMPLEDBMODEL
DESCRIPTOR.enum_types_by_name['ExampleEnumModel'] = _EXAMPLEENUMMODEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExampleNestedModel = _reflection.GeneratedProtocolMessageType('ExampleNestedModel', (_message.Message,), {
  'DESCRIPTOR' : _EXAMPLENESTEDMODEL,
  '__module__' : 'example_pb2'
  # @@protoc_insertion_point(class_scope:ExampleNestedModel)
  })
_sym_db.RegisterMessage(ExampleNestedModel)

ExampleDBModelWithKey = _reflection.GeneratedProtocolMessageType('ExampleDBModelWithKey', (_message.Message,), {
  'DESCRIPTOR' : _EXAMPLEDBMODELWITHKEY,
  '__module__' : 'example_pb2'
  # @@protoc_insertion_point(class_scope:ExampleDBModelWithKey)
  })
_sym_db.RegisterMessage(ExampleDBModelWithKey)

ExampleDBModel = _reflection.GeneratedProtocolMessageType('ExampleDBModel', (_message.Message,), {

  'MapStringStringEntry' : _reflection.GeneratedProtocolMessageType('MapStringStringEntry', (_message.Message,), {
    'DESCRIPTOR' : _EXAMPLEDBMODEL_MAPSTRINGSTRINGENTRY,
    '__module__' : 'example_pb2'
    # @@protoc_insertion_point(class_scope:ExampleDBModel.MapStringStringEntry)
    })
  ,

  'MapStringInt32Entry' : _reflection.GeneratedProtocolMessageType('MapStringInt32Entry', (_message.Message,), {
    'DESCRIPTOR' : _EXAMPLEDBMODEL_MAPSTRINGINT32ENTRY,
    '__module__' : 'example_pb2'
    # @@protoc_insertion_point(class_scope:ExampleDBModel.MapStringInt32Entry)
    })
  ,
  'DESCRIPTOR' : _EXAMPLEDBMODEL,
  '__module__' : 'example_pb2'
  # @@protoc_insertion_point(class_scope:ExampleDBModel)
  })
_sym_db.RegisterMessage(ExampleDBModel)
_sym_db.RegisterMessage(ExampleDBModel.MapStringStringEntry)
_sym_db.RegisterMessage(ExampleDBModel.MapStringInt32Entry)


_EXAMPLEDBMODEL_MAPSTRINGSTRINGENTRY._options = None
_EXAMPLEDBMODEL_MAPSTRINGINT32ENTRY._options = None
# @@protoc_insertion_point(module_scope)
