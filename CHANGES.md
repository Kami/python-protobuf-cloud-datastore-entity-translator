# v0.1.0 - June 5th, 2019

- Initial release which exposes the following public functions:

  - ``model_pb_to_entity_pb`` for translating custom Protobuf object into Entity
    Protobuf object which can be used with Google Datastore.

  - ``entity_pb_to_model_pb`` for translating Entity Protobuf object as returned
    by Google Datastore into a custom user-defined Protobuf object.
