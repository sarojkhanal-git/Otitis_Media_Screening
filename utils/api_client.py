# API Configuration
# Switch between real API (port 8000) and mock API (port 8002) for testing
USE_MOCK_API = False  # Set to False to use real API

if USE_MOCK_API:
    API_URL = "http://127.0.0.1:8002"  # Mock API
else:
    API_URL = "http://127.0.0.1:8000"  # Real API
