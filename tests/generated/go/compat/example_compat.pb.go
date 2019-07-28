// Code generated by protoc-gen-go. DO NOT EDIT.
// source: compat/example_compat.proto

package example_compat

import (
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	_struct "github.com/golang/protobuf/ptypes/struct"
	timestamp "github.com/golang/protobuf/ptypes/timestamp"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

type ExampleCompatEnumModel int32

const (
	ExampleCompatEnumModel_ENUM10 ExampleCompatEnumModel = 0
	ExampleCompatEnumModel_ENUM11 ExampleCompatEnumModel = 1
	ExampleCompatEnumModel_ENUM12 ExampleCompatEnumModel = 2
)

var ExampleCompatEnumModel_name = map[int32]string{
	0: "ENUM10",
	1: "ENUM11",
	2: "ENUM12",
}

var ExampleCompatEnumModel_value = map[string]int32{
	"ENUM10": 0,
	"ENUM11": 1,
	"ENUM12": 2,
}

func (x ExampleCompatEnumModel) String() string {
	return proto.EnumName(ExampleCompatEnumModel_name, int32(x))
}

func (ExampleCompatEnumModel) EnumDescriptor() ([]byte, []int) {
	return fileDescriptor_54e697ecc33a0316, []int{0}
}

type ExampleCompatNestedModel struct {
	StringKey            string                 `protobuf:"bytes,1,opt,name=string_key,json=stringKey,proto3" json:"string_key,omitempty"`
	Int32Key             int32                  `protobuf:"varint,2,opt,name=int32_key,json=int32Key,proto3" json:"int32_key,omitempty"`
	EnumKey              ExampleCompatEnumModel `protobuf:"varint,3,opt,name=enum_key,json=enumKey,proto3,enum=ExampleCompatEnumModel" json:"enum_key,omitempty"`
	XXX_NoUnkeyedLiteral struct{}               `json:"-"`
	XXX_unrecognized     []byte                 `json:"-"`
	XXX_sizecache        int32                  `json:"-"`
}

func (m *ExampleCompatNestedModel) Reset()         { *m = ExampleCompatNestedModel{} }
func (m *ExampleCompatNestedModel) String() string { return proto.CompactTextString(m) }
func (*ExampleCompatNestedModel) ProtoMessage()    {}
func (*ExampleCompatNestedModel) Descriptor() ([]byte, []int) {
	return fileDescriptor_54e697ecc33a0316, []int{0}
}

func (m *ExampleCompatNestedModel) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_ExampleCompatNestedModel.Unmarshal(m, b)
}
func (m *ExampleCompatNestedModel) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_ExampleCompatNestedModel.Marshal(b, m, deterministic)
}
func (m *ExampleCompatNestedModel) XXX_Merge(src proto.Message) {
	xxx_messageInfo_ExampleCompatNestedModel.Merge(m, src)
}
func (m *ExampleCompatNestedModel) XXX_Size() int {
	return xxx_messageInfo_ExampleCompatNestedModel.Size(m)
}
func (m *ExampleCompatNestedModel) XXX_DiscardUnknown() {
	xxx_messageInfo_ExampleCompatNestedModel.DiscardUnknown(m)
}

var xxx_messageInfo_ExampleCompatNestedModel proto.InternalMessageInfo

func (m *ExampleCompatNestedModel) GetStringKey() string {
	if m != nil {
		return m.StringKey
	}
	return ""
}

func (m *ExampleCompatNestedModel) GetInt32Key() int32 {
	if m != nil {
		return m.Int32Key
	}
	return 0
}

func (m *ExampleCompatNestedModel) GetEnumKey() ExampleCompatEnumModel {
	if m != nil {
		return m.EnumKey
	}
	return ExampleCompatEnumModel_ENUM10
}

