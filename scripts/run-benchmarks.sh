#!/usr/bin/env bash
# Copyright 2019 Tomaz Muraus
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

#Script which runs py.test benchmarks and also compares results to previous run (if previous run
# exists)

OUTPUT=$(ls -la .benchmarks)
EXIT_CODE=$?

if [ ${EXIT_CODE} -ne 0 ]; then
    # Previous run doesn't exist yet, create one so we have something to compare against during
    # the next run
    echo "Previous run doesn't exist, skipping compare..."
    exec py.test --benchmark-autosave tests/test_benchmarks.py
else
    exec py.test --benchmark-autosave --benchmark-compare --benchmark-compare-fail=min:14% tests/test_benchmarks.py
fi
