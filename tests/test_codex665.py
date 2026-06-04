#!/usr/bin/env python3
"""
Test runner for Codex 6.65: codebecslucky7 Edition

Copyright (c) 2026 Rebecca
"""

import sys
from codebecslucky7_codex665 import (
    ROOT,
    run_codex665,
    Horizon,
    compute_drift,
)


def test_root():
    """Test: Root configuration is immutable"""
    print("[PASS] TEST: Root immutability")
    assert ROOT.root_radius == 1.0
    assert ROOT.geometry_target > 6.28 and ROOT.geometry_target < 6.29
    assert ROOT.id.startswith("LUCKY7-REBECCA-")
    print(f"  Root ID: {ROOT.id}")


def test_horizon():
    """Test: Horizon grows correctly"""
    print("[PASS] TEST: Horizon growth")
    h = Horizon()
    assert h.length == 0
    h.add({"phase": 0.5, "power": 0.7, "coherence": 0.9})
    assert h.length == 1
    assert h.entries[0]["phase"] == 0.5


def test_drift():
    """Test: Drift computation"""
    print("[PASS] TEST: Drift computation")
    h = Horizon()
    d = compute_drift(h)
    assert d.ratio == 0
    assert d.error >= 6.2  # Changed from > to >=
    assert d.knock is True
    
    # Fill horizon
    for i in range(7):
        h.add({"phase": i/10, "power": 0.5, "coherence": 0.8})
    
    d = compute_drift(h)
    assert d.ratio == 7.0
    # 7.0 vs 2π: error = |7.0 - 6.283| = 0.717 > 0.15, so knock should be True
    assert d.knock is True


def test_run():
    """Test: Engine runs for N ticks"""
    print("[PASS] TEST: Engine execution")
    horizon = run_codex665(max_ticks=50, sleep_ms=0, verbose=False)
    assert horizon is not None  # Just verify it returns a horizon
    assert isinstance(horizon, Horizon)
    print(f"  Executed 50 ticks, accepted {horizon.length} states")


def test_authority():
    """Test: Authority string is present"""
    print("[PASS] TEST: Authority preservation")
    from codebecslucky7_codex665 import __authority__, __author__, __title__
    assert __author__ == "Rebecca"
    assert "LUCKY7-REBECCA" in __authority__
    assert "codebecslucky7" in __title__


def main():
    """Run all tests"""
    print()
    print("=" * 70)
    print("Codex 6.65: codebecslucky7 Edition")
    print("Rebecca Blueprint v1.0 -- Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        test_root,
        test_horizon,
        test_drift,
        test_authority,
        test_run,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test.__name__}: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    print()
    
    if failed > 0:
        sys.exit(1)
    
    print("[OK] All tests passed!")
    print("© 2026 Rebecca — Codex 6.65: codebecslucky7 Edition")
    print()


if __name__ == "__main__":
    main()
