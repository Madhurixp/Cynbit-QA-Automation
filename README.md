# Cynbit Website – QA Automation Project

## Project Overview

This project focuses on Quality Assurance testing of the Cynbit Technologies website using Python and Selenium WebDriver.

The objective is to evaluate website functionality, navigation, page availability, contact form structure, images, and responsive behaviour.

**Website Under Test:** https://www.cynbit.in/

## Tools and Technologies

- Python 3.14.4
- Selenium WebDriver 4.54.0
- WebDriver Manager 4.1.2
- Requests
- Google Chrome
- PyCharm

## Testing Scope

The automation checks cover:

- Homepage loading and page title
- Logo and header visibility
- Navigation menu inspection
- Internal link discovery and HTTP status checks
- Navigation across internal pages
- Image URL availability
- Contact page and form field inspection
- Products and BitElevate pages
- Careers, Blog and Case Studies pages
- Footer visibility
- Responsive overflow checks for desktop, tablet and mobile viewports

## Automation Execution Summary

| Metric | Result |
|---|---:|
| Total results | 72 |
| Passed | 60 |
| Failed | 0 |
| Informational | 12 |

These results represent the checks executed by the consolidated automation script. They do not establish that every website feature is defect-free.

## Project Structure

```text
Cynbit_QA_Automation/
│
├── tests/
├── reports/
├── screenshots/
├── cynbit script.py
├── requirements.txt
├── .gitignore
└── README.md
```

*The folder structure above describes the intended organisation of the project.*

## How to Run

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the main automation script:

```bash
python "cynbit script.py"
```

## Test Report

The consolidated automation script generates:

`reports/cynbit_complete_audit_report.txt`

## Project Purpose

This project was created as part of a QA Testing Intern assessment to demonstrate practical knowledge of website testing, Python automation, Selenium WebDriver, and QA reporting.

**Author:** Madhuri