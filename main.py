import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, pyqtSlot, QTimer

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser_app = parent

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if url.scheme() == 'sigma':
            self.browser_app.handle_sigma_url(url.toString())
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)

class BrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SigmaNet Browser")
        
        # Create widgets
        self.url_entry = QLineEdit(self)
        self.url_entry.setPlaceholderText("Enter sigma:// URL")
        self.fetch_button = QPushButton("Fetch", self)
        self.web_view = QWebEngineView(self)
        self.web_view.setPage(CustomWebEnginePage(self))
        
        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.url_entry)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.web_view)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Connect signals
        self.fetch_button.clicked.connect(self.fetch_html)
        self.web_view.urlChanged.connect(self.update_url_bar)
        
        # DNS server address
        self.dns_server = ('147.185.221.20', 9302)
        
        # Timer to periodically check the URL
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_and_fix_url)
        self.timer.start(750)  # 750 milliseconds

    def resolve_dns(self, domain):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.dns_server)
                s.sendall(domain.encode())
                ip = s.recv(1024).decode().strip()
                return ip
        except Exception as e:
            print(f"Failed to resolve domain {domain}: {str(e)}")
            return None
    
    def fetch_html(self):
        url = self.url_entry.text().strip()
        self.handle_sigma_url(url)
    
    @pyqtSlot(QUrl)
    def update_url_bar(self, qurl):
        url = qurl.toString()
        if url.startswith("http://"):
            url = url.replace("http://", "sigma://", 1)
        self.url_entry.setText(url)
    
    @pyqtSlot(str)
    def handle_sigma_url(self, url):
        if url.startswith('sigma://'):
            url = url[len('sigma://'):]  # Remove sigma:// prefix
            
            # Parse URL to extract domain and optional path
            parts = url.split('/')
            domain_port = parts[0]
            domain, port = self.extract_domain_and_port(domain_port)
            
            # Extract file path
            file_path = '/'.join(parts[1:])
            
            # Resolve domain to IP using DNS server
            ip = self.resolve_dns(domain)
            if ip:
                try:
                    # Connect to the domain IP and port with a timeout of 10 seconds
                    with socket.create_connection((ip, port), timeout=10) as s:
                        # Construct HTTP GET request for the specific file
                        request = f"GET /{file_path} HTTP/1.1\r\nHost: {domain}\r\n\r\n"
                        s.sendall(request.encode())
                        data = s.recv(4096)
                        
                        # Decode response headers and body
                        response = data.decode(errors='ignore')
                        headers, body = response.split('\r\n\r\n', 1)
                        
                        # Load HTML content into QWebEngineView
                        self.web_view.setHtml(body, QUrl(f"http://{domain}"))
                        
                except socket.timeout:
                    print("Connection timed out. Please try again later.")
                except Exception as e:
                    print(f"Failed to fetch URL: {str(e)}")
        
        else:
            print("Invalid URL. URL must start with sigma://")
    
    def extract_domain_and_port(self, domain_port):
        # Extract domain and port from domain:port string
        if ':' in domain_port:
            domain, port = domain_port.split(':')
            port = int(port)
        else:
            domain = domain_port
            port = 24364  # Default SigmaNet port
        
        return domain, port

    def check_and_fix_url(self):
        current_url = self.url_entry.text().strip()
        if current_url.startswith('http://'):
            fixed_url = current_url.replace('http://', 'sigma://', 1)
            self.url_entry.setText(fixed_url)
        elif not current_url.startswith('sigma://'):
            self.url_entry.setText(f'sigma://{current_url}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = BrowserApp()
    browser.show()
    sys.exit(app.exec_())

