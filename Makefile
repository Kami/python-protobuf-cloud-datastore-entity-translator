.PHONY: all
all: protobuf

.PHONY: protobuf
protobuf: protobuf-python protobuf-go

.PHONY: protobuf-python
protobuf-python:
	echo "Generating Python protobuf files..."
	mkdir -p tests/generated/
	touch tests/generated/__init__.py
	touch tests/generated/models/__init__.py
	protoc --proto_path=protobuf/ --mypy_out=tests/generated/ --python_out=tests/generated/ protobuf/*.proto
	protoc --proto_path=protobuf/ --mypy_out=tests/generated/ --python_out=tests/generated/ protobuf/models/*.proto

.PHONY: protobuf-go
protobuf-go:
	echo "Generating Go protobuf files..."
	mkdir -p tests/generated/
	protoc --proto_path=protobuf/ --go_out=tests/generated/go/ protobuf/example_compat.proto
