.PHONY: all
all: protobuf

.PHONY: protobuf
protobuf:
	echo "Generating protobuf files..."
	mkdir -p tests/generated/
	touch tests/generated/__init__.py
	protoc --proto_path=protobuf/ --python_out=tests/generated/ protobuf/*.proto
