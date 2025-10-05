#!/usr/local/autopkg/python

import json
from autopkglib import ProcessorError, URLGetter

__all__ = ["BlackMagicURLProvider"]

SUPPORT_PAGE_URL = "https://www.blackmagicdesign.com/api/support/us/downloads.json"

class BlackMagicURLProvider(URLGetter):
    """
    A diagnostic processor to download and print the raw JSON from Blackmagic's
    support API.
    """
    description = __doc__
    input_variables = {}
    output_variables = {}

    def main(self):
        """
        Download the JSON and print it to the console.
        """
        try:
            self.output("Downloading raw JSON from Blackmagic server...")
            raw_json = self.download(SUPPORT_PAGE_URL, text=True)
            
            # --- DIAGNOSTIC STEP ---
            self.output("--- Raw JSON Output ---")
            # Print the raw text directly to see its structure
            print(raw_json)
            self.output("-----------------------")
            # --- END DIAGNOSTIC STEP ---

        except Exception as e:
            raise ProcessorError(f"Could not retrieve or parse support page JSON: {e}")
        
        raise ProcessorError(
            "Diagnostic run complete. Please copy the raw JSON output above."
        )

if __name__ == "__main__":
    PROCESSOR = BlackMagicURLProvider()
    PROCESSOR.execute_shell()