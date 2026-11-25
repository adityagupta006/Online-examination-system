# Test Cases and Results

**67 test cases - 60 passed, 7 failed.**
Executed by `tests/test_exam.py` against the unmodified application. Failures are genuine defects, see [DEFECTS.md](DEFECTS.md).

## Login

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC01 | Negative | Login with both fields empty | username='', password='' | Error: Please enter username and password. | Please enter username and password. | ✅ Pass |
| TC02 | Negative | Login with empty password | student1 / '' | Error: Please enter username and password. | Please enter username and password. | ✅ Pass |
| TC03 | Negative | Whitespace-only username | '   ' / abc | Error: Please enter username and password. | Please enter username and password. | ✅ Pass |
| TC04 | Functional | Unknown username triggers 'Save account' dialog | student1 / Pass@123 (new) | Dialog 'Save this account?' shown | No account found for "student1". Do you want to save it and log in? | ✅ Pass |
| TC05 | Functional | Choose 'No' in save dialog | Click No | Stay on login; message says account not saved | Account was not saved. Enter a saved username to login. | ✅ Pass |
| TC06 | Functional | Choose 'Yes' saves account and logs in | Click Yes, save & login | Instructions page, greeting shows username | student1 | ✅ Pass |
| TC07 | Functional | Logout from instructions page | Click Logout | Login screen shown | Login screen | ✅ Pass |
| TC08 | Functional | Login with saved valid credentials | student1 / Pass@123 | Instructions page opens (no save dialog) | Intro visible | ✅ Pass |
| TC09 | Negative | Existing user with wrong password | student1 / WrongPass | Error: Incorrect password for this username. | Incorrect password for this username. | ✅ Pass |
| TC10 | Equivalence | Password is case-sensitive | student1 / pass@123 | Incorrect password error | Incorrect password for this username. | ✅ Pass |
| TC11 | Equivalence | Username is case-insensitive | STUDENT1 / Pass@123 | Login succeeds as 'student1' | intro=True, name=student1 | ✅ Pass |
| TC12 | Usability | Enter key in password field submits login | Press Enter | Logs in | Intro visible | ✅ Pass |
| TC13 | Usability | Enter in username moves focus to password | Press Enter in username | Focus moves to password | focus on #pw | ✅ Pass |

## Access Control

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC14 | Security | Exam cannot be started without logging in | Trigger Start while not logged in | Redirected to login; exam hidden | Login shown, exam hidden | ✅ Pass |
| TC15 | Security | Only login screen visible on first load | Open app | Intro, exam, result hidden | Only login visible | ✅ Pass |

## Instructions

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC16 | Functional | Instructions show duration, question count and auto-submit rule | Open instructions | 60 minutes, 20 MCQs, auto-submit text present | True | ✅ Pass |

## Exam

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC17 | Functional | Start exam shows Q1 of 20 and a 60:00 timer | Click Start Examination | 'Question 1 of 20', timer 60:00 | Question 1 of 20; 60:00 | ✅ Pass |
| TC18 | Functional | Exam has exactly 20 questions and 20 navigator buttons | Inspect exam | 20 questions, 20 buttons | 20 questions, 20 buttons | ✅ Pass |

## Question Bank

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC19 | Functional | All bank questions are unique | Inspect question bank | No duplicate questions | 20 unique of 20 | ✅ Pass |
| TC20 | Functional | Each question has 4 distinct options | Inspect all questions | 0 questions with duplicate options | 0 problem question(s) | ✅ Pass |
| TC21 | Functional | Correct answer is always among the displayed options | Inspect exam questions | True for all 20 | True | ✅ Pass |
| TC22 | Functional | Question order is randomised between attempts | Start two exams | Different order each time | Different | ✅ Pass |

