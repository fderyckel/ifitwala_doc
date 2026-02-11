---
title: "Student Logs: Keeping Track of What Matters"
slug: student-log
category: Students
doc_order: 5
summary: "A simple way to record student conversations, incidents, and follow-ups—so nothing falls through the cracks."
---

# Student Logs: Keeping Track of What Matters

We all know the feeling: you had an important conversation with a student, you meant to write it down, and now it's three days later and you can't remember the details. Or worse, a colleague asks "what happened with that incident last month?" and you're digging through emails trying to piece it together.

Student Logs fixes that. It's a simple place to record notes about students—pastoral conversations, behavioral incidents, academic concerns, whatever your school needs to track. Everything lives in one place, tied to the student record, with clear ownership when something needs to happen next.

## How It Helps

When you open a new log and select a student, the system already knows which program they're in, which academic year, which school. You don't have to fill in the same information ten times a day. The system pulls it from their enrollment record automatically.

This means:
- **Less busywork** — no duplicating information the system already has
- **Fewer errors** — the context is accurate because it comes from the official record
- **Clearer picture** — when you look back at a log, you know exactly where the student was at that moment

<Callout type="tip">
**Did you know?** The system is smart about which school to record. It checks the program offering first, then the enrollment, then the academic year—so the right campus is always attached, even in multi-school setups.
</Callout>

## Setting Up the Workflow (For Admins)

Before teachers can use this properly, someone needs to set up the categories and workflows. Here's what that looks like:

### Step 1: Decide What Kinds of Logs You Need

First, create the **Student Log Types** your school actually uses. These are entirely up to you:

- **Academic** — for learning support notes, intervention records, progress updates
- **Behavioral** — conduct incidents, positive behavior recognition
- **Pastoral** — wellbeing check-ins, counselor referrals, concerns about home life
- **Administrative** — attendance issues, uniform violations, general documentation

You can have different types for different schools if you run a multi-campus setup.

### Step 2: Set Up What Happens Next

This is where the real time-saving happens. You create **Student Log Next Steps** — templates that automatically route issues to the right person.

Each template defines:

| What you set | What it means | Example |
|-------------|-------------|---------|
| **The action** | What needs to happen | "Refer to Counselor" |
| **The role** | Who is qualified to do it | "Student Counsellor" |
| **Due date** | How quickly they should respond | "2 days" |
| **Auto-close** | When to archive old items | "30 days" |

Here's why this matters: when a teacher logs a concern and selects "Refer to Counselor," they don't have to figure out which counselor is on duty, or whether Mrs. Johnson is the right person, or whether she's even available. They just pick the action. The system finds someone with the "Student Counsellor" role, assigns the task, sets the due date, and notifies them.

<Callout type="tip">
**A practical example:** Set up a "Learning Support Review" next step that assigns to your SEN coordinator within 3 days. Now any teacher who flags a potential learning issue knows it will reach the right person quickly—without them having to remember who that person is or how to contact them.
</Callout>

### Step 3: The Teacher Experience

Once you've set this up, here's what a teacher actually does:

1. **They create a log** — select the student, choose a type (e.g., "Behavioral")
2. **They check "Requires Follow Up"** — this reveals the "Next Step" field
3. **They pick the action** — "Refer to Counselor" (not a specific person)
4. **The system handles the rest** — finds the right role, assigns a ToDo, sets the deadline

The teacher describes what happened in their own words. They don't need to know your staffing roster or who's on call. They just say what the concern is and what kind of response it needs. Your pre-defined rules handle the routing.

<Callout type="warning">
**Important:** If no one at that student's school has the required role (e.g., no "Student Counsellor" exists), the system won't let the teacher submit the log. This prevents issues from disappearing into a void—you'll know immediately if your staffing coverage has gaps.
</Callout>

## Where Teachers Can Use It

Student Logs appears wherever your staff already work:

- **From the Desk** — full access for Academic Admins and Counsellors to manage everything
- **From a Student's Profile** — teachers can add a log directly while looking at a student's record
- **From the Staff Home** — classroom teachers can log notes for whole groups without navigating away
- **Follow-up Interface** — a dedicated view for people who are assigned tasks to progress them

Students and guardians can see logs you've marked as visible to them. Keep sensitive notes internal; share the ones that help families stay informed.

<Callout type="tip">
**Did you know?** When a student views their log in the portal, the system tracks whether they've seen it. So you know if that important behavioral note actually reached the family.
</Callout>

## Voice Dictation for Busy Teachers

Sometimes you're walking between classrooms, or supervising lunch, or simply don't have a free hand to type. Student Logs supports voice dictation right in the browser (works in Chrome and Edge). Teachers can dictate their note and clean it up later—much better than forgetting to record it at all.

## Keeping Things Tidy

