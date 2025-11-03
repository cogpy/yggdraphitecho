"""
Comprehensive Test Suite for Deep Tree Echo FastAPI Endpoints
Tests all functionality including SSR, batch processing, streaming, and engine integration
"""
import pytest
import httpx
from fastapi.testclient import TestClient
from aphrodite.endpoints.deep_tree_echo.app_factory import create_app
from aphrodite.endpoints.deep_tree_echo.config import DTESNConfig


@pytest.fixture
def test_config():
    """Create test configuration"""
    return DTESNConfig(
        max_membrane_depth=4,
        esn_reservoir_size=256,
        enable_caching=True,
        enable_performance_monitoring=True,
        cache_ttl_seconds=60
    )


@pytest.fixture
def test_app(test_config):
    """Create test FastAPI application"""
    return create_app(config=test_config)


@pytest.fixture
def client(test_app):
    """Create test client"""
    return TestClient(test_app)


class TestHealthAndStatus:
    """Test health check and status endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """Test root service information endpoint"""
        response = client.get("/deep_tree_echo/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "Deep Tree Echo System Network"
    
    def test_status_endpoint(self, client):
        """Test detailed status endpoint"""
        response = client.get("/deep_tree_echo/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "config" in data
        assert "server_rendered" in data


class TestDTESNProcessing:
    """Test DTESN processing endpoints"""
    
    def test_basic_process(self, client):
        """Test basic DTESN processing"""
        response = client.post("/deep_tree_echo/process", json={
            "input_data": "Test input for DTESN processing",
            "membrane_depth": 3,
            "esn_size": 128,
            "output_format": "json"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "result" in data
        assert "processing_time_ms" in data
        assert data["server_rendered"] is True
    
    def test_process_with_validation(self, client):
        """Test input validation"""
        # Test invalid membrane depth
        response = client.post("/deep_tree_echo/process", json={
            "input_data": "Test",
            "membrane_depth": 100,  # Too high
            "esn_size": 128
        })
        assert response.status_code in [400, 422]
        
        # Test invalid ESN size
        response = client.post("/deep_tree_echo/process", json={
            "input_data": "Test",
            "membrane_depth": 3,
            "esn_size": 10000  # Too high
        })
        assert response.status_code in [400, 422]
    
    def test_process_with_performance_metrics(self, client):
        """Test that performance metrics are included"""
        response = client.post("/deep_tree_echo/process", json={
            "input_data": "Performance test input",
            "membrane_depth": 2,
            "esn_size": 64
        })
        assert response.status_code == 200
        data = response.json()
        assert "performance_metrics" in data
        metrics = data["performance_metrics"]
        assert "total_processing_time_ms" in metrics
        assert "dtesn_processing_time_ms" in metrics


class TestBatchProcessing:
    """Test batch processing capabilities"""
    
    def test_batch_process_parallel(self, client):
        """Test parallel batch processing"""
        response = client.post("/deep_tree_echo/batch_process", json={
            "inputs": ["input1", "input2", "input3"],
            "membrane_depth": 2,
            "esn_size": 64,
            "parallel_processing": True,
            "max_batch_size": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "results" in data
        assert len(data["results"]) == 3
        assert data["successful_count"] == 3
        assert data["failed_count"] == 0
    
    def test_batch_process_sequential(self, client):
        """Test sequential batch processing"""
        response = client.post("/deep_tree_echo/batch_process", json={
            "inputs": ["input1", "input2"],
            "membrane_depth": 2,
            "esn_size": 64,
            "parallel_processing": False
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["results"]) == 2
    
    def test_batch_size_limit(self, client):
        """Test batch size validation"""
        # Create too many inputs
        large_batch = [f"input{i}" for i in range(150)]
        response = client.post("/deep_tree_echo/batch_process", json={
            "inputs": large_batch,
            "membrane_depth": 2,
            "esn_size": 64
        })
        # Should either reject or truncate
        assert response.status_code in [200, 400, 422]


class TestStreamingProcessing:
    """Test streaming capabilities"""
    
    def test_stream_process(self, client):
        """Test streaming processing endpoint"""
        response = client.post("/deep_tree_echo/stream_process", json={
            "input_data": "Streaming test input",
            "membrane_depth": 2,
            "esn_size": 64
        })
        # Streaming should return 200
        assert response.status_code == 200
        # Check content type for SSE
        content_type = response.headers.get("content-type", "")
        assert "text/event-stream" in content_type or "application/json" in content_type


class TestInformationEndpoints:
    """Test information and monitoring endpoints"""
    
    def test_membrane_info(self, client):
        """Test membrane information endpoint"""
        response = client.get("/deep_tree_echo/membrane_info")
        assert response.status_code == 200
        data = response.json()
        assert "membrane_system" in data
        assert "max_depth" in data
    
    def test_esn_state(self, client):
        """Test ESN state endpoint"""
        response = client.get("/deep_tree_echo/esn_state")
        assert response.status_code == 200
        data = response.json()
        assert "esn_system" in data
        assert "reservoir_size" in data
    
    def test_engine_integration(self, client):
        """Test engine integration status endpoint"""
        response = client.get("/deep_tree_echo/engine_integration")
        assert response.status_code == 200
        data = response.json()
        assert "engine_available" in data
        assert "integration_capabilities" in data
    
    def test_performance_metrics(self, client):
        """Test performance metrics endpoint"""
        response = client.get("/deep_tree_echo/performance_metrics")
        assert response.status_code == 200
        data = response.json()
        assert "service_metrics" in data
        assert "dtesn_performance" in data


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_empty_input(self, client):
        """Test handling of empty input"""
        response = client.post("/deep_tree_echo/process", json={
            "input_data": "",
            "membrane_depth": 2,
            "esn_size": 64
        })
        # Should handle gracefully
        assert response.status_code in [200, 400, 422]
    
    def test_missing_required_fields(self, client):
        """Test missing required fields"""
        response = client.post("/deep_tree_echo/process", json={
            "membrane_depth": 2
            # Missing input_data
        })
        assert response.status_code == 422
    
    def test_invalid_json(self, client):
        """Test invalid JSON handling"""
        response = client.post(
            "/deep_tree_echo/process",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestServerSideRendering:
    """Test server-side rendering capabilities"""
    
    def test_ssr_flag_in_response(self, client):
        """Test that server_rendered flag is present"""
        response = client.post("/deep_tree_echo/process", json={
            "input_data": "SSR test",
            "membrane_depth": 2,
            "esn_size": 64
        })
        assert response.status_code == 200
        data = response.json()
        assert "server_rendered" in data
        assert data["server_rendered"] is True
    
    def test_no_client_dependencies(self, client):
        """Test that responses don't require client-side processing"""
        response = client.post("/deep_tree_echo/process", json={
            "input_data": "Complete server-side processing",
            "membrane_depth": 2,
            "esn_size": 64
        })
        assert response.status_code == 200
        data = response.json()
        # Result should be complete, not requiring client processing
        assert "result" in data
        assert data["result"] is not None


