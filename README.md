# Protobuf Message to Google Datastore Entity Protobuf Message Translator

[![Tests Build Status](https://travis-ci.org/Kami/python-protobuf-cloud-datastore-entity-translator.svg?branch=master)](https://travis-ci.org/Kami/python-protobuf-cloud-datastore-entity-translator) [![Codecov](https://codecov.io/github/Kami/python-protobuf-cloud-datastore-entity-translator/badge.svg?branch=master&service=github)](https://codecov.io/github/Kami/python-protobuf-cloud-datastore-entity-translator?branch=master) [![](https://img.shields.io/pypi/v/protobuf-cloud-datastore-translator.svg)](https://pypi.org/project/protobuf-cloud-datastore-translator/)  [![](https://img.shields.io/pypi/pyversions/protobuf-cloud-datastore-translator.svg)](https://pypi.org/project/protobuf-cloud-datastore-translator/) [![](https://img.shields.io/github/license/Kami/python-protobuf-cloud-datastore-entity-translator.svg)](https://github.com/Kami/python-protobuf-cloud-datastore-entity-translator/blob/master/LICENSE)

This library allows you to store arbitrary Protobuf message objects inside the Google Datastore.

It exposes methods for translating arbitrary Protobuf message objects to Entity Protobuf objects
which are used by Google Datastore and vice-versa.

It supports all the native which are supported by the Google Datastore.

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
  ``google.protobuf.Struct``, ``google.types.LatLng``)
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

## Supported Python versions

* Python 2.7
* Python 3.6
* Python 3.7

It may also work with Python 3.4 and 3.5, but we don't test against those versions.

## Usage

This library exposes three main public methods.

### ``model_pb_to_entity_pb(model_pb, exclude_falsy_values=False, exclude_from_index=None)``

This method converts arbitrary Protobuf message objects to the Entity Protobuf object which can
be used with Google Datastore.

For example:

```python
from google.cloud import datastore
from google.protobuf.timestamp_pb2 import Timestamp

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb

from generated.protobuf.models import my_model_pb2

# 1. Store your database model object which is represented using a custom Protobuf message class
# instance inside Google Datastore

# Create database model Protobuf instance
model_pb = my_model_pb2.MyModelDB()
# Other entity attributes
model_pb.key1 = 'value1'
model_pb.key2 = 200
model_pb.parameters['foo'] = 'bar'
model_pb.parameters['bar'] = 'baz'

start_time_timestamp = Timestamp()
start_time_timestamp.GetCurrentTime()

model_pb.start_time = start_time_timestamp

# Convert it to Entity Protobuf object which can be used with Google Datastore
entity_pb = model_pb_to_entity_pb(model_pb)

# Store it in the datastore
client = Client(...)
key = self.client.key('MyModelDB', 'some_primary_key')
entity_pb_translated.key.CopyFrom(key.to_protobuf())
entity = datastore.helpers.entity_from_protobuf(entity_pb)
client.put(entity)
```

### ``model_pb_with_key_to_entity_pb(client, model_pb, exclude_falsy_values=False, exclude_from_index=None)``

As a convenience, this library also exposes ``model_pb_to_entity_pb`` method. This method assumes
there is a special ``key`` string field on your Protobuf message which will act as an Entity
primary key.

Underneath, this method infers ``project_id`` and ``namespace_id`` parts of the Entity composite
primary key from the ``client`` object which is passed to this method. Entity ``kind`` is inferred
from the Protobuf message model name. For example, if the Protobuf message model name is
``UserInfoDB``, entity kind would be set to ``UserInfoDB``.

For example:

```python
from google.cloud import datastore

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb

model_pb = my_model_pb2.MyModelDB()
model_pb.key = 'key-1234'
# set model fields
# ...

client = Client(project='my-project', namespace='my-namespace')

entity_pb = model_pb_to_entity_pb(model_pb)

# Store it in the datastore
entity = datastore.helpers.entity_from_protobuf(entity_pb)
client.put(entity)

# In this scenario, actual key would look the same if you manually constructed it like this:
key = client.key('MyModelDB', 'key-1234', project='my-project', namespace='my-namespace')
```

### ``entity_pb_to_model_pb(model_pb_class, entity_pb, strict=False)``

This method converts raw Entity Protobuf object as returned by the Google Datastore to provided
Protobuf message class.

By default, fields which are found on the Datastore Entity Protobuf object, but not on the
Protobuf message class are ignored. If you want an exception to be thrown in such scenario, you
can pass ``strict=True`` argument to the method.

For example:

```python
key = client.key('MyModelDB', 'some_primary_key')
entity = client.get(key)
entity_pb = datastore.helpers.entity_to_protobuf(entity)

model_pb = entity_pb_to_model_pb(my_model_pb2.MyModelPB, entity_pb)
print(model_pb)
```

## Excluding Protobuf Model Fields from Indexes

By default, Google Cloud Datstore automatically indexes each entity (model) property.

Indexing each field (entity property) is usually not desired nor needed. It also has some
limitations (for example, size of a simple field which is to be indexed is limited to ``1500``
bytes, etc.). In addition to that, uncessary indexing causes increased storage space consumption.

This library allows you to define which model fields to exclude from index on the field basis
utilizing Protobuf field options extension.

For example:

```protobuf
syntax = "proto3";

import "google/protobuf/descriptor.proto";

// Custom Protobuf option which specifies which model fields should be excluded
// from index
// NOTE: Keep in mind that it's important not to change the option name
// ("exclude_from_index") since this library uses that special option name to
// determine if a field should be excluded from index.
extend google.protobuf.FieldOptions {
    bool exclude_from_index = 50000;
}

message ExampleDBModelWithOptions1 {
    string string_key_one = 1 [(exclude_from_index) = true];
    string string_key_two = 2;
    string string_key_three = 3 [(exclude_from_index) = true];
    string string_key_four = 4;
    int32 int32_field_one = 5;
    int32 int32_field_two = 6 [(exclude_from_index) = true];
}
```

In this example, fields ``string_key_one``, ``string_key_three`` and ``int32_field_two`` won't be
indexed (https://cloud.google.com/datastore/docs/concepts/indexes#unindexed_properties).

In this example, field option extension is defined in the same file where model is defined, but in
reality you will likely define that extension inside a custom protobuf file (e.g
``field_options.proto``) and include that file inside other files which contain your database model
definitions.

Keep in mind that if you define option extension inside a package, that package needs to match the
package under which the models are stored.

For example:

1. ``protobuf/models/field_options.proto``:

```protobuf
syntax = "proto3";

package models;

import "google/protobuf/descriptor.proto";

// Custom Protobuf option which specifies which model fields should be excluded
// from index
// NOTE: Keep in mind that it's important not to change the option name
// ("exclude_from_index") since this library uses that special option name to
// determine if a field should be excluded from index.
extend google.protobuf.FieldOptions {
    bool exclude_from_index = 50000;
}
```

2. ``protobuf/models/my_model.proto``:

```protobuf
syntax = "proto3";

package models;

import "models/field_options.proto";

message ExampleDBModelWithOptions1 {
    string string_key_one = 1 [(exclude_from_index) = true];
    string string_key_two = 2;
    string string_key_three = 3 [(exclude_from_index) = true];
    string string_key_four = 4;
    int32 int32_field_one = 5;
    int32 int32_field_two = 6 [(exclude_from_index) = true];
}
```

## Examples

For example Protobuf message definitions, see ``protobuf/`` directory.

Example usage:

```python
from google.cloud import datastore

from protobuf_cloud_datastore_translator import model_pb_to_entity_pb
from protobuf_cloud_datastore_translator import entity_pb_to_model_pb

from generated.protobuf.models import my_model_pb2

# 1. Store your database model object which is represented using a custom Protobuf message class
# instance inside Google Datastore

# Create database model Protobuf instance
model_pb = my_model_pb2.MyModelDB()
model_pb.key1 = 'value1'
model_pb.key2 = 200

# Convert it to Entity Protobuf object which can be used with Google Datastore
entity_pb = model_pb_to_entity_pb(model_pb)

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

model_pb = entity_pb_to_model_pb(my_model_pb2.MyModelPB, entity_pb)
print(model_pb)
```


## Gotchas

### Default values

In Protobuf syntax version 3 a concept of field being set has been removed and combined with a
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

entity_pb_translated = model_pb_to_entity_pb(example_pb)
print(entity_pb_translated)

# No field values are provided, implicit default values are used during serialization
example_pb = example_pb2.ExampleDBModel()
entity_pb_translated = model_pb_to_entity_pb(example_pb)
print(entity_pb_translated)
```

If you don't want default values to be set on the translated Entity Protobuf objects and stored
inside the datastore, you can pass ``exclude_falsy_values=True`` argument to the
``model_pb_to_entity_pb`` method.

For details, see:

* https://developers.google.com/protocol-buffers/docs/reference/python-generated
* https://github.com/protocolbuffers/protobuf/issues/1606
* https://github.com/googleapis/google-cloud-python/issues/1402
* https://github.com/googleapis/google-cloud-python/pull/1450
* https://github.com/googleapis/google-cloud-python/pull/1329

### Struct Field type

This library supports ``google.protobuf.Struct`` field type out of the box. Struct field values
are serialized as an embedded entity.

Keep in mind that ``google.protobuf.Struct`` field type mimics JSON type which only supports
``number`` type for numeric values (https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/struct.proto#L62).
This means all the numbers (including integers) are represented as double precision floating
point values (internally on the Entity, that's stored as ``value_pb.double_value``).

## Translator Libraries for Other Programming Languages

This section contains a list of translator libraries for other programming languages which offer
the same functionality.

* Golang - [go-protobuf-cloud-datastore-entity-translator](https://github.com/Sheshagiri/go-protobuf-cloud-datastore-entity-translator)

## Tests

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

NOTE 1: Integration tests depend on the Google Cloud Datastore Emulator to be running
(``./scripts/run-datastore-emulator.sh``).

NOTE 2: Integration tests also run cross programming language compatibility tests which
verify that the Python and Go translator libraries produce exactly the same output. As such,
those tests also require Golang >= 1.12 to be installed on the system.

## License

Copyright 2019 Tomaz Muraus

Copyright 2019 Extreme Networks, Inc

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except
in compliance with the License. You may obtain a copy of the License in the [LICENSE](LICENSE) file,
or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by your employer) and
you grant a full, complete, irrevocable copyright license to all users and developers of the
project, present and future, pursuant to the license of the project.
