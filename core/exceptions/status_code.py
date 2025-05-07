# 1xx - Informational responses
HTTP_100_CONTINUE = 100
HTTP_101_SWITCHING_PROTOCOLS = 101
HTTP_102_PROCESSING = 102
HTTP_103_EARLY_HINTS = 103

# 2xx - Successful responses
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
HTTP_204_NO_CONTENT = 204
HTTP_205_RESET_CONTENT = 205
HTTP_206_PARTIAL_CONTENT = 206
HTTP_207_MULTI_STATUS = 207
HTTP_208_ALREADY_REPORTED = 208
HTTP_226_IM_USED = 226

# 3xx - Redirection messages
HTTP_300_MULTIPLE_CHOICES = 300
HTTP_301_MOVED_PERMANENTLY = 301
HTTP_302_FOUND = 302
HTTP_303_SEE_OTHER = 303
HTTP_304_NOT_MODIFIED = 304
HTTP_305_USE_PROXY = 305  # Deprecated
HTTP_306_SWITCH_PROXY = 306  # Not used
HTTP_307_TEMPORARY_REDIRECT = 307
HTTP_308_PERMANENT_REDIRECT = 308

# 4xx - Client error responses
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_402_PAYMENT_REQUIRED = 402
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_406_NOT_ACCEPTABLE = 406
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
HTTP_408_REQUEST_TIMEOUT = 408
HTTP_409_CONFLICT = 409
HTTP_410_GONE = 410
HTTP_411_LENGTH_REQUIRED = 411
HTTP_412_PRECONDITION_FAILED = 412
HTTP_413_PAYLOAD_TOO_LARGE = 413
HTTP_414_URI_TOO_LONG = 414
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
HTTP_416_RANGE_NOT_SATISFIABLE = 416
HTTP_417_EXPECTATION_FAILED = 417
HTTP_418_IM_A_TEAPOT = 418
HTTP_421_MISDIRECTED_REQUEST = 421
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_423_LOCKED = 423
HTTP_424_FAILED_DEPENDENCY = 424
HTTP_425_TOO_EARLY = 425
HTTP_426_UPGRADE_REQUIRED = 426
HTTP_428_PRECONDITION_REQUIRED = 428
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451

# 5xx - Server error responses
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_501_NOT_IMPLEMENTED = 501
HTTP_502_BAD_GATEWAY = 502
HTTP_503_SERVICE_UNAVAILABLE = 503
HTTP_504_GATEWAY_TIMEOUT = 504
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
HTTP_506_VARIANT_ALSO_NEGOTIATES = 506
HTTP_507_INSUFFICIENT_STORAGE = 507
HTTP_508_LOOP_DETECTED = 508
HTTP_510_NOT_EXTENDED = 510
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511

