---
title: Student Log
slug: student-log
category: Student
doc_order: 10
summary: Tracks student-related notes, follow-ups, and pastoral care actions with configurable workflows, assignment, and visibility controls.
---

# Student Log

## 1. Ecosystem Overview

**Purpose:** The Student Log DocType stores annotated notes about students, supporting academic, pastoral, and administrative tracking. Each log can be configured to require a follow‑up action, which triggers assignment, status tracking, and eventual completion.

**Touchpoints:**
- **Desk List View:** Standard Frappe list and form views for administrative management.
- **Student Dashboard Quick‑Entry:** Accessed via the “Add Log” button on student dashboards (Vue SPA).
- **Staff Home Overlay:** Quick‑create flows for classroom groups (`StudentLogCreateOverlay.vue`).
- **Follow‑Up Overlay:** Dedicated interface for adding follow‑up entries (`StudentLogFollowUpOverlay.vue`).
- **Portal Visibility:** Students and guardians can view logs marked `visible_to_student` or `visible_to_guardians` via the student portal.
- **Analytics Dashboard:** Aggregated metrics and filterable reports (`student_log_dashboard` API).

**Dependencies:**
- **Student Log Type:** Categorizes logs (e.g., “Academic”, “Behavior”, “Pastoral”). Each type can be scoped to a specific school.
- **Student Log Next Step:** Defines the required follow‑up action, associated role, and auto‑close duration.
- **Student Log Follow Up:** Child DocType that records progress on a log’s follow‑up chain.
- **Program Enrollment:** Provides default academic context (program, academic year, program offering, school) when a student is selected.
- **School Tree:** Determines visibility and assignment boundaries via nested‑set hierarchy.

## 2. Data Structure

| Field Label | Type | Mandatory? | Logic/Notes |
| :--- | :--- | :--- | :--- |
| Student | Link (Student) | Yes | Only enabled students are selectable. |
| Student Name | Data (read‑only) | No | Fetched from the Student master. |
| Date | Date | Yes | Defaults to today. |
| Time | Time | No | Defaults to current time. |
| Log Type | Link (Student Log Type) | Yes | Determines the category of the note. |
| Author Name | Data (read‑only) | No | Fetched from the linked Employee record of the current user. |
| Academic Year | Link (Academic Year) | No | Auto‑filled from the student’s active Program Enrollment. |
| Program | Link (Program) | No | Auto‑filled from the student’s active Program Enrollment. |
| Program Offering | Link (Program Offering) | No | Auto‑filled from the student’s active Program Enrollment. |
| School | Link (School) | No | Resolved from Program Offering → Program Enrollment → Academic Year (authoritative delivery school). |
| Visible to Student | Check | No | Default `1`. When checked, the log appears in the student portal. |
| Visible to Guardians | Check | No | Default `1`. When checked, guardians can view the log. |
| Log | Text Editor | Yes | Rich‑text note body. Supports client‑side voice dictation via browser SpeechRecognition API. |
| Requires Follow Up | Check | No | When enabled, fields `next_step`, `follow_up_role`, `follow_up_person`, and `follow_up_status` become mandatory. |
| Next Step | Link (Student Log Next Step) | If follow‑up required | Defines the follow‑up action and associated role. |
| Follow‑up Role | Data | If follow‑up required | Populated from the selected Next Step’s `associated_role` (default “Academic Staff”). |
| Follow‑up User | Link (User) | If follow‑up required | Person responsible for the follow‑up. Role‑filtered and pre‑submit editable. |
| Follow‑up Status | Select (Open / In Progress / Completed) | No | Derived automatically from the presence of open ToDos and follow‑up entries. Terminal state “Completed” locks core fields. |
| Student Image | Attach Image (hidden) | No | Fetched from the Student master for UI display. |

**Key Derived Fields:**
- `follow_up_status` is computed as:
  - **Open:** Exactly one open ToDo exists and no follow‑up entries.
  - **In Progress:** At least one follow‑up entry exists (draft or submitted).
  - **Completed:** Explicitly set by author/admin or via auto‑close after inactivity.
- `school` is resolved in priority order:
  1. Program Offering’s school.
  2. Program Enrollment’s school (same academic year).
  3. Academic Year’s school.

## 3. Backend Logic

### Validation (`validate` method)
- If `requires_follow_up` is checked:
  - `next_step` is mandatory.
  - When `follow_up_person` is set pre‑submit, exactly one open ToDo is ensured for that user (single‑assignee policy).
  - Role guard: the selected `follow_up_person` must have the `follow_up_role` (from Next Step’s `associated_role`).
  - The current open assignee is mirrored back into `follow_up_person`.
- If `requires_follow_up` is unchecked:
  - `next_step`, `follow_up_person`, and `follow_up_status` are cleared.
  - Any existing open ToDos are closed.
- Delivery context (program, academic year, program offering, school) is auto‑filled from the student’s active Program Enrollment when any of those fields is missing.
- Status transitions are enforced:
  - `Completed` is terminal; fields `requires_follow_up`, `next_step`, `follow_up_role`, `follow_up_person`, `program`, `academic_year` become immutable.
  - Allowed transitions: `None` → `Open` / `In Progress`; `Open` → `In Progress` / `Completed`; `In Progress` → `Completed`.

