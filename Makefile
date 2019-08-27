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
	# Workaround for Protobuf compiler not using relative imports which breakes things
	sed -i -E "s/^from models(.*) import/from ..models\1 import/" tests/generated/*/*.py
	sed -i -E "s/^from models(.*) import/from ..models\1 import/" tests/generated/*/*.pyi
	sed -i -E "s/^import options(.*)/from . import options\1/" tests/generated/*.py
	sed -i -E "s/^import options(.*)/from . import options\1/" tests/generated/*.pyi

.PHONY: protobuf-go
protobuf-go:
	echo "Generating Go protobuf files..."
	mkdir -p tests/generated/go/
	protoc --proto_path=protobuf/ --go_out=tests/generated/go/ protobuf/compat/example_compat.proto