// ExampleCompat DB model definition which contains most of the common field types (simple and scalar)
type ExampleCompatDBModel struct {
	// Simple types
	Int32Key  int32   `protobuf:"varint,1,opt,name=int32_key,json=int32Key,proto3" json:"int32_key,omitempty"`
	StringKey string  `protobuf:"bytes,2,opt,name=string_key,json=stringKey,proto3" json:"string_key,omitempty"`
	BoolKey   bool    `protobuf:"varint,3,opt,name=bool_key,json=boolKey,proto3" json:"bool_key,omitempty"`
	BytesKey  []byte  `protobuf:"bytes,4,opt,name=bytes_key,json=bytesKey,proto3" json:"bytes_key,omitempty"`
	DoubleKey float64 `protobuf:"fixed64,14,opt,name=double_key,json=doubleKey,proto3" json:"double_key,omitempty"`
	//float float_key = 15;
	Int64Key int64 `protobuf:"varint,16,opt,name=int64_key,json=int64Key,proto3" json:"int64_key,omitempty"`
	// Container types with simple values
	MapStringString map[string]string `protobuf:"bytes,5,rep,name=map_string_string,json=mapStringString,proto3" json:"map_string_string,omitempty" protobuf_key:"bytes,1,opt,name=key,proto3" protobuf_val:"bytes,2,opt,name=value,proto3"`
	MapStringInt32  map[string]int32  `protobuf:"bytes,6,rep,name=map_string_int32,json=mapStringInt32,proto3" json:"map_string_int32,omitempty" protobuf_key:"bytes,1,opt,name=key,proto3" protobuf_val:"varint,2,opt,name=value,proto3"`
	StringArrayKey  []string          `protobuf:"bytes,7,rep,name=string_array_key,json=stringArrayKey,proto3" json:"string_array_key,omitempty"`
	Int32ArrayKey   []int32           `protobuf:"varint,8,rep,packed,name=int32_array_key,json=int32ArrayKey,proto3" json:"int32_array_key,omitempty"`
	// Enum types
	EnumKey ExampleCompatEnumModel `protobuf:"varint,10,opt,name=enum_key,json=enumKey,proto3,enum=ExampleCompatEnumModel" json:"enum_key,omitempty"`
	// Complex types from protobuf stdlib
	TimestampKey         *timestamp.Timestamp `protobuf:"bytes,11,opt,name=timestamp_key,json=timestampKey,proto3" json:"timestamp_key,omitempty"`
	StructKey            *_struct.Struct      `protobuf:"bytes,12,opt,name=struct_key,json=structKey,proto3" json:"struct_key,omitempty"`
	XXX_NoUnkeyedLiteral struct{}             `json:"-"`
	XXX_unrecognized     []byte               `json:"-"`
	XXX_sizecache        int32                `json:"-"`
}

func (m *ExampleCompatDBModel) Reset()         { *m = ExampleCompatDBModel{} }
func (m *ExampleCompatDBModel) String() string { return proto.CompactTextString(m) }
func (*ExampleCompatDBModel) ProtoMessage()    {}
func (*ExampleCompatDBModel) Descriptor() ([]byte, []int) {
	return fileDescriptor_54e697ecc33a0316, []int{1}
}

func (m *ExampleCompatDBModel) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_ExampleCompatDBModel.Unmarshal(m, b)
}
func (m *ExampleCompatDBModel) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_ExampleCompatDBModel.Marshal(b, m, deterministic)
}
func (m *ExampleCompatDBModel) XXX_Merge(src proto.Message) {
	xxx_messageInfo_ExampleCompatDBModel.Merge(m, src)
}
func (m *ExampleCompatDBModel) XXX_Size() int {
	return xxx_messageInfo_ExampleCompatDBModel.Size(m)
}
func (m *ExampleCompatDBModel) XXX_DiscardUnknown() {
	xxx_messageInfo_ExampleCompatDBModel.DiscardUnknown(m)
}

var xxx_messageInfo_ExampleCompatDBModel proto.InternalMessageInfo

func (m *ExampleCompatDBModel) GetInt32Key() int32 {
	if m != nil {
		return m.Int32Key
	}
	return 0
}

func (m *ExampleCompatDBModel) GetStringKey() string {
	if m != nil {
		return m.StringKey
	}
	return ""
}

func (m *ExampleCompatDBModel) GetBoolKey() bool {
	if m != nil {
		return m.BoolKey
	}
	return false
}

func (m *ExampleCompatDBModel) GetBytesKey() []byte {
	if m != nil {
		return m.BytesKey
	}
	return nil
}

func (m *ExampleCompatDBModel) GetDoubleKey() float64 {
	if m != nil {
		return m.DoubleKey
	}
	return 0
}

func (m *ExampleCompatDBModel) GetInt64Key() int64 {
	if m != nil {
		return m.Int64Key
	}
	return 0
}

func (m *ExampleCompatDBModel) GetMapStringString() map[string]string {
	if m != nil {
		return m.MapStringString
	}
	return nil
}

