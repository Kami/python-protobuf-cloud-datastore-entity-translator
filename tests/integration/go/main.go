package main

import (
	"cloud.google.com/go/datastore"
	"context"
	"encoding/json"
	"flag"
	"github.com/Kami/python-protobuf-cloud-datastore-entity-translator/tests/generated/go"
	translator "github.com/Sheshagiri/go-protobuf-cloud-datastore-entity-translator/datastore-translator"
	"github.com/golang/protobuf/jsonpb"
	"log"
	"os"
)

func main() {
	typ := flag.String("type", "put/get", "put or get from from datastore")
	primaryKey := flag.String("primary-key", "", "primary key, this will be used as Name in Datastore Key, ex: key-1")
	jsonFile := flag.String("json-file", "", "path to json file containing protobuf")

	flag.Parse()

	ctx := context.Background()

	projectId := os.Getenv("DATASTORE_PROJECT_ID")

	if projectId == "" {
		projectId = "translator-tests"
	}

	dsClient, err := datastore.NewClient(ctx, projectId)

	if err != nil {
		log.Fatalf("unable to connect to datastore, error: %v", err)
	}
	defer dsClient.Close()

	translatedProto := &example_compat.ExampleDBModel{}
	kind := "ExampleDBModel"

	if *typ == "get" {
		key := datastore.NameKey(kind, *primaryKey, nil)
		log.Println("getting key from datastore: ", key.String())
		dsEntity, err := dsClient.GetEntity(ctx, key)
		if err != nil {
			log.Fatalf("unable to get from datastore, error: %v", err)
		}
		err = translator.DatastoreEntityToProtoMessage(dsEntity, translatedProto, true)
		// We want to use original field names and not CamelCase ones
		marshaller := jsonpb.Marshaler{OrigName: true, EmitDefaults: true}
		log.Println("dumping the proto message to stdout")
		err = marshaller.Marshal(os.Stdout, translatedProto)
		prettyJson, err := json.MarshalIndent(translatedProto, "", "    ")
		log.Printf("%s", string(prettyJson))
	} else if *typ == "put" {
		data, err := os.Open(*jsonFile)
		if err != nil {
			log.Printf("unable to read file %s, error: %v", *jsonFile, err)
		}
		err = jsonpb.Unmarshal(data, translatedProto)
		if err != nil {
			log.Printf("unmarshalling failed, error: %v", err)
		}
		log.Println("Original Proto: ", translatedProto)
		if err != nil {
			log.Fatalf("unable to load json, error: %v", err)
		}
		translatedEntity, err := translator.ProtoMessageToDatastoreEntity(translatedProto, true)
		log.Println("Translated Entity:", translatedEntity)
		if err != nil {
			log.Fatalf("unable to translate execution request to datastore format, error: %v", err)
		}
		key := datastore.NameKey(kind, *primaryKey, nil)
		_, err = dsClient.PutEntity(ctx, key, &translatedEntity)
		if err != nil {
			log.Fatalf("unable to translate execution request to datastore format, error: %v", err)
		}
		log.Printf("key %v is saved to datastore", key.String())
	} else {
		log.Fatalf("unknown type %s", *typ)
	}
}
