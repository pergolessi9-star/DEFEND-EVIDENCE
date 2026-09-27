#!/usr/bin/env python3
"""Compatibility entry point for the conservative audit scorer.

The original v1 scorer could report PASS without independently checking
claims, state changes or rollback. It is intentionally unavailable here.
"""
from audit_score import main

if __name__ == "__main__":
    main()