class TestConfiguration:
    """Test configuration management"""
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = DTESNConfig(
            max_membrane_depth=8,
            esn_reservoir_size=512,
            enable_caching=False
        )
        app = create_app(config=config)
        client = TestClient(app)
        
        response = client.get("/deep_tree_echo/status")
        assert response.status_code == 200
        data = response.json()
        assert data["config"]["max_membrane_depth"] == 8
        assert data["config"]["esn_reservoir_size"] == 512


class TestIntegration:
    """Integration tests for complete workflows"""
    
    def test_complete_workflow(self, client):
        """Test complete processing workflow"""
        # 1. Check health
        health = client.get("/health")
        assert health.status_code == 200
        
        # 2. Check status
        status = client.get("/deep_tree_echo/status")
        assert status.status_code == 200
        
        # 3. Process single input
        process = client.post("/deep_tree_echo/process", json={
            "input_data": "Integration test",
            "membrane_depth": 3,
            "esn_size": 128
        })
        assert process.status_code == 200
        
        # 4. Check performance metrics
        metrics = client.get("/deep_tree_echo/performance_metrics")
        assert metrics.status_code == 200
    
    def test_batch_workflow(self, client):
        """Test batch processing workflow"""
        # Process batch
        batch = client.post("/deep_tree_echo/batch_process", json={
            "inputs": ["test1", "test2", "test3"],
            "membrane_depth": 2,
            "esn_size": 64,
            "parallel_processing": True
        })
        assert batch.status_code == 200
        data = batch.json()
        
        # Verify all processed
        assert data["successful_count"] == 3
        assert len(data["results"]) == 3
        
        # Each result should have proper structure
        for result in data["results"]:
            assert "status" in result
            assert "result" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
