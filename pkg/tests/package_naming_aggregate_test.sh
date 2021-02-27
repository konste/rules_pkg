# Copyright 2021 The Bazel Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This test simply checks that when we create packages with package_file_name
# that we get the expected file names.
set -e

declare -r DATA_DIR="${TEST_SRCDIR}/rules_pkg/tests"

for pkg in test_naming_some_value.deb test_naming_some_value.tar test_naming_some_value.zip ; do
  ls -l "${DATA_DIR}/$pkg"
done

TAR_STRUCTURE=$(tar -tf tests/test_tar_package_dir_substitution.tar)
EXPECTED_OUTPUT=$'./\x0a./level1/\x0a./level1/some_value/\x0a./level1/some_value/level3/\x0a./level1/some_value/level3/BUILD'
if [[ "$TAR_STRUCTURE" != "$EXPECTED_OUTPUT" ]]; then
    echo "Unexpected TAR structure."
    exit 1
fi

echo "PASS"
