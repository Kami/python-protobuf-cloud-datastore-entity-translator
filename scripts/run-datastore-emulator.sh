#!/usr/bin/env bash
# Script which installs and starts Google Cloud Datastore Emulator

export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install google-cloud-sdk google-cloud-sdk-datastore-emulator
nohup gcloud beta emulators datastore start --host-port=127.0.0.1:8081 --no-store-on-disk &
