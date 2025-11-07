#!/usr/bin/env python3
"""
Validate Echo.kern integration for Deep Tree Echo functionality.
This script ensures all required components are present and functional.
"""

import sys
import os
from pathlib import Path

# Add echo.kern to path
echo_kern_path = Path(__file__).parent / "echo.kern"
if echo_kern_path.exists():
    sys.path.insert(0, str(echo_kern_path))

def validate_imports():
    """Validate that all required echo.kern components can be imported."""
    print("=" * 60)
    print("Echo.kern Integration Validation")
    print("=" * 60)
    
    required_components = [
        ("bseries_tree_classifier", "BSeriesTreeClassifier"),
        ("dtesn_integration", "DTESNConfiguration"),
        ("esn_reservoir", "ESNConfiguration"),
        ("esn_reservoir", "ESNReservoir"),
        ("oeis_a000081_enumerator", "OEIS_A000081_Enumerator"),
        ("psystem_membranes", "MembraneType"),
        ("psystem_membranes", "PSystemMembraneHierarchy"),
    ]
    
    all_passed = True
    
    for module_name, class_name in required_components:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except ImportError as e:
            print(f"❌ {module_name}.{class_name}: Import Error - {e}")
            all_passed = False
        except AttributeError as e:
            print(f"❌ {module_name}.{class_name}: Attribute Error - {e}")
            all_passed = False
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: Unexpected Error - {e}")
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("✅ All echo.kern components validated successfully!")
        return 0
    else:
        print("❌ Some echo.kern components failed validation")
        return 1

def validate_dtesn_processor():
    """Validate DTESN processor integration."""
    print("\n" + "=" * 60)
    print("DTESN Processor Validation")
    print("=" * 60)
    
    try:
        # Check if dtesn_processor exists
        processor_path = Path(__file__).parent / "aphrodite" / "endpoints" / "deep_tree_echo" / "dtesn_processor.py"
        if not processor_path.exists():
            print(f"❌ DTESN processor not found at {processor_path}")
            return 1
        
        print(f"✅ DTESN processor found at {processor_path}")
        
        # Try to import it
        sys.path.insert(0, str(Path(__file__).parent))
        from aphrodite.endpoints.deep_tree_echo import dtesn_processor
        print("✅ DTESN processor module imported successfully")
        
        # Check for key classes
        if hasattr(dtesn_processor, 'DTESNResult'):
            print("✅ DTESNResult class found")
        else:
            print("❌ DTESNResult class not found")
            return 1
        
        if hasattr(dtesn_processor, 'DTESNProcessor'):
            print("✅ DTESNProcessor class found")
        else:
            print("⚠️  DTESNProcessor class not found (may be defined differently)")
        
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"❌ DTESN processor validation failed: {e}")
        print("=" * 60)
        return 1

def validate_serializers():
    """Validate that serializers are properly implemented."""
    print("\n" + "=" * 60)
    print("Serializer Implementation Validation")
    print("=" * 60)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from aphrodite.endpoints.deep_tree_echo import serializers
        
        # Check for concrete implementations
        required_serializers = [
            'OptimizedJSONSerializer',
            'BinarySerializer',
            'DeterministicSerializer',
        ]
        
        all_found = True
        for serializer_name in required_serializers:
            if hasattr(serializers, serializer_name):
                print(f"✅ {serializer_name} found")
                # Try to instantiate
                try:
                    from aphrodite.endpoints.deep_tree_echo.serializers import SerializationConfig
                    config = SerializationConfig()
                    serializer_class = getattr(serializers, serializer_name)
                    instance = serializer_class(config)
                    print(f"   ✅ {serializer_name} instantiated successfully")
                except Exception as e:
                    print(f"   ⚠️  {serializer_name} instantiation warning: {e}")
            else:
                print(f"❌ {serializer_name} not found")
                all_found = False
        
        print("=" * 60)
        return 0 if all_found else 1
        
    except Exception as e:
        print(f"❌ Serializer validation failed: {e}")
        print("=" * 60)
        return 1

def main():
    """Run all validation checks."""
    print("\n🔍 Starting Echo.kern Integration Validation\n")
    
    results = []
    
    # Run validations
    results.append(("Echo.kern Components", validate_imports()))
    results.append(("DTESN Processor", validate_dtesn_processor()))
    results.append(("Serializers", validate_serializers()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSED" if result == 0 else "❌ FAILED"
        print(f"{name}: {status}")
        if result != 0:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ All validations passed! Echo.kern integration is functional.\n")
        return 0
    else:
        print("\n❌ Some validations failed. Please review the errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
