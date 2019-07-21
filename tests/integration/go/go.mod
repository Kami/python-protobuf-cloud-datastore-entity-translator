module github.com/Kami/python-protobuf-cloud-datastore-entity-translator/tests/integration/go

go 1.12

require (
	cloud.google.com/go v0.43.0 // indirect
	github.com/Kami/python-protobuf-cloud-datastore-entity-translator/tests/generated/go v0.0.0-00010101000000-000000000000 // indirect
	github.com/Sheshagiri/go-protobuf-cloud-datastore-entity-translator v0.0.0-20190717044751-d1375259e3e5 // indirect
)

replace cloud.google.com/go => github.com/Sheshagiri/google-cloud-go v0.41.1-0.20190711043959-301311007500

replace github.com/Kami/python-protobuf-cloud-datastore-entity-translator/tests/generated/go => ../../generated/go