STATUS_DESCRIPTIONS = {
    # 1xx - Informational responses
    100: "Continue - The server has received the request headers and the client should proceed to send the request body.",
    101: "Switching Protocols - The requester has asked the server to switch protocols and the server has agreed to do so.",
    102: "Processing - The server has received and is processing the request, but no response is available yet.",
    103: "Early Hints - Used to return some response headers before final HTTP message.",

    # 2xx - Successful responses
    200: "OK - The request has succeeded.",
    201: "Created - The request has been fulfilled and a new resource has been created.",
    202: "Accepted - The request has been accepted for processing, but the processing has not been completed.",
    203: "Non-Authoritative Information - The returned metadata is not exactly the same as is available from the origin server.",
    204: "No Content - The server has fulfilled the request but does not need to return a response body.",
    205: "Reset Content - The server has fulfilled the request and the client should reset the document view.",
    206: "Partial Content - The server has fulfilled the partial GET request for the resource.",
    207: "Multi-Status - Multiple separate responses are being provided.",
    208: "Already Reported - The members of a DAV binding have already been enumerated in a preceding part of the response.",
    226: "IM Used - The server has fulfilled a request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.",

    # 3xx - Redirection messages
    300: "Multiple Choices - The requested resource has multiple representations available.",
    301: "Moved Permanently - The requested resource has been assigned a new permanent URI.",
    302: "Found - The requested resource resides temporarily under a different URI.",
    303: "See Other - The response to the request can be found under a different URI and should be retrieved using a GET method.",
    304: "Not Modified - The resource has not been modified since the last request.",
    305: "Use Proxy (Deprecated) - The requested resource is available only through a proxy.",
    306: "Switch Proxy (Not used) - This code was used in a previous version of the specification but is no longer used.",
    307: "Temporary Redirect - The requested resource resides temporarily under a different URI.",
    308: "Permanent Redirect - The requested resource has been assigned a new permanent URI.",

    # 4xx - Client error responses
    400: "Bad Request - The server cannot or will not process the request due to a client error.",
    401: "Unauthorized - Authentication is required and has failed or has not been provided.",
    402: "Payment Required - Reserved for future use.",
    403: "Forbidden - The server understood the request but refuses to authorize it.",
    404: "Not Found - The requested resource could not be found on the server.",
    405: "Method Not Allowed - The method specified in the request is not allowed for the resource.",
    406: "Not Acceptable - The server cannot produce a response matching the list of acceptable values.",
    407: "Proxy Authentication Required - Authentication with the proxy is required.",
    408: "Request Timeout - The server timed out waiting for the request.",
    409: "Conflict - The request could not be completed due to a conflict with the current state of the resource.",
    410: "Gone - The requested resource is no longer available at the server and no forwarding address is known.",
    411: "Length Required - The server refuses to accept the request without a defined Content-Length.",
    412: "Precondition Failed - One of the preconditions specified by the client failed.",
    413: "Payload Too Large - The server refuses to process a request because the request payload is too large.",
    414: "URI Too Long - The server refuses to service the request because the request-target is longer than the server is willing to interpret.",
    415: "Unsupported Media Type - The server refuses to accept the request because the media type is not supported.",
    416: "Range Not Satisfiable - The client has asked for a portion of the file, but the server cannot supply that portion.",
    417: "Expectation Failed - The server cannot meet the requirements of the Expect request-header field.",
    418: "I'm a teapot - The server refuses the attempt to brew coffee with a teapot.",
    421: "Misdirected Request - The request was directed at a server that is not able to produce a response.",
    422: "Unprocessable Entity - The request was well-formed but was unable to be followed due to semantic errors.",
    423: "Locked - The resource that is being accessed is locked.",
    424: "Failed Dependency - The request failed due to failure of a previous request.",
    425: "Too Early - The server is unwilling to risk processing a request that might be replayed.",
    426: "Upgrade Required - The server refuses to perform the request using the current protocol.",
    428: "Precondition Required - The origin server requires the request to be conditional.",
    429: "Too Many Requests - The user has sent too many requests in a given amount of time.",
    431: "Request Header Fields Too Large - The server is unwilling to process the request because its header fields are too large.",
    451: "Unavailable For Legal Reasons - The server is denying access to the resource as a consequence of a legal demand.",

    # 5xx - Server error responses
    500: "Internal Server Error - The server encountered an unexpected condition that prevented it from fulfilling the request.",
    501: "Not Implemented - The server does not support the functionality required to fulfill the request.",
    502: "Bad Gateway - The server, while acting as a gateway or proxy, received an invalid response from an upstream server.",
    503: "Service Unavailable - The server is currently unable to handle the request due to temporary overloading or maintenance.",
    504: "Gateway Timeout - The server, while acting as a gateway or proxy, did not receive a timely response from an upstream server.",
    505: "HTTP Version Not Supported - The server does not support the HTTP protocol version used in the request.",
    506: "Variant Also Negotiates - The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself.",
    507: "Insufficient Storage - The server is unable to store the representation needed to complete the request.",
    508: "Loop Detected - The server detected an infinite loop while processing the request.",
    510: "Not Extended - Further extensions to the request are required for the server to fulfill it.",
    511: "Network Authentication Required - The client needs to authenticate to gain network access."
}
