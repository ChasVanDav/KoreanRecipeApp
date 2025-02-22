# Knowledge Check 5 - Testing & Error Handling

## Unit Tests

### 3 Test Files, 5 Tests

![alt text](<../static/images/Screenshot 2025-02-14 at 1.16.29 PM.png>)

### Run:

```
coverage run -m unittest discover
```

![Unit Test Terminal Output](<../static/images/Screenshot 2025-02-14 at 12.25.47 PM.png>)

### Unit Test Results

![Unit Test Results](<../static/images/Screenshot 2025-02-14 at 12.33.26 PM.png>)

## Coverage Report

### Run:

```
 pytest --cov=app --cov-report=html tests/
```

### 1. Terminal Output

![Coverage Report - Terminal Output](<../static/images/Screenshot 2025-02-14 at 12.01.14 AM.png>)

### 2. HTML Page Output

![Coverage Report - HTML Page Output](<../static/images/Screenshot 2025-02-14 at 12.00.06 AM.png>)

## Error Handling & Logging

### Logging Error in Terminal

In this case, the website url for webscraping has a type error

![alt text](<../static/images/Screenshot 2025-02-14 at 1.04.15 PM.png>)

## Client-facing Error Handling

This is what the user sees instead of an empty page:
![alt text](<../static/images/Screenshot 2025-02-14 at 1.07.32 PM.png>)

If they try to go to an invalid path:
![alt text](<../static/images/Screenshot 2025-02-14 at 1.08.40 PM.png>)
