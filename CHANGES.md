# in development

- Update ``model_pb_to_entity_pb`` method so it always explicitly sets enum
  values for repeated fields which reference another Protobuf message with
  enum field.

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
