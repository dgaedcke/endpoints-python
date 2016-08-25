# Copyright 2016 Google Inc. All Rights Reserved.
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
"""Module for setting up App Engine library paths.

This module searches for the root of the App Engine Python SDK or Google Cloud
SDK and computes a list of library paths and adds them to sys.path. This is
necessary for two reasons:

1. The endpointscfg tool imports user code and therefore must be able to
   import modules used in the app.
2. As a consequence of the first item, we must call an App Engine method to
   set up service stubs in case an app's initialization code utilizes an App
   Engine service. For example, there exists an App Engine version of pytz
   which uses memcache and users may use it at the global level because it
   seems to be declarative.
"""
import logging
import os
import sys

_PYTHON_EXTENSIONS_WARNING = """
Found Cloud SDK, but App Engine Python Extensions are not
installed. If you encounter errors, please run:
  $ gcloud components install app-engine-python
""".strip()


_IMPORT_ERROR_WARNING = """
Could not import App Engine Python libraries. If you encounter
errors, please make sure that the SDK binary path is in your PATH environment
variable or that the ENDPOINTS_GAE_SDK variable points to a valid SDK root.
""".strip()


_NOT_FOUND_WARNING = """
Could not find either the Cloud SDK or the App Engine Python SDK.
If you encounter errors, please make sure that the SDK binary path is in your
PATH environment variable or that the ENDPOINTS_GAE_SDK variable points to a
valid SDK root.""".strip()


def _FindSdkPath():
  environ_sdk = os.environ.get('ENDPOINTS_GAE_SDK')
  if environ_sdk:
    maybe_cloud_sdk = os.path.join(environ_sdk, 'platform', 'google_appengine')
    if os.path.exists(maybe_cloud_sdk):
      return maybe_cloud_sdk
    return environ_sdk

  for path in os.environ['PATH'].split(os.pathsep):
    if os.path.exists(os.path.join(path, 'dev_appserver.py')):
      if (path.endswith('bin') and
          os.path.exists(os.path.join(path, 'gcloud'))):
        # Cloud SDK ships with dev_appserver.py in a bin directory. In the
        # root directory, we can find the Python SDK in
        # platform/google_appengine provided that it's installed.
        sdk_path = os.path.join(os.path.dirname(path),
                                'platform',
                                'google_appengine')
        if not os.path.exists(sdk_path):
          logging.warning(_PYTHON_EXTENSIONS_WARNING)
        return sdk_path
      # App Engine SDK ships withd dev_appserver.py in the root directory.
      return path


def _SetupPaths():
  sdk_path = _FindSdkPath()
  if sdk_path:
    sys.path.append(sdk_path)
    try:
      import wrapper_util  # pylint: disable=g-import-not-at-top
      paths = wrapper_util.Paths(sdk_path)
      additional_paths = paths.v1_extra_paths + paths.endpointscfg_extra_paths
      sys.path = additional_paths + sys.path
    except ImportError:
      logging.warning(_IMPORT_ERROR_WARNING)
    return
  else:
    logging.warning(_NOT_FOUND_WARNING)


_SetupPaths()
