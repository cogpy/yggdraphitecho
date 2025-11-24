#!/usr/bin/env python3
"""
Test suite for critical fixes to deep tree echo system.
Tests the fixes to dynamic_model_manager, dtesn_integration, and continuous_learning.
"""

import sys
import logging
import asyncio
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all fixed modules can be imported."""
    try:
        from aphrodite.dynamic_model_manager import DynamicModelManager, IncrementalUpdateRequest
        from aphrodite.dtesn_integration import DTESNDynamicIntegration, DTESNLearningConfig
        from aphrodite.continuous_learning import ContinuousLearningSystem, ContinuousLearningConfig
        logger.info("✅ All critical modules imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ Failed to import modules: {e}")
        return False

def test_dynamic_model_manager_structure():
    """Test that DynamicModelManager has the fixed methods."""
    try:
        from aphrodite.dynamic_model_manager import DynamicModelManager
        import inspect
        
        # Check that the critical methods exist
        assert hasattr(DynamicModelManager, '_get_model_parameters'), "Missing _get_model_parameters"
        assert hasattr(DynamicModelManager, '_apply_parameter_update'), "Missing _apply_parameter_update"
        assert hasattr(DynamicModelManager, '_get_performance_metrics'), "Missing _get_performance_metrics"
        
        # Check that _apply_parameter_update is not just 'pass'
        source = inspect.getsource(DynamicModelManager._apply_parameter_update)
        assert 'torch.no_grad()' in source, "_apply_parameter_update should use torch.no_grad()"
        assert 'param.add_' in source or 'param.mul_' in source or 'param.copy_' in source, \
            "_apply_parameter_update should actually modify parameters"
        
        # Check that _get_model_parameters doesn't return hardcoded empty dict
        source = inspect.getsource(DynamicModelManager._get_model_parameters)
        assert 'state_dict' in source, "_get_model_parameters should access state_dict"
        
        # Check that _get_performance_metrics uses real metrics
        source = inspect.getsource(DynamicModelManager._get_performance_metrics)
        assert 'torch.cuda' in source, "_get_performance_metrics should check CUDA memory"
        
        logger.info("✅ DynamicModelManager structure validated")
        return True
    except Exception as e:
        logger.error(f"❌ DynamicModelManager structure validation failed: {e}")
        return False

def test_dtesn_integration_structure():
    """Test that DTESNDynamicIntegration has the fix."""
    try:
        from aphrodite.dtesn_integration import DTESNDynamicIntegration
        import inspect
        
        # Check that enhanced_incremental_update exists
        assert hasattr(DTESNDynamicIntegration, 'enhanced_incremental_update'), \
            "Missing enhanced_incremental_update method"
        
        # Check that it doesn't use torch.randn_like for current_params
        source = inspect.getsource(DTESNDynamicIntegration.enhanced_incremental_update)
        
        # Should NOT have the mock implementation
        assert 'torch.randn_like(update_data)' not in source, \
            "Still using torch.randn_like mock implementation"
        
        # Should access dynamic_manager.get_model_parameters
        assert 'get_model_parameters' in source, \
            "Should call get_model_parameters to get actual parameters"
        
        # Should have error handling
        assert 'try:' in source and 'except' in source, \
            "Should have error handling for parameter retrieval"
        
        logger.info("✅ DTESNDynamicIntegration structure validated")
        return True
    except Exception as e:
        logger.error(f"❌ DTESNDynamicIntegration structure validation failed: {e}")
        return False

def test_continuous_learning_structure():
    """Test that ContinuousLearningSystem has the fix."""
    try:
        from aphrodite.continuous_learning import ContinuousLearningSystem
        import inspect
        
        # Check that _get_current_parameters exists
        assert hasattr(ContinuousLearningSystem, '_get_current_parameters'), \
            "Missing _get_current_parameters method"
        
        # Check that it doesn't use torch.randn
        source = inspect.getsource(ContinuousLearningSystem._get_current_parameters)
        
        # Should NOT return random tensors
        assert 'torch.randn(' not in source, \
            "Still using torch.randn for random parameters"
        
        # Should access dynamic_manager
        assert 'dynamic_manager' in source or 'get_model_parameters' in source, \
            "Should access dynamic_manager to get actual parameters"
        
        # Should use zeros as fallback instead of randn
        assert 'torch.zeros' in source, \
            "Should use zeros as fallback instead of random"
        
        logger.info("✅ ContinuousLearningSystem structure validated")
        return True
    except Exception as e:
        logger.error(f"❌ ContinuousLearningSystem structure validation failed: {e}")
        return False

def test_no_mock_patterns():
    """Test that common mock patterns have been removed."""
    try:
        from aphrodite import dynamic_model_manager, dtesn_integration, continuous_learning
        import inspect
        
        modules = [
            ('dynamic_model_manager', dynamic_model_manager),
            ('dtesn_integration', dtesn_integration),
            ('continuous_learning', continuous_learning),
        ]
        
        issues = []
        for name, module in modules:
            source = inspect.getsource(module)
            
            # Check for problematic patterns
            if 'torch.randn_like(update_data)' in source:
                issues.append(f"{name}: Still has torch.randn_like(update_data)")
            
            if '"model_state": {},' in source and 'Would contain actual model state dict' in source:
                issues.append(f"{name}: Still has empty model_state placeholder")
            
            if 'return torch.randn(' in source and 'Typical MLP dimension' in source:
                issues.append(f"{name}: Still has torch.randn with dimension comments")
        
        if issues:
            for issue in issues:
                logger.error(f"❌ {issue}")
            return False
        
        logger.info("✅ No mock patterns detected in critical files")
        return True
    except Exception as e:
        logger.error(f"❌ Mock pattern check failed: {e}")
        return False

def main():
    """Run all validation tests."""
    logger.info("=" * 70)
    logger.info("Critical Fixes Validation Test Suite")
    logger.info("=" * 70)
    logger.info("")
    
    tests = [
        ("Module Imports", test_imports),
        ("DynamicModelManager Structure", test_dynamic_model_manager_structure),
        ("DTESNDynamicIntegration Structure", test_dtesn_integration_structure),
        ("ContinuousLearningSystem Structure", test_continuous_learning_structure),
        ("No Mock Patterns", test_no_mock_patterns),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning: {test_name}")
        logger.info("-" * 70)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}", exc_info=True)
            results.append((test_name, False))
        logger.info("")
    
    logger.info("=" * 70)
    logger.info("Test Results Summary")
    logger.info("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("")
    logger.info(f"Total: {passed}/{total} tests passed")
    logger.info("=" * 70)
    
    if passed == total:
        logger.info("🎉 All validation tests passed!")
        logger.info("The critical fixes have been successfully applied.")
        return 0
    else:
        logger.warning(f"⚠️ {total - passed} test(s) failed")
        logger.warning("Some fixes may not have been applied correctly.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
