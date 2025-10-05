#!/usr/local/autopkg/python
#
# Copyright 2022 James Stewart
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

"""
This processor finds the download URL for the latest version of DaVinci Resolve
or DaVinci Resolve Studio.
"""

import re

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["BlackMagicURLProvider"]

# URL of the support page
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
                "Product to download. At the moment, only 'DaVinci Resolve' and "
                "'DaVinci Resolve Studio' are supported."
            ),
        },
        "major_version": {
            "required": False,
            "default": "20",
            "description": "The major version to look for, e.g., '20'.",
        },
    }
    output_variables = {
        "url": {"description": "The URL for the latest release of the given product."},
        "version": {"description": "The version of the latest release."},
    }

    def main(self):
        """
        Find the URL for the latest DaVinci Resolve download.
        """
        product_name = self.env["product_name"]
        major_version = self.env["major_version"]
        self.output(f"Searching for {product_name} version {major_version}...")

        try:
            json_data = self.download_json(SUPPORT_PAGE_URL)
        except Exception as e:
            raise ProcessorError(f"Could not retrieve support page JSON: {e}")

        # Find the DaVinci Resolve product family
        resolve_downloads = None
        for category in json_data.get("downloads", []):
            if category.get("title") == "DaVinci Resolve":
                resolve_downloads = category.get("mac")
                break
        
        if not resolve_downloads:
            raise ProcessorError("Could not find 'DaVinci Resolve' download category in JSON.")

        # Construct the search pattern based on product name and major version
        # Example: "DaVinci Resolve Studio 20.1"
        search_pattern = re.compile(
            rf"^{re.escape(product_name)}\s+{re.escape(major_version)}.*"
        )
        
        latest_matching_download = None

        for download in resolve_downloads:
            release_name = download.get("title", "")
            if search_pattern.match(release_name):
                # We found a match, assume this is the latest and break
                # The support pages usually list the newest versions first
                latest_matching_download = download
                break
        
        if not latest_matching_download:
            raise ProcessorError(
                f"Could not find a download matching '{product_name} {major_version}'."
            )

        # Extract version number from the title
        version_match = re.search(r"(\d+(\.\d+)+)", latest_matching_download["title"])
        if not version_match:
            raise ProcessorError("Could not parse version number from download title.")
        
        self.env["version"] = version_match.group(0)
        self.env["url"] = latest_matching_download.get("urls", {}).get("Mac OS X")
        
        if not self.env["url"]:
            raise ProcessorError("Could not find a macOS download URL for the release.")

        self.output(f"Found version: {self.env['version']}")
        self.output(f"Download URL: {self.env['url']}")

if __name__ == "__main__":
    PROCESSOR = BlackMagicURLProvider()
    PROCESSOR.execute_shell()