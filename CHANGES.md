# v0.1.1 - June 11th, 2019

- Implement support for ``geo_point_value`` and ``google.type.LatLng`` field
  type.

  Now all the field types which are supported by Google Datastore are also
  supported by this library.

# v0.1.0 - June 5th, 2019

- Initial release which exposes the following public functions:

  - ``model_pb_to_entity_pb`` for translating custom Protobuf object into Entity
    Protobuf object which can be used with Google Datastore.

  - ``entity_pb_to_model_pb`` for translating Entity Protobuf object as returned
    by Google Datastore into a custom user-defined Protobuf object.
