# v0.1.10 - September 4th, 2019

* Fix ``entity_pb_to_model_pb`` to correctly handle repeated Struct field types
  (aka array of Structs). #21 #20

# v0.1.9 - August 29th, 2019

- Internal code optimizations and add new
  ``utils.get_exclude_from_index_fields_for_model`` utility method. #19

# v0.1.8 - August 28th, 2019

- Fix ``exclude_from_index`` Protobuf field option functionality so it works
  correctly when field option extension is defined inside a Protobuf file which
  is part of a package.

  NOTE: In such scenario, definitions for other Protobuf datastore models need
  to be part of the same package. #18

# v0.1.7 - August 27th, 2019

- Add support for declaring which model fields are to be excluded from the
  index by specifying a custom ``exclude_from_index`` field option directly
  on the Protobuf message model field.

  For more information and example usage, please refer to the README. #17

# v0.1.6 - August 21th, 2019

- Fix a bug with ``model_pb_to_entity_pb`` method not correctly handling
  ``null`` values for nested ``google.protobuf.Struct`` fields. #16

# v0.1.5 - August 16th, 2019

- Add support for new ``exclude_from_index`` argument to the
  ``model_pb_to_entity_pb`` and ``model_pb_with_key_to_entity_pb`` method.
  With this argument, user can specify a list of model / entity fields which
  won't be indexed. #15

# v0.1.4 - July 29th, 2019

- Fix dynamic module import handling for referenced messages inside
  ``entity_pb_to_model_pb`` and make sure we don't try to import a
  module again if it's already imported under a different name (aka alias). #14
- Fix ``entity_pb_to_model_pb`` so it correctly handles messages with a custom
  referenced type which contains a struct field. #14

# v0.1.3 - July 28th, 2019

- Update ``model_pb_to_entity_pb`` method so it always explicitly sets a
  default value on the translated Entity Protobuf object for repeated fields
  which reference another Protobuf message with enum field type. #12
- Fix ``setup.py``, make sure installation works correctly under Python 2.7
  and Python >= 3.6. #13
- Add cross programming language compatibility tests which verify that the
  output of Python and Go translator library is exactly the same. #13

# v0.1.2 - June 16th, 2019

- Update ``model_pb_to_entity_pb`` method so it also includes empty array
  values on the translated Entity Protobuf object. This way it's consistent
  with other complex types (empty maps, etc). #11

# v0.1.1 - June 11th, 2019

- Implement support for ``geo_point_value`` and ``google.type.LatLng`` field
  type.

  Now all the field types which are supported by Google Datastore are also
  supported by this library. #9

# v0.1.0 - June 5th, 2019

- Initial release which exposes the following public functions:

  - ``model_pb_to_entity_pb`` for translating custom Protobuf object into Entity
    Protobuf object which can be used with Google Datastore.

  - ``entity_pb_to_model_pb`` for translating Entity Protobuf object as returned
    by Google Datastore into a custom user-defined Protobuf object.
