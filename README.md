# Online Examination System

A browser-based online exam application with an automated test suite.
Built for **Software Testing - Unit 5: Emerging Trends in Software Technologies**.

> **Live demo:** `https://<your-username>.github.io/<repository-name>/`
> (enable it under *Settings > Pages > Deploy from branch > main / root*)

## About
Students log in, read the instructions, and take a **60-minute, 20-question MCQ test on Software Testing**.
They can move freely between questions, change or clear answers, and submit manually or be auto-submitted when
the timer ends. A score and a per-question answer review appear immediately.

### Features
- Login with username and password (accounts saved in the browser)
- Exam can be started only after login
- 60-minute countdown timer (turns red at 5 minutes) with **automatic submission**
- 20 MCQs, shuffled questions and options on every attempt
- Question navigator, change / clear answers, submit-confirmation dialog
- Instant result: score, pass/fail (40% pass mark), correct / wrong / skipped, answer review
- Responsive layout (mobile friendly) and automatic dark mode

## Project structure
```
.
├── index.html            # application (screens and markup)
├── script.js             # application logic: auth, exam engine, timer, scoring
├── style.css             # responsive layout and dark mode
├── tests/
│   ├── test_exam.py      # 67 automated test cases (Playwright + Python)
│   └── results.json      # results of the latest run
├── docs/
│   ├── Online_Examination_System_Software_Testing_Assignment.pdf   # full report
│   ├── TEST_CASES.md     # all test cases in readable tables
│   ├── DEFECTS.md        # defect log with recommended fixes
│   ├── diagrams/         # architecture, use case, DFD, screen flow, data model
│   └── screenshots/      # screenshots captured from the running app
├── tools/                # scripts that regenerate the diagrams and the PDF report
├── .github/workflows/    # CI: runs the test suite on every push
└── requirements.txt
```

## Run the application
No installation is needed. Open `index.html` in a modern browser, or serve the folder:
```bash
python -m http.server 8000      # then open http://localhost:8000
```

## Run the tests
```bash
pip install -r requirements.txt
playwright install chromium
python tests/test_exam.py
```
The script drives the real UI in Chromium, uses Playwright's **fake clock** to test the 60-minute timer and
auto-submit in seconds, writes `tests/results.json` and refreshes the screenshots in `docs/screenshots/`.

## Test summary
| | |
|---|---|
| Test cases | 67 |
| Passed | 60 |
| Failed | 7 (6 distinct defects) |

Techniques: boundary value analysis, equivalence partitioning, state-transition, negative, security,
usability / accessibility and performance testing. See [docs/TEST_CASES.md](docs/TEST_CASES.md).

The application code is tested **unmodified**, so the 7 failing tests are genuine findings and are documented in
[docs/DEFECTS.md](docs/DEFECTS.md):

| ID | Severity | Finding |
|---|---|---|
| DEF-01 | High | Passwords stored in plain text (localStorage, sessionStorage, cookie, `window.name`) |
| DEF-02 | High | Answer key readable from the browser console (`BANK`) |
| DEF-03 | High | Reloading during an exam loses progress and restarts the 60:00 timer |
| DEF-04 | Medium | No password policy (1-character password accepted) |
| DEF-05 | Medium | Answer options are not keyboard accessible |
| DEF-06 | Low | Login inputs are not linked to their labels |

## Regenerate diagrams and report
```bash
python tools/diagrams.py
python tools/build_pdf.py
```

## Technologies
HTML5, CSS3, vanilla JavaScript - Python 3, Playwright (testing) - ReportLab, Matplotlib (report)

## Known limitations
Client-side prototype: accounts and the answer key live in the browser, so it is **not suitable for real
high-stakes exams** until a back end (server-side authentication, scoring and attempt tracking) is added.

## Author
`<Your name>` - `<Roll number>` - `<Course / Semester>`
