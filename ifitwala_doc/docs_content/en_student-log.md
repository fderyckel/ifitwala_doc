---
title: "Student Logs: The Pulse of Your Campus"
slug: student-log
category: Students
doc_order: 10
summary: "Centralize every pastoral note, behavioral incident, and academic follow-up in one secure, intelligent timeline—so no student falls through the cracks."
---

# Student Logs: The Pulse of Your Campus

Stop chasing paper trails. Stop digging through email threads and scattered notebooks. Student Logs transforms how your school captures, tracks, and acts on every critical moment in a student's journey.

Whether it's a pastoral check-in, a behavioral incident, or an academic intervention, every note lives in one secure, intelligent timeline. Your staff stays aligned. Your follow-ups never stall. And your students get the support they need—exactly when they need it.

## Intelligent Context Capture

Your staff shouldn't waste time manually entering academic context. When you select a student, the system automatically pulls their active Program Enrollment—filling in program, academic year, program offering, and school in a single click.

This means:
- **Zero duplication** of effort
- **Accurate reporting** across campuses and programs
- **Instant visibility** into a student's academic standing when reviewing notes

<Callout type="tip">
**Did you know?** The system resolves school context intelligently—checking Program Offering first, then Enrollment, then Academic Year—ensuring the authoritative delivery school is always recorded correctly.
</Callout>

## Streamlined Follow-Up Workflows

Critical issues demand clear ownership. When a log requires follow-up, the system enforces accountability from day one:

- **Smart Assignment:** Link a "Next Step" template to automatically set the required role and assignee
- **Role Guard:** Only users with the designated role (e.g., "Academic Staff") can be assigned—no accidental misrouting
- **Status Tracking:** Watch progress move from Open → In Progress → Completed with full audit visibility
- **ToDo Integration:** Every assignment generates an open ToDo with automatic due dates based on your school's default settings

<Callout type="info">
**Status transitions are enforced.** Once a log reaches "Completed," core fields lock—preserving the integrity of your audit trail.
</Callout>

## Multi-Channel Accessibility

Student Logs meets your staff where they work:

- **Desk View:** Full administrative control for Academic Admins and Counsellors
- **Student Dashboard Quick-Entry:** Teachers can add logs directly from a student's profile
- **Staff Home Overlay:** Classroom teachers log notes for entire rosters without leaving their workflow
- **Follow-Up Overlay:** Dedicated interface for progressing existing logs

Plus, students and guardians see only what they should. Mark logs `visible_to_student` or `visible_to_guardians` to share relevant updates while keeping sensitive notes internal.

<Callout type="tip">
**Did you know?** Students see their logs in the student portal with read-receipt tracking—so you know when important information has been acknowledged.
</Callout>

## Voice-Enabled Documentation

Teachers are busy. That's why Student Logs supports **voice dictation** directly in the browser. Using the SpeechRecognition API (Chrome/Edge), staff can dictate rich-text notes hands-free—perfect for capturing observations while moving between classes or during active supervision.

## Automated Housekeeping

Keep your database pristine without lifting a finger. The system runs a daily scheduled job that auto-completes inactive follow-ups after your configured `auto_close_after_days` threshold. Open ToDos close automatically. Audit comments log every action.

Your team focuses on **active issues**, not clutter.

## Enterprise-Grade Privacy

Staff only see students relevant to their specific role and scope:

| Role | Access Scope |
|------|--------------|
| Academic Admin / Counsellor | Full school branch via nested hierarchy |
| Academic Staff | Students in their assigned Student Groups |
| Pastoral Lead | Students in their Pastoral Student Groups |
| Curriculum Coordinator | Students in their coordinated programs |
| Author / Assignee | Their own logs and assigned items |

No configuration drift. No accidental data exposure. Privacy is **architected in**, not bolted on.

## Analytics & Reporting

Turn qualitative notes into quantitative insights. The built-in analytics dashboard aggregates logs across filters—student, log type, status, date range—so you can identify patterns, track intervention efficacy, and report to leadership with confidence.

> **Screenshot:** The Student Log analytics dashboard showing filtered metrics and trend visualization

---

## Under the Hood (For IT)

### DocType Structure
- **Core DocType:** `Student Log` (`ifitwala_ed/student_management/doctype/student_log/`)
- **Supporting DocTypes:**
  - `Student Log Type` — Categorization (Academic, Behavior, Pastoral)
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