## Navigation

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC23 | Boundary Value | Previous disabled on question 1 | Open Q1 | Previous disabled | disabled | ✅ Pass |
| TC24 | Functional | Next moves to question 2 | Click Next | Question 2 of 20 | Question 2 of 20 | ✅ Pass |
| TC25 | Boundary Value | Next disabled on question 20 | Jump to Q20 | Next disabled | disabled | ✅ Pass |
| TC26 | Functional | Navigator jumps to chosen question | Click button 10 | Question 10 of 20 | Question 10 of 20 | ✅ Pass |
| TC27 | Functional | Answer is remembered when moving away and back | Pick option B, Next, Previous | Option B still selected | selected index 1 | ✅ Pass |

## Answering

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC28 | Functional | Changing answer keeps only one option selected | Pick B, then C | Only C selected | 1 selected, index 2 | ✅ Pass |
| TC29 | Functional | Answered question is marked in navigator and progress | Answer Q1 | '1/20 answered', button turns green | 1/20 answered; class='ans cur' | ✅ Pass |
| TC30 | Functional | Clear answer removes selection | Click Clear answer | No option selected, '0/20 answered' | 0 selected; 0/20 answered | ✅ Pass |
| TC31 | Functional | Progress counter tracks several answers | Answer Q1, Q6, Q20 | '3/20 answered' | 3/20 answered | ✅ Pass |

## Timer

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC32 | Functional | Timer counts down every second | Wait 5 seconds | 59:55 | 59:55 | ✅ Pass |
| TC33 | Functional | Timer is not reset by navigating questions | Next twice, wait 5 s | 59:50 | 59:50 | ✅ Pass |
| TC34 | Boundary Value | Timer turns red at 05:00 remaining | Advance to 55 minutes | 05:00 with warning style | 05:00, low=True | ✅ Pass |
| TC35 | Boundary Value | One second before time-up exam is still running | Advance to 59:59 | 00:01, exam visible | 00:01, exam visible=True | ✅ Pass |

## Auto-submit

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC36 | Boundary Value | Exam auto-submits at 00:00 | Advance to 60:00 | Result page with 'Time is up' message | ⏰ Time is up — your exam was submitted automatically. | ✅ Pass |
| TC37 | Functional | Timer stops after submission (time taken stays fixed) | Wait 2 more minutes | Time taken unchanged: 60:00 | Time taken: 60:00 · Passing mark: 40% -> Time taken: 60:00 · Passing mark: 40% | ✅ Pass |

## Submit

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC38 | Functional | Submit asks confirmation and shows unanswered count | Click Submit with no answers | Dialog: 20 unanswered + time left | You have 20 unanswered question(s). Time left: 60:00. | ✅ Pass |
| TC39 | Functional | 'Continue exam' closes the dialog and keeps exam | Click Continue exam | Exam still visible | Exam continues | ✅ Pass |
| TC40 | Functional | Dialog says all answered when none are skipped | Answer all, Submit | 'All questions answered' | All questions answered. Time left: 59:58. | ✅ Pass |
| TC41 | Functional | Manual submit shows success message | Click Yes, submit | 'Exam submitted successfully' | ✅ Exam submitted successfully. | ✅ Pass |

## Scoring

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC42 | Boundary Value | All 20 correct | 20 correct, 0 wrong, 0 skipped | 20 / 20, PASS, 100% | 20 / 20, PASS, 100% | ✅ Pass |
| TC43 | Boundary Value | All 20 wrong | 0 correct, 20 wrong, 0 skipped | 0 / 20, FAIL, 0% | 0 / 20, FAIL, 0% | ✅ Pass |
| TC44 | Boundary Value | No answers (all skipped) | 0 correct, 0 wrong, 20 skipped | 0 / 20, FAIL, 0% | 0 / 20, FAIL, 0% | ✅ Pass |
| TC45 | Boundary Value | 8 correct = 40% (pass boundary) | 8 correct, 12 wrong, 0 skipped | 8 / 20, PASS, 40% | 8 / 20, PASS, 40% | ✅ Pass |
| TC46 | Boundary Value | 7 correct = 35% (just below pass mark) | 7 correct, 13 wrong, 0 skipped | 7 / 20, FAIL, 35% | 7 / 20, FAIL, 35% | ✅ Pass |
| TC47 | Functional | Correct + wrong + skipped always equals 20 | 5 correct, 5 wrong, 10 skipped | 5 / 5 / 10 | 5 / 5 / 10 | ✅ Pass |

