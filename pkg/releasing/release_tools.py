# Copyright 2019 The Bazel Authors. All rights reserved.
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
"""Utilities to help create a rule set release."""

import hashlib
import os
from string import Template
import textwrap


WORKSPACE_STANZA_TEMPLATE = Template(textwrap.dedent(
    """
    load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
    http_archive(
        name = "${repo}",
        url = "${url}",
        sha256 = "${sha256}",
    )
    """).strip())


DEPS_STANZA_TEMPLATE = Template(textwrap.dedent(
    """
    load("@${repo}//${setup_file}", ${to_load})
    """).strip())



def package_basename(repo, version):
  return '%s-%s.tar.gz' % (repo, version)


def get_package_sha256(tarball_path):
  with open(tarball_path, 'rb') as pkg_content:
    tar_sha256 = hashlib.sha256(pkg_content.read()).hexdigest()
  return tar_sha256


def workspace_content(url, repo, sha256, setup_file=None, deps_method=None,
                      toolchains_method=None):
  # Create the WORKSPACE stanza needed for this rule set.
  methods = []
  if deps_method:
    methods.append(deps_method)
  if toolchains_method:
    methods.append(toolchains_method)

  ret = WORKSPACE_STANZA_TEMPLATE.substitute({
      'url': url,
      'sha256': sha256,
      'repo': repo,
  })
  if methods:
    deps = DEPS_STANZA_TEMPLATE.substitute({
        'repo': repo,
        'setup_file': setup_file or ':deps.bzl',
        'to_load': ', '.join('"%s"' % m for m in methods),
    })
    ret += "\n%s" % deps

  for m in methods:
    ret += '\n%s()' % m

  return ret