### Post‑Submission (`on_submit` method)
- If `requires_follow_up` is unchecked, the log is immediately marked `Completed`.
- If `requires_follow_up` is checked:
  - Exactly one open assignee must exist (creates a ToDo if `follow_up_person` is set but no assignment exists).
  - `follow_up_person` is updated from the assignee.
  - Status is recomputed (Open if only a ToDo exists, In Progress if any follow‑up entries exist).

### Scheduled Job (`auto_close_completed_logs`)
- Runs daily via `hooks.py`.
- Logs with `follow_up_status = "In Progress"` and `auto_close_after_days > 0` are moved to `Completed` after the specified days of inactivity (based on `modified` timestamp).
- All open ToDos referencing those logs are closed.
- A concise audit comment is added to each auto‑completed log.

### Permission & Visibility

The visibility predicate (`get_student_log_visibility_predicate`) determines which logs a user can see based on role and context. Write, submit, and amend permissions are restricted to the author, Academic Admin, or current assignee.

| Role | Access Scope | Logic / Condition |
| :--- | :--- | :--- |
| System Manager, Administrator | Full system | Unrestricted access (admin roles). |
| Academic Admin, Counsellor, Learning Support | School Branch | Can see all logs within their school's nested tree. |
| Accreditation Visitor | Aggregate Only | Can see logs only for aggregate reporting (`allow_aggregate_only=True`); detail views are blocked. |
| Pastoral Lead | Student Group | Limited to students they explicitly instruct in active Pastoral Student Groups. |
| Academic Staff | Student Group | Limited to students they explicitly instruct in non‑pastoral Student Groups. |
| Curriculum Coordinator | Program | Can see logs for students in programs they coordinate. |
| Author / Assignee | Ownership | Always see their own logs and logs assigned to them. |

### API Endpoints (`ifitwala_ed.api.student_log`)
- `get_student_logs`: Paginated list for the student portal (respects `visible_to_student` flag).
- `get_student_log_detail`: Single log with read‑receipt tracking.
- `search_students`, `search_follow_up_users`, `get_form_options`, `submit_student_log`: Support the Vue overlay quick‑create workflow.

### Assignment & Reassignment (`assign_follow_up`)
- Can be invoked by the log author, Academic Admin, current assignee, or a user with the `follow_up_role`.
- Validates that the new assignee’s school branch includes the log’s school.
- Ensures the assignee has the required role (default “Academic Staff”).
- Closes any existing open ToDos and creates a new open ToDo with a due date based on the school’s `default_follow_up_due_in_days`.

## 4. Frontend Integration (Technical Context)

### Vue Components
- **`StudentLogCreateOverlay.vue`:** Handles quick creation of logs in “single‑student” or “group‑roster” modes. Communicates with `studentLogService.ts`.
- **`StudentLogFollowUpOverlay.vue`:** Dedicated form for adding follow‑up entries. Submits via `focusService.ts`.
- **`FocusRouterOverlay.vue`:** Routes follow‑up submission and review actions.

### Service Layer (`src/lib/services/`)
- **`studentLogService.ts`:** Encapsulates API calls for student search, follow‑up user search, form options, and log submission.
- **`studentLogDashboardService.ts`:** Fetches filter metadata, dashboard data, recent logs, and distinct student lists for analytics.
- **`focusService.ts`:** Handles follow‑up submission and outcome review.

### UI Signals (`src/lib/uiSignals.ts`)
- `SIGNAL_STUDENT_LOG_INVALIDATE`: Triggers refetch of log data.
- `SIGNAL_STUDENT_LOG_DASHBOARD_INVALIDATE`: Invalidates dashboard caches.
- `SIGNAL_STUDENT_LOG_RECENT_LOGS_INVALIDATE`: Invalidates recent‑logs lists.
- `SIGNAL_STUDENT_LOG_FILTER_META_INVALIDATE`: Invalidates filter metadata.

### Client‑Script Behaviors (`student_log.js`)
- **Voice Dictation:** Browser SpeechRecognition API integration for hands‑free note entry (Chrome/Edge only).
- **Dynamic Field Visibility:** Follow‑up fields are shown/hidden based on the `requires_follow_up` checkbox.
- **Pre‑submit Assignment:** The `follow_up_person` field is editable before submission and filtered by the role derived from the selected Next Step.
- **Custom Buttons:** Context‑aware buttons for Assign/Re‑assign, Follow Up, Complete, and Reopen appear based on user role and log status.
- **Student Change Handler:** Automatically populates program, academic year, program offering, and school from the student’s active Program Enrollment.

### Reports
- **Student Log & Follow‑up Report (`student_logs`):** Script‑based report providing filtered views of logs and their follow‑up chains. Accessible to System Manager, Academic Admin, Academic Staff, and Counselor roles.

### Integration Points
- **ToDo System:** Each follow‑up generates an open ToDo with a due date; closing ToDos does not automatically complete the log.
- **Portal Read Receipts:** Unread logs are highlighted in the student portal via the `Portal Read Receipt` mechanism.
- **Realtime Notifications:** Authors receive a toast notification when a follow‑up is ready for review (`follow_up_ready_to_review` event).
- **School‑tree Awareness:** All assignment and visibility checks respect the nested‑set school hierarchy.