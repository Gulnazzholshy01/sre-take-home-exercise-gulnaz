# Endpoint Health Monitor

#### 1. Installation
Ensure Python is installed, then install dependencies:
```python -m pip install  requests pyyaml```

#### 2. Running the Monitor
Execute the script with a YAML configuration file:
```python monitor.py samples.yaml```

## Issue Identification & Fixes

#### 1. YAML Validation
**Identified Issue:**  
- The script lacked error handling for missing or malformed YAML files.
- Running the script with an invalid YAML file caused crashes.

**Why the Fix Was Made:**  
- Added error handling to ensure the script exits gracefully when the YAML file is missing or incorrectly formatted.

---

#### 2. Default Request Method
**Identified Issue:**  
- Some endpoints did not specify an HTTP method.
- Requests failed due to missing method parameters.

**Why the Fix Was Made:**  
- Set `GET` as the default method when none is provided, ensuring requests are valid even if the method is omitted.

---

#### 3. Response Time Constraint
**Identified Issue:**  
- Some endpoints might be marked `"UP"` even though they took longer than 500ms to respond.
- This violated the requirement that responses must be fast.

**Why the Fix Was Made:**  
- Introduced a `timeout=0.5` constraint to ensure only fast responses (≤ 500ms) are considered available.

---

#### 4. Prevented Division by Zero in Availability Calculation
**Identified Issue:**  
- If an endpoint has `total = 0` checks, the percentage calculation (`up / total`) fails.

**Why the Fix Was Made:**  
- Used conditional logic to prevent division by zero, ensuring percentages remain valid.

---

#### 5. Domain Extraction Fix
**Identified Issue:**  
- If URLs include port numbers, it leads to incorrect domain-based calculations.
  
**Why the Fix Was Made:**  
- Used `urllib.parse` to extract domains while **removing ports**, ensuring proper grouping.

---

#### 6. Maintaining 15-Second Cycles
**Identified Issue:**  
- Long-running requests might push the sleep time beyond 15 seconds.
  
**Why the Fix Was Made:**  
- Used `time.sleep(max(0, 15 - elapsed_time))` to **adjust cycle timing dynamically**, preventing delays.


