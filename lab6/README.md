# Lab 6: Code and Branch Coverage Analysis
## Elevator Dispatch System

### 1. Objective

The objective of this lab is to measure and improve the code coverage and branch coverage of the Elevator Dispatch application using Python's `pytest` and `coverage` libraries.

The testing process focuses on identifying untested statements and decision branches and designing test cases to achieve at least 90% coverage.

### 2. Project Structure

```text
lab6/
├── elevator_dispatch.py
├── test_elevator_dispatch.py
├── CodeCoverageTest_38_application.py
├── BranchCoverageTest_38_application.py
└── SCREENSHOTS/
    ├── Code_coverage.png
    └── Branch_coverage.png
```

### 3. Software Requirements

- Python 3.x
- pytest
- coverage

Install dependencies:

```bash
pip install pytest coverage
```

### 4. Code Coverage Analysis

Code coverage measures the percentage of executable statements that are executed during testing.

The test file `CodeCoverageTest_38_application.py` contains test cases covering the application's functions, including:

- Elevator direction selection.
- Elevator door operations.
- Elevator selection based on distance and availability.
- Empty request and elevator scenarios.
- Boundary conditions and priority decisions.

**Command to execute:**

```bash
coverage erase
coverage run --source=elevator_dispatch -m pytest -q CodeCoverageTest_38_application.py
coverage report -m
```

**Result: 100% code coverage**

- 19 tests passed.
- 39 statements covered.
- 0 missing statements.

### 5. Branch Coverage Analysis

Branch coverage measures whether both possible outcomes of conditional decisions are executed during testing.

The test file `BranchCoverageTest_38_application.py` contains test cases covering:

- Upward elevator movement.
- Downward elevator movement.
- Idle elevator movement.
- Emergency door handling.
- Overload conditions.
- Door obstruction handling.
- Normal door closing.
- Empty and non-empty elevator lists.
- Elevator selection and tie-breaking conditions.

**Command to execute:**

```bash
coverage erase
coverage run --branch --source=elevator_dispatch -m pytest -q BranchCoverageTest_38_application.py
coverage report -m
```

**Result: 100% branch coverage**

- 5 tests passed.
- 39 statements covered.
- 28 branches covered.
- 0 missing branches.

### 6. Git Commits

The test cases and coverage results were committed separately.

**Commit 1 – Code Coverage**

```bash
git add lab6/CodeCoverageTest_38_application.py
git commit -m "Add elevator dispatch code coverage tests"
```

**Commit 2 – Branch Coverage**

```bash
git add lab6/BranchCoverageTest_38_application.py
git add lab6/SCREENSHOTS/
git commit -m "Add elevator dispatch branch coverage tests"
```

Both commits were pushed to the personal GitHub fork.

### 7. Conclusion

The code and branch coverage analysis of the Elevator Dispatch application was successfully completed.

The code coverage test suite achieved 100% statement coverage, while the branch coverage test suite achieved 100% coverage of the measured statements and branches.

The exercise demonstrates how targeted test cases can improve testing completeness by covering normal operations, alternative decision outcomes, and edge cases.
