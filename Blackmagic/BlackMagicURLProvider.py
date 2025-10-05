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
        }, # This closing brace was missing
        "major_version": {
            "required": False,
            "default": "20",
            "description": "The major version to look for, e.g., '20'.",
        },
    }
    output_variables = {
        "url": {"description": "The URL for the latest release of the given product."},
        "version": {"description": "The version of the latest release."},
        "download_id": {"description": "The unique download ID for the release."},
    }

    def main(self):
        """
        Find the URL for the latest DaVinci Resolve download.
        """
        product_name_search = self.env["product_name"]
        major_version_search = self.env["major_version"]
        self.output(f"Searching for '{product_name_search}' version {major_version_search}...")

        try:
            raw_json = self.download(SUPPORT_PAGE_URL, text=True)
            json_data = json.loads(raw_json)
        except Exception as e:
            raise ProcessorError(f"Could not retrieve or parse support page JSON: {e}")

        all_downloads = json_data.get("downloads", [])
        if not all_downloads:
            raise ProcessorError("JSON data is missing the 'downloads' list.")
            
        latest_matching_download = None

        for download in all_downloads:
            release_name = download.get("name", "")
            
            if release_name.startswith(f"{product_name_search} {major_version_search}"):
                latest_matching_download = download
                self.output(f"Found a matching release: '{release_