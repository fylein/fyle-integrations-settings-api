import os
import sys
import importlib.util

def run_test(test_case, org_id):
    # Load the test case module dynamically
    test_module_path = f"webhook_tests/test_cases/{test_case}.py"
    spec = importlib.util.spec_from_file_location("test_module", test_module_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    # Call the run_test() function from the loaded module
    test_module.run_test(org_id)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python executor.py <test_case>")
        sys.exit(1)

    test_case = sys.argv[1]
    org_id = sys.argv[2]
    run_test(test_case, org_id)