Old logs don't clutter your view forever. The system runs a daily check and automatically closes follow-ups that haven't been touched in the time you specified (your `auto_close_after_days` setting). Open ToDos close with them. The log gets an audit comment showing it was auto-completed, so you have a record.

Your team focuses on active concerns, not a backlog of stale items.

## Who Can See What

Not everyone should see everything. The system respects your school structure and staff assignments:

| Role | What they can see |
|------|-------------------|
| Academic Admin / Counsellor | All logs in their school branch |
| Academic Staff | Only students in their assigned Student Groups |
| Pastoral Lead | Only students in their Pastoral Groups |
| Curriculum Coordinator | Students in programs they coordinate |
| Author / Assigned person | Their own logs and anything assigned to them |

Teachers won't see students they don't teach. Staff won't see schools they don't work in. It's simple, and it prevents those awkward moments of stumbling across information you shouldn't have.

## Seeing the Patterns

When you have enough logs, the analytics dashboard helps you spot trends. How many behavioral incidents this month compared to last? Which students have multiple pastoral concerns? Are follow-ups being completed on time?

This isn't about surveillance—it's about knowing where to focus your attention and resources.

> **Screenshot:** The Student Log analytics dashboard showing filtered metrics and a simple trend chart

---

## Technical Details (For IT)

### DocType Structure
- **Core DocType:** `Student Log` (`ifitwala_ed/student_management/doctype/student_log/`)
- **Supporting DocTypes:**
  - `Student Log Type` — Categorization (Academic, Behavior, Pastoral, etc.)
  - `Student Log Next Step` — Follow-up templates with roles and auto-close settings
  - `Student Log Follow Up` — Child table tracking follow-up progress

### Key Backend Logic

**Validation (`validate` method):**
- Enforces `next_step` mandatory when `requires_follow_up` is checked
- Ensures single-assignee policy (exactly one open ToDo)
- Validates role compatibility for `follow_up_person`
- Auto-fills delivery context from Program Enrollment
- Enforces terminal "Completed" state locking

**Post-Submission (`on_submit`):**
- Marks complete immediately if no follow-up required
- Creates ToDo if assignee set but no assignment exists
- Recomputes status based on follow-up entries

**Scheduled Job (`auto_close_completed_logs`):**
- Runs daily via `hooks.py`
- Closes logs with `auto_close_after_days > 0` after inactivity
- Closes associated ToDos and appends audit comment

### API Endpoints (`ifitwala_ed.api.student_log`)
- `get_student_logs` — Paginated portal list (respects `visible_to_student`)
- `get_student_log_detail` — Single log with read-receipt tracking
- `search_students`, `search_follow_up_users`, `get_form_options`, `submit_student_log` — Vue overlay support
- `assign_follow_up` — Assignment/reassignment with role and school validation

### Permission & Visibility Predicate
`get_student_log_visibility_predicate` handles role-based access:
- System Manager / Administrator: Unrestricted
- Academic Admin / Counsellor / Learning Support: School tree branch
- Accreditation Visitor: Aggregate-only (`allow_aggregate_only=True`)
- Pastoral Lead / Academic Staff: Student Group membership
- Curriculum Coordinator: Program scope

### Vue Frontend Components
- `StudentLogCreateOverlay.vue` — Quick-create (single/group modes)
- `StudentLogFollowUpOverlay.vue` — Follow-up entry form
- `FocusRouterOverlay.vue` — Submission/review routing

### Service Layer (`src/lib/services/`)
- `studentLogService.ts` — Student search, user search, form options, submission
- `studentLogDashboardService.ts` — Dashboard data, filters, recent logs
- `focusService.ts` — Follow-up submission, outcome review

### UI Signals (`src/lib/uiSignals.ts`)
- `SIGNAL_STUDENT_LOG_INVALIDATE`
- `SIGNAL_STUDENT_LOG_DASHBOARD_INVALIDATE`
- `SIGNAL_STUDENT_LOG_RECENT_LOGS_INVALIDATE`
- `SIGNAL_STUDENT_LOG_FILTER_META_INVALIDATE`

### Client-Script Behaviors (`student_log.js`)
- Voice dictation via SpeechRecognition API
- Dynamic field visibility based on `requires_follow_up`
- Pre-submit assignment with role-filtered user selection
- Context-aware buttons (Assign, Follow Up, Complete, Reopen)
- Auto-population of academic context on student change

### Integration Points
- **ToDo System:** Open/close tracking; closing ToDo does not auto-complete log
- **Portal Read Receipts:** `Portal Read Receipt` mechanism for unread highlighting
- **Realtime Notifications:** `follow_up_ready_to_review` toast events for authors
- **School Tree:** Nested-set hierarchy for all visibility and assignment checks

### Reports
- **Student Log & Follow-up Report** (`student_logs`): Filtered views of logs and follow-up chains (roles: System Manager, Academic Admin, Academic Staff, Counselor)
