# GopherGun 🚀 **Your One-Way Ticket to Forging Gopher Payloads for SSRF.**

![Language: Go](https://img.shields.io/badge/language-python-blue.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)
<br>

**Crafted with ❤️ by EragonKashyap11**
![Demo](
---

### **Table of Contents**
- [Overview](#overview)
- [Why GopherGun?](#why-GopherGun)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
  - [Help Menu](#help-menu)
  - [Interactive Mode](#interactive-mode)
  - [Command-Line Mode Examples](#command-line-mode-examples)
- [Understanding the Outputs](#understanding-the-outputs)
- [License](#license)

## Overview

**GopherGun** is a powerful and user-friendly Python script designed to generate Gopher payloads that perfectly replicate HTTP requests. It's an essential tool for security researchers and penetration testers who need to craft precise payloads for exploiting Server-Side Request Forgery (SSRF) vulnerabilities.

Manually creating Gopher payloads is tedious and error-prone. You have to worry about `CRLF` line endings, URL encoding, and the dreaded double-encoding required when injecting the payload into a URL parameter. GopherGun automates this entire process, letting you focus on the exploit.

## Why GopherGun?

Dealing with SSRF that allows the `gopher://` wrapper can be a goldmine, but crafting the payload is a pain. GopherGun solves the most common frustrations:

-   **Incorrect Line Endings:** Automatically handles the `CRLF` (`\r\n`) endings required by the HTTP protocol.
-   **Complex Encoding:** Provides both single-encoded and double-encoded outputs, so you have the right format for any SSRF scenario.
-   **Dynamic Content-Length:** Forget calculating the size of your POST/PUT data. GopherGun does it for you automatically.
-   **Speed and Efficiency:** Switch between a guided interactive mode and a fast command-line mode perfect for scripting and automation.

## Key Features

-   **Dual Mode Operation:** Use the friendly **interactive mode** for guided payload creation or the powerful **command-line mode** for quick, scripted generation.
-   **Full HTTP Method Support:** Generates payloads for `GET`, `POST`, and `PUT` requests.
-   **Automatic Content-Length:** Auto-calculates the `Content-Length` header for `POST` and `PUT` requests.
-   **Multiple Output Formats:** Provides three essential outputs:
    1.  **Raw Request:** For verification and manual use.
    2.  **Single-Encoded:** Standard Gopher URL.
    3.  **Double-Encoded:** For injecting into URL parameters during SSRF attacks.
-   **Custom Headers:** Easily add multiple custom HTTP headers.
-   **File Input:** Read request body data directly from a file using the `--file` flag.
-   **Built-in Help:** A comprehensive and auto-generated `--help` menu explains every option.

## Installation

No complex installation is needed. Just grab the script!

1.  **Save the script** (not included here) as `GopherGun.py`.
2.  **Ensure you have Python 3.**
3.  (Optional) Make the script executable for easier use:
    ```bash
    chmod +x GopherGun.py
    ```

## Usage

GopherGun is flexible. You can run it with arguments for speed or without any for a guided experience.

### Help Menu

To see all available commands and options, run:
```bash
python3 GopherGun.py --help
```
```
usage: GopherGun.py [-h] [--headers HEADERS] [--data DATA | --file FILE] [method] [host] [port] [path]

A script to generate Gopher payloads for crafting HTTP requests. Useful for exploiting Server-Side Request Forgery (SSRF) vulnerabilities. The script can be run with command-line arguments or in
interactive mode.

positional arguments:
  method                The HTTP method (GET, POST, PUT).
  host                  The target host (e.g., 127.0.0.1).
  port                  The target port (e.g., 80).
  path                  The request path (e.g., /index.php).

options:
  -h, --help            show this help message and exit
  --headers HEADERS     An HTTP header. Can be specified multiple times (e.g., --headers "User-Agent: MyClient").
  --data DATA           The request body data for POST/PUT requests.
  --file FILE           File containing the request body data for POST/PUT.

Examples:
  # Run in interactive mode
  python3 GopherGun.py

  # Generate a GET request
  python3 GopherGun.py GET 127.0.0.1 80 /

  # Generate a POST request with headers and data
  python3 GopherGun.py POST 127.0.0.1 80 /login.php --headers "Content-Type: application/x-www-form-urlencoded" --data "user=admin&pass=123"

  # Generate a PUT request with data from a file
  python3 GopherGun.py PUT 127.0.0.1 80 /api/v1/resource --file ./data.json --headers "Content-Type: application/json"
```

### Interactive Mode

For a step-by-step guided process, simply run the script without any arguments:
```bash
python3 GopherGun.py
```
The script will then prompt you for the method, host, port, path, headers, and data.

### Command-Line Mode Examples

#### **1. Simple GET Request**
```bash
python3 GopherGun.py GET 127.0.0.1 80 /
```

#### **2. POST Request with Multiple Headers**
To provide more than one custom header, just use the `--headers` flag multiple times.
```bash
python3 GopherGun.py POST 192.168.1.10 8080 /api/v2/users \
--data "name=hacker&role=admin" \
--headers "Content-Type: application/x-www-form-urlencoded" \
--headers "X-Forwarded-For: 127.0.0.1" \
--headers "Cookie: session=xyz123"
```

#### **3. PUT Request with JSON Data from a File**
First, create your data file (`data.json`):
```json
{
  "action": "update",
  "user_id": 1,
  "is_admin": true
}
```
Now, run GopherGun using the `--file` flag:
```bash
python3 GopherGun.py PUT internal.service 80 /api/user/update \
--file data.json \
--headers "Content-Type: application/json"```
```

## Understanding the Outputs

GopherGun provides three payloads. Knowing which one to use is key:

1.  **Raw HTTP Request:**
    -   This is the plain-text representation of the HTTP request.
    -   **Use Case:** Verifying that your request is structured correctly before encoding.

2.  **Standard Gopher URL (Single-Encoded):**
    -   A standard `gopher://` URL where the payload has been URL-encoded once.
    -   **Use Case:** Use this when the vulnerable application *directly* expects a Gopher URL.

3.  **Double-Encoded Payload (for SSRF):**
    -   The *entire Gopher URL* (including `gopher://`) from the previous step is URL-encoded a second time.
    -   **Use Case:** This is the most common format for SSRF. Use this when you are passing the Gopher link as a **parameter value in another URL**, like `http://victim.com/proxy?url=[PASTE_THIS_PAYLOAD_HERE]`.

## License

This project is licensed under the MIT License.
