import uuid

import httpx
from typing import Dict, Any, Optional, Union, ByteString


class HttpClient:
    """
    Asynchronous HTTP client using httpx with logging capabilities.

    This class provides methods for making HTTP requests with automatic
    logging, request ID generation, and consistent parameter handling.
    """

    def __init__(
            self,
            default_timeout: float = 300.0,
            default_connect_timeout: float = 10.0,
            default_retries: int = 3,
            use_http2: bool = True,
    ):
        """
        Initialize the HTTP client with default configuration.

        Args:
            default_timeout: The total time allowed for the entire request in seconds
            default_connect_timeout: The maximum time allowed to establish a connection in seconds
            default_retries: Number of retries for failed requests
            use_http2: Whether to use HTTP/2 protocol
        """
        self.default_timeout = default_timeout
        self.default_connect_timeout = default_connect_timeout
        self.default_retries = default_retries
        self.use_http2 = use_http2

    async def send(
            self,
            method: str,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            files=None,
            follow_redirects: bool = True,
            verify: bool = True,
            content: Optional[ByteString] = None,
    ) -> httpx.Response:
        """
        Send an HTTP request with the specified method and parameters.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: Target URL
            params: URL query parameters
            data: Form data to send
            json: JSON data to send
            headers: HTTP headers
            files: Files to upload
            follow_redirects: Whether to follow HTTP redirects
            verify: Whether to verify SSL certificates
            content: Raw content bytes to send

        Returns:
            httpx.Response: The HTTP response
        """
        # Set timeouts
        timeout = httpx.Timeout(self.default_timeout, connect=self.default_connect_timeout)
        transport = httpx.AsyncHTTPTransport(retries=self.default_retries, verify=verify)

        # Generate request ID and enrich headers
        request_id = str(uuid.uuid4())
        kwargs = {
            "params": params,
            "data": data,
            "json": json,
            "headers": headers,
            "files": files,
            "follow_redirects": follow_redirects,
            "content": content,
        }

        # Remove None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        kwargs = self._enrich_headers(kwargs, request_id)

        async with httpx.AsyncClient(
                timeout=timeout,
                transport=transport,
                http2=self.use_http2
        ) as client:
            response = await client.request(method, url, **kwargs)

        return response

    async def get(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            follow_redirects: bool = True,
            verify: bool = True,
            content: Optional[ByteString] = None,
    ) -> httpx.Response:
        """Send a GET request."""
        return await self.send(
            method="GET",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            follow_redirects=follow_redirects,
            verify=verify,
            content=content,
        )

    async def post(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            files=None,
            follow_redirects: bool = True,
            verify: bool = True,
    ) -> httpx.Response:
        """Send a POST request."""
        return await self.send(
            method="POST",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            files=files,
            follow_redirects=follow_redirects,
            verify=verify,
        )

    async def put(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            verify: bool = True,
    ) -> httpx.Response:
        """Send a PUT request."""
        return await self.send(
            method="PUT",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            verify=verify,
        )

    async def delete(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, Any]] = None,
            verify: bool = True,
    ) -> httpx.Response:
        """Send a DELETE request."""
        return await self.send(
            method="DELETE",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            verify=verify,
        )

    @staticmethod
    def _enrich_headers(kwargs: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """
        Add necessary headers to the request including the request ID.

        Args:
            kwargs: The keyword arguments for the request
            request_id: The unique ID for this request

        Returns:
            Dict with enriched headers
        """
        if kwargs.get("headers") is None:
            kwargs["headers"] = {"request_id": request_id}
        else:
            kwargs["headers"].update({"request_id": request_id})

        cleaned_headers = {}
        for key, value in kwargs["headers"].items():
            if key is not None and value is not None:
                cleaned_headers[key] = value
        kwargs["headers"] = cleaned_headers
        return kwargs
