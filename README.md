# Protobuf Message to Google Datastore Entity Protobuf Message Translator

[![Tests Build Status](https://travis-ci.org/Kami/python-protobuf-cloud-datastore-entity-translator.svg?branch=master)](https://travis-ci.org/Kami/python-protobuf-cloud-datastore-entity-translator) [![Codecov](https://codecov.io/github/Kami/python-protobuf-cloud-datastore-entity-translator/badge.svg?branch=master&service=github)](https://codecov.io/github/Kami/python-protobuf-cloud-datastore-entity-translator?branch=master)

This repository contains a Python library which converts arbitrary protobuf message objects into
Entity protobuf objects which can be used with Google Datastore.

## Why, Motivation

If you are working with Google Datastore from a single programming language you can utilize
one of the multiple Datastore ORMs for that programming language. Those ORMs allow you to define
schema for your database models and work with them using native programming language types.

This approach brakes down when you want to work with the same set of datastore entities from
multiple programming language.

There are multiple solutions for that problem, but one approach is to define some kind of model
schema which is programming language agnostic.

And this library tries to do just that. It utilizes native protobuf message definitions as a schema
for database models. This way those definitions can be shared by multiple programming language and
each language just needs a light translator library (like this one) which knows how to translate
arbitrary Protobuf object into Entity Protobuf object and vice-versa.

## Features

Right now the library supports the following Protobuf field types and functionality:

* All the simple types (string, int32, int64, double, float, bytes, bool, enum)
* Scalar / container types (map, repeated)
* Complex types from Protobuf standard library (``google.protobuf.Timestamp``,
  ``google.Protobuf.Struct``)
* Using imports and referencing types from different Protobuf definition files. For example,
  you can have Protobuf message definition called ``Model1DB`` inside file ``model1.proto`` which
  has a field which references ``Model2DB`` from ``model2.proto`` file.

  For that to work, you need to make sure that the root directory which contains all the generated
  Protobuf Python files is available in ``PYTHONPATH``.

  For example, if generated files are written to ``my_app/generated/``, ``my_app/generated/`` needs
  to be in ``PYTHONPATH`` and this directory needs to be a Python package (it needs to contain
  ``__init__.py`` file).

For more information on the actual types supported by Google Datastore, refer to
https://cloud.google.com/datastore/docs/concepts/entities#properties_and_value_types.

## Supported Python versions:

* Python 2.7
* Python 3.6
* Python 3.7

It may also work with Python 3.4 and 3.5, but we don't test against those versions.

## Gotchas

In protobuf syntax version 3 a concept of field being set has been removed and combined with a
concept of a default value. This means that even when a field is not set, a default value which
is specific to that field type will be returned.

As far as this library is concerned, this means when you are converting / translating Protobuf
object with no values set, translated object will still contain default values for fields which
are not set.

For example, the output / end result of both those two calls will be the same:

```python
# Field values are explicitly provided, but they match default values
example_pb = example_pb2.ExampleDBModel()
example_pb.bool_key = False
example_pb.string_key = ''
example_pb.int32_key = 0
example_pb.int64_key = 0
example_pb.double_key = 0.0
example_pb.float_key = 0.0
example_pb.enum_key = example_pb2.ExampleEnumModel.ENUM0
example_pb.bool_key = False
example_pb.bytes_key = b''
example_pb.null_key = 1

entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)
print(entity_pb_translated)

# No field values are provided, implicit default values are used during serialization
example_pb = example_pb2.ExampleDBModel()
entity_pb_translated = model_pb_to_entity_pb(model_pb=example_pb)
print(entity_pb_translated)
```

For details, see:

* https://developers.google.com/protocol-buffers/docs/reference/python-generated
* https://github.com/protocolbuffers/protobuf/issues/1606
* https://github.com/googleapis/google-cloud-python/issues/1402
* https://github.com/googleapis/google-cloud-python/pull/1450
* https://github.com/googleapis/google-cloud-python/pull/1329

## Examples

For example protobuf definitions, see ``protobuf/`` directory.

Example usage:

```python
from google.cloud import datastore

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb

from generated import my_model_pb2

# 1. Store your database model object which is represented using a custom Protobuf message class
# instance inside Google Datastore

# Create database model Protobuf instance
my_model_pb = MyModelDB()
# NOTE: "key" is a special attribute which is used as entity primary key
my_model_pb.key = 'some_primary_key'
# Other entity attributes
my_model_pb.key1 = 'value1'
my_model_pb.key2 = 200
my_model_pb['foo'] = 'bar'
my_model_pb['bar'] = 'baz'

# Convert it to Entity Protobuf object which can be used with Google Datastore
entity_pb = model_pb_to_entity_pb(my_model_pb)

# Store it in the datastore
# To avoid conversion back and forth you can also use lower level client methods which
# work directly with the Entity Protobuf objects
# For information on the low level client usage, see
# https://github.com/GoogleCloudPlatform/google-cloud-datastore/blob/master/python/demos/trivial/adams.py#L66
client = Client(...)
key = self.client.key('MyModelDB', 'some_primary_key')
entity_pb_translated.key.CopyFrom(key.to_protobuf())

entity = datastore.helpers.entity_from_protobuf(entity_pb)

client.put(entity)

# 2. Retrieve entity from the datastore and convert it to your Protobuf DB model instance class
# Same here - you can also use low level client to retrieve Entity protobuf object directly and
# avoid unnecessary conversion round trip
key = client.key('MyModelDB', 'some_primary_key')
entity = client.get(key)
entity_pb = datastore.helpers.entity_to_protobuf(entity)

my_model_pb = entity_pb_to_model_pb(my_model_pb2, my_model_pb2.MyModelPB, entity_pb)
print(my_model_pb)
```

### Tests

Unit and integration tests can be found inside ``tests/`` directory.

You can run unit and integration tests and other lint checks by using tox.

```bash
# Run all tox targets
tox

# Run only lint checks
tox -e lint

# Run unit tests under Python 2.7
tox -e py2.7-unit-tests

# Run Integration tests under Python 3.7
tox -e py3.7-integration-tests

# Run unit and integration tests and generate and display code coverage report
tox -e coverage
```

## License

Copyright 2019 Tomaz Muraus

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except
in compliance with the License. You may obtain a copy of the License in the [LICENSE](LICENSE) file,
or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by your employer) and
you grant a full, complete, irrevocable copyright license to all users and developers of the
project, present and future, pursuant to the license of the project.
