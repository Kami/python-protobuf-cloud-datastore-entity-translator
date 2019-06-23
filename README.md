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

## Gotchas

In protobuf syntax version 3 a concept of field being set has been removed and combined with a
concept of a default value. This means that even when a field is not set, a default value which
is specific to that field type will be returned.

As far as this library is concerned, this means when you are converting / translating Protobuf
object with no values set, translated object will still contain default values for fields which
are not set.

For details, see:

* https://developers.google.com/protocol-buffers/docs/reference/python-generated
* https://github.com/protocolbuffers/protobuf/issues/1606
* https://github.com/googleapis/google-cloud-python/issues/1402
* https://github.com/googleapis/google-cloud-python/pull/1450
* https://github.com/googleapis/google-cloud-python/pull/1329

## Examples

For example protobuf definitions, see ``protobuf/`` directory.

TBW.

## License

Copyright Tomaz Muraus

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except
in compliance with the License. You may obtain a copy of the License in the [LICENSE](LICENSE) file,
or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by your employer) and
you grant a full, complete, irrevocable copyright license to all users and developers of the
project, present and future, pursuant to the license of the project.
