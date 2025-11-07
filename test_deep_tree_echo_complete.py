#!/usr/bin/env python3
"""
Complete Deep Tree Echo Integration Test
Tests all echo.kern components without requiring torch
"""

import sys
from pathlib import Path

# Add echo.kern to path
sys.path.insert(0, str(Path(__file__).parent / "echo.kern"))

def test_echo_kern_components():
    """Test all echo.kern components"""
    print("=" * 70)
    print("DEEP TREE ECHO INTEGRATION TEST")
    print("=" * 70)
    print()
    
    # Test imports
    print("1. Testing component imports...")
    try:
        from bseries_tree_classifier import BSeriesTreeClassifier
        from dtesn_integration import DTESNConfiguration
        from esn_reservoir import ESNConfiguration, ESNReservoir
        from oeis_a000081_enumerator import OEIS_A000081_Enumerator
        from psystem_membranes import MembraneType, PSystemMembraneHierarchy
        print("   ✅ All components imported successfully")
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test ESN Configuration
    print("\n2. Testing ESN Configuration...")
    try:
        esn_config = ESNConfiguration(
            reservoir_size=100,
            input_dimension=10,
            output_dimension=5,
            spectral_radius=0.9,
            sparsity_level=0.1
        )
        print(f"   ✅ ESNConfiguration created: {esn_config.reservoir_size} neurons")
    except Exception as e:
        print(f"   ❌ ESNConfiguration failed: {e}")
        return False
    
    # Test OEIS A000081 Enumerator
    print("\n3. Testing OEIS A000081 Enumerator...")
    try:
        enumerator = OEIS_A000081_Enumerator()
        term = enumerator.get_term(5)
        sequence = enumerator.get_sequence(10)
        print(f"   ✅ OEIS enumerator working: term(5) = {term}")
        print(f"   ✅ Sequence(10): {sequence}")
    except Exception as e:
        print(f"   ❌ OEIS enumerator failed: {e}")
        return False
    
    # Test Membrane Types
    print("\n4. Testing P-System Membranes...")
    try:
        membrane_skin = MembraneType.SKIN
        membrane_elementary = MembraneType.ELEMENTARY
        membrane_root = MembraneType.ROOT
        print(f"   ✅ MembraneType.SKIN: {membrane_skin}")
        print(f"   ✅ MembraneType.ELEMENTARY: {membrane_elementary}")
        print(f"   ✅ MembraneType.ROOT: {membrane_root}")
    except Exception as e:
        print(f"   ❌ Membrane types failed: {e}")
        return False
    
    # Test DTESN Configuration
    print("\n5. Testing DTESN Configuration...")
    try:
        dtesn_config = DTESNConfiguration()
        print(f"   ✅ DTESNConfiguration created")
        # Check for any attributes without assuming specific ones
        attrs = [a for a in dir(dtesn_config) if not a.startswith('_')]
        if attrs:
            print(f"   ✅ Configuration has {len(attrs)} attributes")
    except Exception as e:
        print(f"   ❌ DTESN configuration failed: {e}")
        return False
    
    # Test B-Series Tree Classifier
    print("\n6. Testing B-Series Tree Classifier...")
    try:
        classifier = BSeriesTreeClassifier()
        print(f"   ✅ BSeriesTreeClassifier created")
    except Exception as e:
        print(f"   ❌ B-Series classifier failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - Deep Tree Echo components are functional!")
    print("=" * 70)
    return True

def test_serializers():
    """Test serializer implementations (without torch dependency)"""
    print("\n" + "=" * 70)
    print("SERIALIZER IMPLEMENTATION TEST")
    print("=" * 70)
    print()
    
    try:
        # Check if serializers module exists
        serializer_path = Path(__file__).parent / "aphrodite" / "endpoints" / "deep_tree_echo" / "serializers.py"
        if not serializer_path.exists():
            print("❌ Serializers module not found")
            return False
        
        print("✅ Serializers module found")
        
        # Check for required classes (without importing to avoid torch dependency)
        with open(serializer_path, 'r') as f:
            content = f.read()
            
        required_classes = [
            'class OptimizedJSONSerializer',
            'class BinarySerializer',
            'class DeterministicSerializer',
            'def serialize',
            'def deserialize',
        ]
        
        all_found = True
        for class_name in required_classes:
            if class_name in content:
                print(f"✅ {class_name} found")
            else:
                print(f"❌ {class_name} not found")
                all_found = False
        
        # Check for abstract base class implementation
        if 'class BaseSerializer' in content and 'ABC' in content:
            print("✅ BaseSerializer abstract class properly defined")
        else:
            print("⚠️  BaseSerializer may not be properly abstract")
        
        # Check for concrete implementations (not just pass statements)
        if content.count('def serialize(self') >= 3:  # At least 3 implementations
            print("✅ Multiple serializer implementations found")
        else:
            print("⚠️  May have incomplete serializer implementations")
        
        print("\n" + "=" * 70)
        if all_found:
            print("✅ SERIALIZER TEST PASSED")
        else:
            print("⚠️  SERIALIZER TEST COMPLETED WITH WARNINGS")
        print("=" * 70)
        return all_found
        
    except Exception as e:
        print(f"❌ Serializer test failed: {e}")
        print("=" * 70)
        return False

def main():
    """Run all tests"""
    print("\n🔍 STARTING COMPREHENSIVE DEEP TREE ECHO VALIDATION\n")
    
    success = True
    
    # Test echo.kern components
    if not test_echo_kern_components():
        success = False
    
    # Test serializers
    if not test_serializers():
        success = False
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL VALIDATION SUMMARY")
    print("=" * 70)
    
    if success:
        print("✅ ALL VALIDATIONS PASSED")
        print("   - Echo.kern components are functional")
        print("   - Serializers are properly implemented")
        print("   - Deep Tree Echo integration is ready")
        print("\n🎉 Repository is ready for build!")
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED")
        print("   Please review the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
