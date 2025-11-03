# Deep Tree Echo Testing and Deployment Guide

## 🎯 Overview

This guide provides comprehensive instructions for testing, running, and deploying the Deep Tree Echo FastAPI endpoints integrated with the Aphrodite Engine.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Starting the Server](#starting-the-server)
- [Interactive Demo](#interactive-demo)
- [API Documentation](#api-documentation)
- [Production Deployment](#production-deployment)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Software

- **Python**: 3.9 or higher (3.11 recommended)
- **pip**: Latest version
- **Git**: For repository management

### Required Python Packages

```bash
pip install pytest pytest-asyncio pytest-cov httpx fastapi uvicorn rich
```

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/cogpy/yggdraphitecho.git
cd yggdraphitecho
```

### 2. Install Dependencies

```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Install server dependencies
pip install fastapi uvicorn

# Install demo dependencies
pip install rich
```

### 3. Verify Installation

```bash
python3.11 -m pytest --version
python3.11 -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
```

## 🧪 Running Tests

### Comprehensive Test Suite

The repository includes a comprehensive test suite covering all Deep Tree Echo endpoints.

#### Run All Tests

```bash
cd /path/to/yggdraphitecho
python3.11 -m pytest tests/endpoints/test_deep_tree_echo_comprehensive.py -v
```

#### Run Specific Test Categories

```bash
# Health and status tests
pytest tests/endpoints/test_deep_tree_echo_comprehensive.py::TestHealthAndStatus -v

# DTESN processing tests
pytest tests/endpoints/test_deep_tree_echo_comprehensive.py::TestDTESNProcessing -v

# Batch processing tests
pytest tests/endpoints/test_deep_tree_echo_comprehensive.py::TestBatchProcessing -v

# Streaming tests
pytest tests/endpoints/test_deep_tree_echo_comprehensive.py::TestStreamingProcessing -v

# Integration tests
pytest tests/endpoints/test_deep_tree_echo_comprehensive.py::TestIntegration -v
```

#### Run with Coverage

```bash
pytest tests/endpoints/test_deep_tree_echo_comprehensive.py --cov=aphrodite.endpoints.deep_tree_echo --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Test Output Example

```
tests/endpoints/test_deep_tree_echo_comprehensive.py::TestHealthAndStatus::test_health_endpoint PASSED
tests/endpoints/test_deep_tree_echo_comprehensive.py::TestHealthAndStatus::test_root_endpoint PASSED
tests/endpoints/test_deep_tree_echo_comprehensive.py::TestDTESNProcessing::test_basic_process PASSED
tests/endpoints/test_deep_tree_echo_comprehensive.py::TestBatchProcessing::test_batch_process_parallel PASSED
...

======================== 25 passed in 5.23s ========================
```

## 🚀 Starting the Server

### Quick Start

```bash
python3.11 run_deep_tree_echo_server.py
```

### Custom Configuration

Create a custom configuration file `config.py`:

```python
from aphrodite.endpoints.deep_tree_echo.config import DTESNConfig

config = DTESNConfig(
    max_membrane_depth=8,
    esn_reservoir_size=1024,
    enable_caching=True,
    enable_performance_monitoring=True,
    cache_ttl_seconds=300
)
```

### Server Output

```
======================================================================
               Deep Tree Echo FastAPI Server
======================================================================

Configuration:
  Max Membrane Depth: 8
  ESN Reservoir Size: 1024
  Caching Enabled: True
  Performance Monitoring: True

Server starting on http://0.0.0.0:8000
API Documentation: http://0.0.0.0:8000/docs
Alternative Docs: http://0.0.0.0:8000/redoc
======================================================================

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 🎭 Interactive Demo

### Running the Demo

```bash
python3.11 demo_deep_tree_echo_interactive.py
```

### Demo Features

The interactive demo showcases:

1. **Health Check**: Verify service availability
2. **Service Information**: Display service details
3. **Basic Processing**: Single input DTESN processing
4. **Batch Processing**: Parallel processing of multiple inputs
5. **Streaming**: Real-time processing updates
6. **System Status**: Comprehensive system information
7. **Performance Metrics**: Detailed performance monitoring

### Demo Output

The demo uses the Rich library for beautiful terminal output with:
- Color-coded sections
- Formatted JSON responses
- Performance metrics tables
- Progress indicators
- Summary panels

## 📚 API Documentation

### Accessing Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/deep_tree_echo/` | GET | Service information |
| `/deep_tree_echo/process` | POST | Process single input |
| `/deep_tree_echo/batch_process` | POST | Process multiple inputs |
| `/deep_tree_echo/stream_process` | POST | Streaming processing |
| `/deep_tree_echo/status` | GET | System status |
| `/deep_tree_echo/membrane_info` | GET | Membrane system info |
| `/deep_tree_echo/esn_state` | GET | ESN state |
| `/deep_tree_echo/engine_integration` | GET | Engine integration status |
| `/deep_tree_echo/performance_metrics` | GET | Performance metrics |

### Example API Calls

#### Single Processing

```bash
curl -X POST "http://localhost:8000/deep_tree_echo/process" \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": "Test input",
    "membrane_depth": 4,
    "esn_size": 512,
    "output_format": "json"
  }'
```

#### Batch Processing

```bash
curl -X POST "http://localhost:8000/deep_tree_echo/batch_process" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": ["input1", "input2", "input3"],
    "membrane_depth": 3,
    "esn_size": 256,
    "parallel_processing": true
  }'
```

## 🏭 Production Deployment

### Docker Deployment

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Environment variables
ENV DTESN_MAX_MEMBRANE_DEPTH=8
ENV DTESN_ESN_RESERVOIR_SIZE=1024
ENV DTESN_ENABLE_CACHING=true
ENV DTESN_ENABLE_PERFORMANCE_MONITORING=true
ENV DTESN_CACHE_TTL_SECONDS=300

# Expose port
EXPOSE 8000

# Run server
CMD ["python3.11", "run_deep_tree_echo_server.py"]
```

#### Build and Run

```bash
# Build image
docker build -t deep-tree-echo:latest .

# Run container
docker run -p 8000:8000 deep-tree-echo:latest
```

### Docker Compose

```yaml
version: '3.8'

services:
  deep-tree-echo:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DTESN_MAX_MEMBRANE_DEPTH=8
      - DTESN_ESN_RESERVOIR_SIZE=1024
      - DTESN_ENABLE_CACHING=true
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deep-tree-echo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: deep-tree-echo
  template:
    metadata:
      labels:
        app: deep-tree-echo
    spec:
      containers:
      - name: deep-tree-echo
        image: deep-tree-echo:latest
        ports:
        - containerPort: 8000
        env:
        - name: DTESN_MAX_MEMBRANE_DEPTH
          value: "8"
        - name: DTESN_ESN_RESERVOIR_SIZE
          value: "1024"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
---
apiVersion: v1
kind: Service
metadata:
  name: deep-tree-echo-service
spec:
  selector:
    app: deep-tree-echo
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## ⚡ Performance Optimization

### Configuration Tuning

```python
# High-performance configuration
config = DTESNConfig(
    max_membrane_depth=8,
    esn_reservoir_size=2048,
    enable_caching=True,
    cache_ttl_seconds=600,
    enable_performance_monitoring=True
)
```

### Caching Strategy

- **Response Caching**: Enabled by default for frequently accessed data
- **TTL Configuration**: Adjust `cache_ttl_seconds` based on data freshness requirements
- **Cache Invalidation**: Automatic invalidation on configuration changes

### Horizontal Scaling

The Deep Tree Echo endpoints are designed for horizontal scaling:

1. **Stateless Design**: All endpoints are stateless
2. **Load Balancing**: Use nginx or cloud load balancers
3. **Session Affinity**: Not required
4. **Database**: No database dependencies for basic operation

### Performance Monitoring

Access real-time metrics:

```bash
curl http://localhost:8000/deep_tree_echo/performance_metrics
```

Monitor:
- Processing times
- Throughput
- Cache hit rates
- Resource utilization

## 🔍 Troubleshooting

### Common Issues

#### Server Won't Start

**Problem**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001
```

#### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'aphrodite'`

**Solution**:
```bash
# Ensure you're in the correct directory
cd /path/to/yggdraphitecho

# Install in development mode
pip install -e .
```

#### Tests Failing

**Problem**: Tests fail with connection errors

**Solution**:
```bash
# Ensure server is not running during tests
# Tests use TestClient which doesn't require a running server

# If tests still fail, check dependencies
pip install --upgrade pytest pytest-asyncio httpx fastapi
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run server
python3.11 run_deep_tree_echo_server.py
```

### Health Check

Verify server health:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Deep Tree Echo System Network",
  "timestamp": "2025-11-03T..."
}
```

## 📊 Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Test Deep Tree Echo

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-asyncio pytest-cov httpx fastapi uvicorn
    
    - name: Run tests
      run: |
        pytest tests/endpoints/test_deep_tree_echo_comprehensive.py -v --cov
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 🎓 Next Steps

1. **Explore the API**: Use the interactive documentation at `/docs`
2. **Run the Demo**: Experience all features with the interactive demo
3. **Customize Configuration**: Adjust settings for your use case
4. **Monitor Performance**: Track metrics for optimization opportunities
5. **Scale for Production**: Deploy with Docker/Kubernetes for high availability

## 📞 Support

For issues, questions, or contributions:

- **GitHub Issues**: https://github.com/cogpy/yggdraphitecho/issues
- **Documentation**: See `aphrodite/endpoints/deep_tree_echo/README.md`
- **Roadmap**: See `DEEP_TREE_ECHO_ROADMAP.md`

## 📄 License

This project is part of the Aphrodite Engine and follows the same AGPL-3.0 license.
