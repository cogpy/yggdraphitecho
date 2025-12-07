#!/usr/bin/env python3
"""
Test script to verify all DTESN imports work correctly after fixes.
"""
import sys
import os

# Add echo.kern to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'echo', 'kern'))

def test_direct_imports():
    """Test direct imports from echo.kern modules."""
    print("=" * 60)
    print("Testing Direct Imports from echo.kern")
    print("=" * 60)
    
    try:
        from psystem_membranes import PSystemMembraneHierarchy
        print("✅ PSystemMembraneHierarchy imported successfully")
        print(f"   Class: {PSystemMembraneHierarchy}")
    except ImportError as e:
        print(f"❌ Failed to import PSystemMembraneHierarchy: {e}")
        return False
    
    try:
        from esn_reservoir import ESNReservoir
        print("✅ ESNReservoir imported successfully")
        print(f"   Class: {ESNReservoir}")
    except ImportError as e:
        print(f"❌ Failed to import ESNReservoir: {e}")
        return False
    
    try:
        from bseries_tree_classifier import BSeriesTreeClassifier
        print("✅ BSeriesTreeClassifier imported successfully")
        print(f"   Class: {BSeriesTreeClassifier}")
    except ImportError as e:
        print(f"❌ Failed to import BSeriesTreeClassifier: {e}")
        return False
    
    try:
        from oeis_a000081_enumerator import OEIS_A000081_Enumerator
        print("✅ OEIS_A000081_Enumerator imported successfully")
        print(f"   Class: {OEIS_A000081_Enumerator}")
    except ImportError as e:
        print(f"❌ Failed to import OEIS_A000081_Enumerator: {e}")
        return False
    
    return True

def test_resource_integration():
    """Test dtesn_resource_integration imports."""
    print("\n" + "=" * 60)
    print("Testing dtesn_resource_integration.py")
    print("=" * 60)
    
    try:
        from dtesn_resource_integration import DTESNResourceIntegrator
        print("✅ DTESNResourceIntegrator imported successfully")
        print(f"   Class: {DTESNResourceIntegrator}")
        
        # Try to instantiate
        integrator = DTESNResourceIntegrator()
        print("✅ DTESNResourceIntegrator instantiated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed with dtesn_resource_integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resource_constraint_manager():
    """Test resource_constraint_manager imports."""
    print("\n" + "=" * 60)
    print("Testing resource_constraint_manager.py")
    print("=" * 60)
    
    try:
        from resource_constraint_manager import ResourceConstraintManager
        print("✅ ResourceConstraintManager imported successfully")
        print(f"   Class: {ResourceConstraintManager}")
        
        # Try to instantiate
        manager = ResourceConstraintManager()
        print("✅ ResourceConstraintManager instantiated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed with resource_constraint_manager: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("\n🔍 DTESN Import Verification Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Direct Imports", test_direct_imports()))
    results.append(("Resource Integration", test_resource_integration()))
    results.append(("Resource Constraint Manager", test_resource_constraint_manager()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests PASSED! DTESN imports are working correctly.")
        print("=" * 60)
        return 0
    else:
        print("⚠️  Some tests FAILED. Please review the errors above.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
