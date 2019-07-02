.PHONY: all
all: protobuf

.PHONY: protobuf
protobuf:
	echo "Generating protobuf files..."
	mkdir -p tests/generated/
	touch tests/generated/__init__.py
	touch tests/generated/models/__init__.py
	protoc --proto_path=protobuf/ --mypy_out=tests/generated/ --python_out=tests/generated/ protobuf/*.proto
	protoc --proto_path=protobuf/ --mypy_out=tests/generated/ --python_out=tests/generated/ protobuf/models/*.proto
