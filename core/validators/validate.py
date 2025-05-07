import re
import tldextract
from typing import Optional


class Validator:
    @staticmethod
    def check_email(value):
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,10}\b"
        return re.match(pattern, value)

    @staticmethod
    def check_domain(domain: str) -> Optional[str]:
        """
        Extract and validate a registered domain from a domain string.

        This function uses tldextract to parse the domain and verify if it's a
        valid registered domain (containing both a domain name and a TLD).

        Args:
            domain: A string representing a domain name or URL

        Returns:
            str: The registered domain if valid (e.g., "example.com")
            None: If no valid registered domain is found

        Examples:
            >>> check_domain("https://www.example.com/page")
            'example.com'
            >>> check_domain("subdomain.example.co.uk")
            'example.co.uk'
            >>> check_domain("invalid")
            None
        """
        if not domain:
            return None

        extract_result = tldextract.extract(domain)

        if extract_result.registered_domain:
            return extract_result.registered_domain

        return None
