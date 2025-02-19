# tests/test_basic.py
def test_environment():
    """Test that the environment is correctly set up"""
    import sys
    import os
    
    # Vérifie Python
    assert sys.version_info >= (3, 12), "Python version should be 3.12 or higher"
    
    # Vérifie les dépendances
    try:
        import nicegui
        import PyQt5
        import fastapi
    except ImportError as e:
        raise AssertionError(f"Missing dependency: {e}")
    
    # Vérifie que le PYTHONPATH est correctement configuré
    assert '/app' in sys.path, "PYTHONPATH should include /app"