func (m *ExampleCompatDBModel) GetMapStringInt32() map[string]int32 {
	if m != nil {
		return m.MapStringInt32
	}
	return nil
}

func (m *ExampleCompatDBModel) GetStringArrayKey() []string {
	if m != nil {
		return m.StringArrayKey
	}
	return nil
}

func (m *ExampleCompatDBModel) GetInt32ArrayKey() []int32 {
	if m != nil {
		return m.Int32ArrayKey
	}
	return nil
}

func (m *ExampleCompatDBModel) GetEnumKey() ExampleCompatEnumModel {
	if m != nil {
		return m.EnumKey
	}
	return ExampleCompatEnumModel_ENUM10
}

func (m *ExampleCompatDBModel) GetTimestampKey() *timestamp.Timestamp {
	if m != nil {
		return m.TimestampKey
	}
	return nil
}

func (m *ExampleCompatDBModel) GetStructKey() *_struct.Struct {
	if m != nil {
		return m.StructKey
	}
	return nil
}

func init() {
	proto.RegisterEnum("ExampleCompatEnumModel", ExampleCompatEnumModel_name, ExampleCompatEnumModel_value)
	proto.RegisterType((*ExampleCompatNestedModel)(nil), "ExampleCompatNestedModel")
	proto.RegisterType((*ExampleCompatDBModel)(nil), "ExampleCompatDBModel")
	proto.RegisterMapType((map[string]int32)(nil), "ExampleCompatDBModel.MapStringInt32Entry")
	proto.RegisterMapType((map[string]string)(nil), "ExampleCompatDBModel.MapStringStringEntry")
}

func init() { proto.RegisterFile("compat/example_compat.proto", fileDescriptor_54e697ecc33a0316) }

