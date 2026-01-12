#!/usr/bin/env python3
# .env-ronin: The Drifting Config Samurai
# Wanders through .env files, finding naming inconsistencies like a masterless samurai

import os
import sys
import re
from pathlib import Path

def find_env_files(root_dir='.'):
    """Find .env files like a ronin searching for purpose"""
    env_files = []
    for path in Path(root_dir).rglob('*.env'):
        if path.is_file():
            env_files.append(path)
    return env_files

def parse_env_file(filepath):
    """Extract variables from .env file, ignoring comments and empty lines"""
    variables = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Match VAR=value pattern
                    match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=', line)
                    if match:
                        variables[match.group(1)] = filepath
    except Exception as e:
        print(f"  ⚔️  Failed to read {filepath}: {e}")
    return variables

def main():
    print("⚔️  .env-ronin begins the drift...")
    
    env_files = find_env_files()
    if not env_files:
        print("  No .env files found. The ronin rests.")
        return
    
    print(f"  Found {len(env_files)} .env file(s):")
    for f in env_files:
        print(f"    - {f}")
    
    # Collect all variables across files
    all_vars = {}
    for env_file in env_files:
        vars_in_file = parse_env_file(env_file)
        for var_name, filepath in vars_in_file.items():
            if var_name not in all_vars:
                all_vars[var_name] = []
            all_vars[var_name].append(filepath)
    
    # Find inconsistencies (same variable with different naming)
    print("\n🔍 Scanning for inconsistent naming patterns...")
    issues_found = False
    
    # Group by lowercase version to find similar names
    normalized_groups = {}
    for var_name in all_vars.keys():
        normalized = var_name.lower().replace('_', '')
        if normalized not in normalized_groups:
            normalized_groups[normalized] = []
        normalized_groups[normalized].append(var_name)
    
    for normalized, variations in normalized_groups.items():
        if len(variations) > 1:
            issues_found = True
            print(f"\n  ⚠️  Inconsistent naming for '{normalized}':")
            for var in variations:
                files = all_vars[var]
                print(f"    - {var} (in: {', '.join(str(f) for f in files)})")
    
    if not issues_found:
        print("  ✅ All .env files speak the same language. Harmony achieved.")
    else:
        print("\n⚔️  The ronin's work is done. Choose your naming convention wisely.")

if __name__ == '__main__':
    main()