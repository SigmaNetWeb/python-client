# SigmaNet Browser (Early Beta)

SigmaNet Browser is a simple browser client for navigating SigmaNet, a custom internet protocol using `sigma://` URLs. This client is in early beta and may contain bugs.

## Features

- Basic browsing functionality for `sigma://` URLs.
- Ability to register domains on `sigma://registrar.inf`.
- Supports HTML and basic CSS rendering.
- Timeout mechanism for handling slow responses.

## Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/SigmaNetWeb/python-client.git
   cd repository
   ```

2. **Install dependencies:**

   Ensure you have Python 3.x installed. Install required Python packages using pip.

   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the SigmaNet Browser:**

   ```
   python main.py
   ```

2. **Navigating SigmaNet:**

   - Enter `sigma://` URLs in the address bar.
   - Press Enter to navigate to the specified URL.
   - Links within pages are clickable and will open in the default browser.

3. **Registering Domains:**

   - To register a domain, navigate to `sigma://registrar.inf` in the address bar.
   - Follow the registration instructions on the registrar's page.

4. **Known Issues:**

   - HTML and CSS rendering may be incomplete or buggy.
   - Limited support for complex web pages.
   - Registrar and root domain server sometimes down
   - Timeout handling might not always work as expected.

## Contributing

Contributions are welcome! If you encounter bugs or have suggestions, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

### Explanation:

- **Installation**: Provides step-by-step instructions on cloning the repository and installing dependencies using `pip`.
- **Usage**: Describes how to run the SigmaNet Browser (`main.py`), navigate `sigma://` URLs, and register domains.
- **Features**: Lists key features of the browser and known issues.
- **Contributing**: Encourages contributions and provides guidance on reporting bugs or suggesting improvements.
- **License**: Specifies the project's licensing information.

