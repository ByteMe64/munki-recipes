#!/usr/local/autopkg/python
#
# Copyright 2024 Paul Evans
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law of a statutory law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This processor finds the download URL for the latest version of DaVinci Resolve
or DaVinci Resolve Studio from the new JSON API structure.
"""

import re
import json
from autopkglib import ProcessorError, URLGetter

__all__ = ["BlackMagicURLProvider"]

SUPPORT_PAGE_URL = "https://www.blackmagicdesign.com/api/support/us/downloads.json"

class BlackMagicURLProvider(URLGetter):
    """
    This processor finds the download URL for the latest version of DaVinci Resolve
    or DaVinci Resolve Studio.
    """
    description = __doc__
    input_variables = {
        "product_name": {
            "required": True,
            "description": (
                "Product to download, e.g., 'DaVinci Resolve' or 'DaVinci Resolve Studio'."
            ),
        },
        "major_version": {