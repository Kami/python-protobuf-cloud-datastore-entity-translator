.PHONY: all
all: protobuf

.PHONY: protobuf
protobuf: protobuf-python protobuf-go

.PHONY: protobuf-python
protobuf-python:
	echo "Generating Python protobuf files..."
	mkdir -p tests/generated/models
	mkdir -p tests/generated/compat
	touch tests/generated/__init__.py
	touch tests/generated/models/__init__.py
	touch tests/generated/compat/__init__.py
	protoc --proto_path=protobuf/ --mypy_out=tests/generated/ --python_out=tests/generated/ protobuf/*.proto
	protoc --proto_path=protobuf/ --mypy_out=tests/generated/ --python_out=tests/generated/ protobuf/models/*.proto
	protoc --proto_path=protobuf/ --mypy_out=tests/generated/ --python_out=tests/generated/ protobuf/compat/example_compat.proto

.PHONY: protobuf-go
protobuf-go:
	echo "Generating Go protobuf files..."
	mkdir -p tests/generated/go/
	protoc --proto_path=protobuf/ --go_out=tests/generated/go/ protobuf/compat/example_compat.proto