var fileDescriptor_54e697ecc33a0316 = []byte{
	// 501 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x8c, 0x52, 0x5f, 0x8f, 0xd2, 0x4e,
	0x14, 0xfd, 0x0d, 0xfd, 0x15, 0xca, 0x85, 0x65, 0x6b, 0x25, 0x2e, 0xb2, 0x1a, 0x27, 0xfb, 0x60,
	0xc6, 0x7d, 0x28, 0x6e, 0x77, 0x43, 0x8c, 0x31, 0x31, 0xbb, 0xca, 0x83, 0x21, 0xec, 0xc3, 0xa0,
	0xbe, 0x92, 0x16, 0x46, 0x42, 0xec, 0xbf, 0xb4, 0x53, 0x63, 0xbf, 0x82, 0xdf, 0xd8, 0x37, 0xd3,
	0x3b, 0xa5, 0x50, 0x24, 0x59, 0x5f, 0xda, 0x99, 0x73, 0xce, 0x3d, 0xf7, 0xcf, 0x5c, 0x38, 0x5f,
	0x46, 0x41, 0xec, 0xca, 0x91, 0xf8, 0xe9, 0x06, 0xb1, 0x2f, 0x16, 0xea, 0x6a, 0xc7, 0x49, 0x24,
	0xa3, 0xe1, 0xb3, 0x75, 0x14, 0xad, 0x7d, 0x31, 0xc2, 0x9b, 0x97, 0x7d, 0x1b, 0xa5, 0x32, 0xc9,
	0x96, 0x5b, 0xf6, 0xc5, 0x21, 0x2b, 0x37, 0x81, 0x48, 0xa5, 0x1b, 0xc4, 0x4a, 0x70, 0xf1, 0x8b,
	0xc0, 0x60, 0xa2, 0x7c, 0x3f, 0xa0, 0xed, 0xbd, 0x48, 0xa5, 0x58, 0xcd, 0xa2, 0x95, 0xf0, 0xad,
	0xe7, 0x00, 0xa9, 0x4c, 0x36, 0xe1, 0x7a, 0xf1, 0x5d, 0xe4, 0x03, 0x42, 0x09, 0x6b, 0xf3, 0xb6,
	0x42, 0xa6, 0x22, 0xb7, 0xce, 0xa1, 0xbd, 0x09, 0xe5, 0xb5, 0x83, 0x6c, 0x83, 0x12, 0xa6, 0x73,
	0x03, 0x81, 0x82, 0x74, 0xc0, 0x10, 0x61, 0x16, 0x20, 0xa7, 0x51, 0xc2, 0x7a, 0xce, 0x99, 0x5d,
	0x4b, 0x34, 0x09, 0xb3, 0x00, 0xd3, 0xf0, 0x56, 0x21, 0x9c, 0x8a, 0xfc, 0xe2, 0xb7, 0x0e, 0xfd,
	0x9a, 0xe6, 0xe3, 0x9d, 0x2a, 0xa4, 0x96, 0x89, 0x1c, 0x64, 0xaa, 0x57, 0xd9, 0x38, 0xac, 0xf2,
	0x29, 0x18, 0x5e, 0x14, 0xf9, 0x55, 0x21, 0x06, 0x6f, 0x15, 0xf7, 0xb2, 0x01, 0x2f, 0x97, 0x22,
	0x45, 0xee, 0x7f, 0x4a, 0x58, 0x97, 0x1b, 0x08, 0x94, 0xb6, 0xab, 0x28, 0xf3, 0x7c, 0x81, 0x6c,
	0x8f, 0x12, 0x46, 0x78, 0x5b, 0x21, 0xbb, 0xe6, 0xc7, 0x37, 0xc8, 0x9a, 0x94, 0x30, 0x0d, 0x4b,
	0x1a, 0xdf, 0x14, 0xe4, 0x57, 0x78, 0x14, 0xb8, 0xf1, 0xa2, 0x2c, 0x4b, 0xfd, 0x06, 0x3a, 0xd5,
	0x58, 0xc7, 0xb9, 0xb4, 0x8f, 0x75, 0x68, 0xcf, 0xdc, 0x78, 0x8e, 0x32, 0xf5, 0x9d, 0x84, 0x32,
	0xc9, 0xf9, 0x69, 0x50, 0x47, 0xad, 0x39, 0x98, 0x7b, 0xbe, 0x38, 0x81, 0x41, 0x13, 0x6d, 0x5f,
	0x3d, 0x60, 0xfb, 0xa9, 0xd0, 0x2a, 0xd7, 0x5e, 0x50, 0x03, 0x2d, 0x06, 0x66, 0x69, 0xe8, 0x26,
	0x89, 0x9b, 0x63, 0x43, 0x2d, 0xaa, 0xb1, 0x36, 0xef, 0x29, 0xfc, 0xb6, 0x80, 0x8b, 0xb6, 0x5e,
	0xc2, 0xa9, 0x7a, 0x86, 0x9d, 0xd0, 0xa0, 0x1a, 0xd3, 0xf9, 0x09, 0xc2, 0x95, 0x6e, 0xff, 0xed,
	0xe1, 0xdf, 0xde, 0xde, 0x7a, 0x0f, 0x27, 0xd5, 0x6e, 0x62, 0x60, 0x87, 0x12, 0xd6, 0x71, 0x86,
	0xb6, 0xda, 0x60, 0x7b, 0xbb, 0xc1, 0xf6, 0xe7, 0xad, 0x8a, 0x77, 0xab, 0x80, 0xc2, 0x60, 0x8c,
	0x6b, 0x90, 0x2d, 0x25, 0x46, 0x77, 0x31, 0xfa, 0xec, 0xaf, 0xe8, 0x39, 0x4a, 0x70, 0x3f, 0xb2,
	0xa5, 0x9c, 0x8a, 0x7c, 0x78, 0x07, 0xfd, 0x63, 0xc3, 0xb7, 0x4c, 0xd0, 0x76, 0x5b, 0x5f, 0x1c,
	0xad, 0x3e, 0xe8, 0x3f, 0x5c, 0x3f, 0x13, 0xe5, 0x8e, 0xa9, 0xcb, 0xdb, 0xc6, 0x1b, 0x32, 0xbc,
	0x85, 0xc7, 0x47, 0x26, 0xfd, 0x90, 0x85, 0xbe, 0x67, 0x71, 0xf9, 0x0e, 0x9e, 0x1c, 0x1f, 0x91,
	0x05, 0xd0, 0x9c, 0xdc, 0x7f, 0x99, 0x5d, 0xbd, 0x36, 0xff, 0xab, 0xce, 0x57, 0x26, 0xa9, 0xce,
	0x8e, 0xd9, 0xf0, 0x9a, 0xd8, 0xe0, 0xf5, 0x9f, 0x00, 0x00, 0x00, 0xff, 0xff, 0x54, 0x13, 0x2c,
	0x36, 0x2b, 0x04, 0x00, 0x00,
}
