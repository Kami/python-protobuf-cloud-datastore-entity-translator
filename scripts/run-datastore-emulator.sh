#!/usr/bin/env bash
# Copyright 2019 Tomaz Muraus
# Copyright 2019 Extreme Networks, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Script which installs and starts Google Cloud Datastore Emulator

# Install Cloud SDK
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install google-cloud-sdk google-cloud-sdk-datastore-emulator

gcloud beta emulators datastore start --host-port=127.0.0.1:8081 --no-store-on-disk &> /tmp/emulator.log &
EMULATOR_PID=$!

# Give process some time to start up
sleep 5

if ps -p ${EMULATOR_PID} > /dev/null; then
    echo "Datastore emulator successfully started"
    tail -30 /tmp/emulator.log
    exit 0
else
    echo "Failed to start Datastore emulator"
    tail -30 /tmp/emulator.log
    exit 1
fi