## Review

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC48 | Functional | Answer review lists all 20 questions with correct status | Open review after mixed attempt | 20 items: 5 correct, 5 wrong, 10 skipped | 20 items: 5/5/10 | ✅ Pass |
| TC49 | Functional | Wrong answers display the correct answer | Inspect wrong items | Each shows 'Correct answer:' | True | ✅ Pass |
| TC50 | Functional | Time taken and pass mark shown on result | Inspect result footer | 'Time taken' and 'Passing mark: 40%' | Time taken: 00:00 · Passing mark: 40% | ✅ Pass |

## Result

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC51 | Functional | Logout from result page | Click Logout | Login screen shown | Login shown | ✅ Pass |

## Session

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC52 | Functional | logout() asks confirmation during an exam (called via console, no Logout button exists on exam screen) | logout(): Cancel, then OK | Cancel stays in exam; OK returns to login | after cancel exam=True; after OK login=True; logout button visible on exam screen=False | ✅ Pass |
| TC60 | Functional | Exam progress and remaining time survive a page reload | Answer 3, wait, reload | Exam resumes with answers and remaining time | login shown=True; new exam timer=60:00, 0/20 answered | ❌ Fail |

## Security

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC53 | Security | Password is not stored in plain text | Inspect localStorage 'examUsers' | Plain password absent (hashed) | {"student1":"Pass@123Secret"} | ❌ Fail |
| TC54 | Security | Credentials are not exposed in window.name | Inspect window.name | No credentials in window.name | examUsers={"student1":"Pass@123Secret"} | ❌ Fail |
| TC55 | Security | Answer key is not readable from the browser console | Evaluate BANK in console | Answer key inaccessible | BANK readable: correct answers exposed | ❌ Fail |
| TC56 | Security | XSS payload in username is escaped | <img src=x onerror=alert(1)> | Shown as text; no script runs | img=0, alerts=[], text=<img src=x onerror=alert(1)> | ✅ Pass |
| TC57 | Security | SQL-injection style input does not bypass login | ' OR '1'='1' -- | Treated as plain new username; no access without confirm | save dialog=True, intro=False | ✅ Pass |
| TC58 | Security | Reserved JS names like '__proto__' do not crash or bypass login | __proto__ / abc | Handled as ordinary username; no JS error | dialog=True; errors=[] | ✅ Pass |
| TC59 | Boundary Value | 1-character password is rejected by password policy | weakuser / '1' | Rejected (minimum length enforced) | Accepted - account creation offered | ❌ Fail |

## UI

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC61 | Usability | No horizontal scrolling on mobile (375 px) for login, exam, result | Viewport 375x760 | scrollWidth <= 375 on all screens | login/exam/result = [375, 375, 375] | ✅ Pass |
| TC64 | Usability | Dark mode is applied automatically | prefers-color-scheme: dark | Dark background | rgb(16, 20, 31) | ✅ Pass |

## Accessibility

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC62 | Usability | Every input is programmatically linked to a label | Inspect login form | 0 inputs without a label link | 2 input(s) without linked label | ❌ Fail |
| TC63 | Usability | Answer options can be reached with the keyboard | Check option elements | All 4 options focusable (tabindex >= 0) | 4 of 4 not focusable | ❌ Fail |

## Performance

| ID | Type | Description | Input | Expected | Actual | Status |
|---|---|---|---|---|---|---|
| TC65 | Performance | Initial page load time | Open index.html | Under 1000 ms | 90 ms | ✅ Pass |
| TC66 | Performance | Average question switch time | Switch through 20 questions | Under 50 ms per switch | 0.1 ms | ✅ Pass |
| TC67 | Performance | Result and review generated quickly | Submit full exam | Under 1000 ms | 104 ms | ✅ Pass |
