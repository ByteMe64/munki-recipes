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
# Unless required by applicable law of a statutory law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This processor finds the download URL for the latest version of DaVinci Resolve
or DaVinci Resolve Studio.
"""

import re
import json
from autopkglib import ProcessorError, URLGetter

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
        "product_name": {"required": True, "description": "Product to download."},
        "major_version": {"required": False, "default": "20", "description": "The major version to look for."},
    }
    output_variables = {
        "url": {"description": "The URL for the latest release of the given product."},
        "version": {"description": "The version of the latest release."},
    }

    def main(self):
        """
        Find the URL for the latest DaVinci Resolve download.
        """
        try:
            raw_json = self.download(SUPPORT_PAGE_URL, text=True)
            json_data = json.loads(raw_json)
        except Exception as e:
            raise ProcessorError(f"Could not retrieve or parse support page JSON: {e}")

        # --- DIAGNOSTIC STEP ---
        # Print all available category titles so we can see what they are now.
        all_titles = [category.get("title", "NO TITLE") for category in json_data.get("downloads", [])]
        self.output("--- Available Category Titles ---")
        for title in all_titles:
            self.output(title)
        self.output("---------------------------------")
        # --- END DIAGNOSTIC STEP ---
        
        # The script will now fail intentionally after printing the titles.
        raise ProcessorError(
            "Diagnostic run complete. Please check the output above for the correct category title."
        )

if __name__ == "__main__":
    PROCESSOR = BlackMagicURLProvider()
    PROCESSOR.execute_shell()