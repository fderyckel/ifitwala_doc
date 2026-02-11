---
title: Program
slug: program
category: Curriculum
doc_order: 20
summary: Represents an academic program containing courses, assessment categories, and publication settings for the website. Supports tree hierarchy, grading schemes, and prerequisite management.
---

# Program

## 1. Overview

The Program DocType stores a structured academic program that groups courses, defines assessment categories, and controls publication to the website. Programs can be nested in a tree (parent‑child) and include grading schemes, prerequisite rules, and coordinator assignments.

**Core Capabilities:**
- Tree‑based hierarchy (`parent_program`) for grouping programs.
- Course listing with duplicate and active‑only guards.
- Multiple assessment models (Points, Binary, Criteria, Observations) that can be combined.
- Website publication with slug‑based routing, gallery images, and self‑enrollment flags.
- Inherit assessment categories from a parent program via a dedicated UI button.
- Real‑time weight tracking and validation for active assessment categories.

**Ecosystem Links:**
- **Courses:** Linked via the `courses` child table (Program Course).
- **Assessment Categories:** Configured per program via the `assessment_categories` child table (Program Assessment Category).
- **Program Coordinators:** Assigned via the `program_coordinators` child table (Program Coordinator).
- **Grade Scale:** Single link to the grading scheme used for the program.
- **Gallery Images:** Attached via the `program_gallery_image` child table (Gallery Image).
- **Prerequisites:** Defined as alternative prerequisite paths via the `prerequisites` child table (Program Course Prerequisite).

## 2. Key Fields

| Field Label | Type | Mandatory? | Description/Notes |
| :--- | :--- | :--- | :--- |
| Program Name | Data | Yes | Unique identifier; used for autonaming. |
| Program Abbreviation | Data | No | Short form for display and reporting. |
| Parent Program | Link (Program) | No | Establishes tree hierarchy (`nsm_parent_field`). |
| Is Group | Check | No | Marks the program as a container without its own courses. |
| Archive | Check | No | Prevents publication; archived programs cannot be published. |
| Grade Scale | Link (Grade Scale) | No | Grading scheme applied to the program’s assessments. |
| Points | Check | No | Enables weighted assessment categories; total active weight must not exceed 100. |
| Binary | Check | No | Enables Complete/Incomplete grading. |
| Observations | Data | No | Stores comments‑only feedback (label: “Observations (Comments only)”). |
| Criteria | Check | No | Enables criteria‑based grading. |
| Assessment Categories | Table (Program Assessment Category) | No | Configures category‑specific weights, colors, and activity flags. |
| Program Coordinators | Table (Program Coordinator) | No | Assigns staff responsible for the program. |
| Is Published | Check | No | Makes the program visible on the website; enables dependent fields. |
| Allow Self Enroll | Check | No | Only shown when `is_published` is checked; allows students to self‑enroll. |
| Is Featured | Check | No | Only shown when `is_published` is checked; highlights the program on the website. |
| Program Image | Attach Image | No | Main image displayed on the program’s website profile. |
| URL Slug | Data | No | Required before publishing; forms the website route. |
| Route | Data (hidden) | No | Auto‑generated route; read‑only. |
| Programs Overview & Aims | Small Text | No | Short description; shown only when `is_published` is checked. |
| Intro Video | Data | No | Video embed URL; shown only when `is_published` is checked. |
| Program Overview | Text Editor | No | Detailed overview for the website. |
| Program Aims | Text Editor | No | Stated aims and objectives for the website. |
| Program Gallery Image | Table (Gallery Image) | No | Gallery of images for the website profile. |
| Courses | Table (Program Course) | No | List of courses belonging to the program. |
| Prerequisites | Table (Program Course Prerequisite) | No | Defines alternative prerequisite paths (OR groups). |
| Left, Right, Old Parent | Int (hidden) | No | Nested‑set tree structure fields; read‑only. |

**Tree Configuration:**
- `is_tree`: true
- `nsm_parent_field`: parent_program
- `autoname`: field:program_name

**Field Dependencies:**
- `allow_self_enroll` and `is_featured` depend on `is_published == 1`.
- `description` (Programs Overview & Aims) and `intro_video` depend on `is_published`.
- `program_slug` is required when `is_published` is checked.

## 3. Workflow & Logic

### Validation (`validate` method)

**Duplicate Course Guard**
- The same course cannot appear twice in the `courses` table.
- Throws: “Course {0} entered twice”.

**Active Course Guard**
- Only courses with status “Active” can be added to the program.
- Inactive courses are listed by row index, name, and current status.
- Throws: “Only Active Courses can be added:” followed by the list.

**Website Publication Guard**
- If `is_published` is checked:
  - `archive` must be unchecked (archived programs cannot be published).
  - `program_slug` must be non‑empty.
- Throws appropriate validation errors.

**Assessment Category Default Colors**
- For each row in `assessment_categories` that lacks a `color_override`, the system fetches the `assessment_category_color` from the linked Assessment Category master and populates it.
- Performed in batch to minimize database calls.

**Assessment Category Validation**
- **Duplicate Guard:** The same assessment category cannot appear twice in the table.
- **Weight Bounds:** `default_weight` must be between 0 and 100 (inclusive).
- **Points‑Specific Rules:** When `points` is checked:
  - At least one active assessment category must exist.
  - The sum of `default_weight` for active rows must not exceed 100.
- Errors list the offending rows.

### Server‑Side Method (`inherit_assessment_categories`)

**Purpose:** Copy the parent program’s assessment categories into the current program.

**Trigger:** Custom button “Inherit from Parent” in the assessment categories grid toolbar.

**Logic:**
- Requires a `parent_program` to be set.
- Fetches the parent’s `assessment_categories` rows.
- Deduplicates by assessment category link.
- If `overwrite=1` (default), the current child table is cleared before appending the inherited rows.
- Saves the document and returns counts.

**Permission:** Whitelisted; requires read/write access to the Program.

## 4. Client Interactions

### Field Queries (`onload`)

**Courses Table (`courses`)**
- Filters the `course` link field to:
  - Exclude already‑picked courses in the same table (prevents duplicates).
  - Show only courses with status “Active”.

**Assessment Categories Table (`assessment_categories`)**
- Filters the `assessment_category` link field to exclude already‑selected categories in the same table.

### UI Enhancements (`onload_post_render`)

**Multiple Add for Courses**
- Enables bulk addition of courses via a multiple‑select interface (if the grid supports `set_multiple_add`).

**Inherit from Parent Button**
- A blue primary button labeled “Inherit from Parent” is added to the assessment categories grid toolbar.
- If no parent program is set, shows a red alert.
- If existing rows are present, prompts for confirmation before overwriting.
- Calls the server‑side `inherit_assessment_categories` method, then reloads the document and refreshes the grid.

**Live Weight Tracking**
- Binds change handlers to the `default_weight`, `active`, and `assessment_category` fields in the assessment categories child table.
- Clamps `default_weight` between 0 and 100 on every change.
- Updates a live badge in the grid toolbar showing the **Active Total** percentage.
- Badge color:
  - **Red** if total > 100.
  - **Green** if `points` is enabled and total equals 100 (within floating‑point tolerance).
  - **Grey** otherwise.

### Dashboard Warnings (`refresh`)

- Checks publication consistency:
  - Archived programs cannot be published.
  - Published programs require a slug.
  - Published programs should have at least one published Website Profile.
- Warnings appear as a yellow headline in the dashboard.

### Client‑Side Validation (`before_save`)

**Points‑Only Weight Enforcement**
- Runs only when `points` is checked.
- Repeats the duplicate, negative, and >100 row‑level validations.
- Ensures at least one active category exists.
- Ensures the total active weight does not exceed 100.
- Throws client‑side validation errors that prevent saving.

### Child Table Behaviors (`Program Assessment Category`)

**Default Weight Clamping**
- Any entered value is automatically clamped to the [0, 100] range.
- The UI reflects the clamped value immediately.

**Color Auto‑Pick**
- When a new assessment category is selected and `color_override` is empty, the system fetches the master’s `assessment_category_color` and populates the override field.

**Active Total Recalculation**
- Adding, deleting, or toggling the `active` checkbox updates the live badge.

### Integration Notes

**Tree UI**
- The nested‑set tree is managed by Frappe’s `NestedSet` class (`nsm_parent_field = "parent_program"`).
- The `lft`, `rgt`, and `old_parent` fields are hidden and read‑only.

**Website Publication**
- The `route` field is auto‑generated and hidden; it is used for website routing.
- The `program_slug` is the user‑editable portion of the URL.

**Prerequisite Groups**
- The `prerequisites` table supports alternative prerequisite paths via the `group` number:
  - Rows with the same group number must be met together (AND).
  - Different group numbers represent alternatives (OR); meeting any one group is sufficient.

## 5. Ecosystem Connections

Program is the central academic structure referenced across multiple modules.

### Downstream DocTypes

| DocType | Relationship | Purpose |
| :--- | :--- | :--- |
| **Program Offering** (`schedule`) | One‑to‑many | A concrete instance of a Program delivered at a specific school, with academic‑year spine, capacity, and seat policy. |
| **Program Enrollment** (`schedule`) | One‑to‑many | Records a student’s enrollment in a Program Offering for a given academic year. |
| **Program Enrollment Request** (`schedule`) | Indirect | Request to enroll a student; references a Program Offering (and thus its Program). |
| **Program Website Profile** (`school_site`) | One‑to‑many | Website‑facing profile for a published Program, attached to a specific school. |
| **Program Course** (`curriculum`) | Child table | Lists courses that belong to the Program; defines required flags, subject groups, and repeatability. |
| **Program Assessment Category** (`curriculum`) | Child table | Configures assessment categories, default weights, and colors for the Program. |
| **Program Coordinator** (`curriculum`) | Child table | Assigns staff members as coordinators for the Program. |
| **Program Course Prerequisite** (`curriculum`) | Child table | Defines prerequisite rules for courses within the Program. |
| **Gallery Image** (`school_site`) | Child table | Gallery images displayed on the Program’s website profile. |
| **Student Log** (`students`) | Indirect | Logs can be linked to a Program via the student’s active Program Enrollment. |
| **Sales Invoice** (`accounting`) | Indirect | Invoices can reference a Program Offering (and thus its Program) for tuition billing. |

### Upstream References

| DocType | Field | Purpose |
| :--- | :--- | :--- |
| **Course** (`curriculum`) | Via `Program Course` child table | Courses are linked to Programs through the child table; only “Active” courses can be added. |
| **Assessment Category** (`assessment`) | Via `Program Assessment Category` child table | Master assessment categories are linked; their default colors can be inherited. |
| **Grade Scale** (`assessment`) | `grade_scale` field | Grading scheme applied to the Program’s assessments. |
| **School** (`school_settings`) | Via `Program Offering` / `Program Website Profile` | Programs are delivered through schools via offerings and website profiles. |
| **Academic Year** (`school_settings`) | Via `Program Offering` spine | Programs are scheduled across academic years via offerings. |

### Additional Linked DocTypes

| DocType | Module | Purpose |
| :--- | :--- | :--- |
| Instructor Log | Schedule | Logs instructor activities and notes per Program. |
| Student Group | Schedule | Groups students for instruction; can be filtered by Program. |
| Course Enrollment Tool | Schedule | Tool for enrolling students in courses; filters by Program. |
| Program Enrollment Tool | Schedule | Tool for bulk enrollment of students into a Program Offering. |
| Student Group Creation Tool | Schedule | Tool for creating Student Groups based on Program. |
| Group Message | Schedule | Send messages to groups filtered by Program. |
| Student Applicant | Admission | Applicant’s desired Program. |
| Registration of Interest | Admission | Prospective student’s Program of interest. |
| Communication Interaction | Setup | Tracks communications related to a Program. |
| Student Attendance Summary | Students | Attendance summary aggregated by Program. |
| Student Attendance | Students | Individual attendance record linked to Program. |
| Referral Case | Students | Referral case linked to a Program. |
| Student Referral | Students | Referral linked to a Program. |
| Student Term Report | Students | Term‑level academic report linked to Program. |
| Referral Intake Overview | Students | Report of referral intake filtered by Program. |

### Integration Points

- **Enrollment Engine** (`schedule/enrollment_engine.py`): Uses Program‑level prerequisites and course repeatability rules when evaluating enrollment requests.
- **Student Dashboard**: Displays the student’s current Program and courses.
- **Curriculum Coordinator Workspace**: Shows Programs they coordinate via the `program_coordinators` child table.

## 6. Publication Flow

Publishing a Program makes it visible on the public website and enables self‑enrollment.

### Prerequisites

1. **Program Slug** (`program_slug`) must be set (non‑empty).
2. **Archive** must be unchecked (archived programs cannot be published).
3. **Program Website Profile** should exist for the target school(s) and be marked “Published”.

### Steps

1. **Set `is_published = 1`**  
   - Enables dependent fields: `allow_self_enroll`, `is_featured`, `description`, `intro_video`.
   - Triggers validation that ensures `program_slug` is present and program is not archived.

2. **Create Program Website Profile**  
   - A `Program Website Profile` record links the Program to a specific School.
   - Its `status` automatically syncs with the Program’s `is_published` flag.
   - The profile includes hero image, intro text, and configurable content blocks.

3. **Website Routing**  
   - The `route` field is auto‑generated from the `program_slug`.
   - Public URL pattern: `/{program_slug}` (handled by the website router).

4. **Self‑Enrollment**  
   - If `allow_self_enroll` is checked, students can enroll via the website portal (subject to offering‑level seat policies).

### Dashboard Warnings

The Program form’s dashboard displays warnings if:
- The program is published but archived.
- The program is published but lacks a slug.
- The program is published but has no published Website Profile.

## 7. Reports & Dashboards

### Reports

| Report | Module | Description |
| :--- | :--- | :--- |
| **Enrollment Report** (`enrollment_report`) | Schedule | Aggregate enrollment counts by School, Academic Year, and Program. Supports Program‑level filtering and stacked bar charts. |
| **Enrollment Trend Report** (`enrollment_trend_report`) | Schedule | Time‑series enrollment trends across academic years, grouped by Program. |
| **Enrollment Gaps Report** (`enrollment_gaps_report`) | Schedule | Identifies gaps in student enrollment sequences, filtered by Program. |
| **Student Term Report** (`student_term_report`) | Students | Includes Program context for each student’s term‑level performance. |

### Dashboards

| Dashboard | Module | Cards/Charts Involving Program |
| :--- | :--- | :--- |
| **Current Enrollment Dashboard** (`current_enrollment_dashboard`) | Schedule | “Number of Program” card; “Current Enrollment By Program” chart. |
| **Admin Dashboard** (`admin_dashboard`) | School Settings | May include Program‑level enrollment summaries. |
| **Student Dashboard** (`student_dashboard`) | Students | Shows the student’s current Program and enrolled courses. |

### API Endpoints

- `program_course_options` – returns catalog rows for a Program, used in offering‑course selection.
- `hydrate_catalog_rows` – maps course names to Program Course defaults for offering rows.
- `inherit_assessment_categories` – copies parent program’s assessment categories (whitelisted).
- `compute_program_offering_defaults` – computes default dates and title based on Program abbreviation and organization.

## 8. Integration Points

### Enrollment Validation

- **Program Offering Course Validation**: Each course in a Program Offering must belong to the Program’s catalog (`Program Course` table) unless marked as non‑catalog with a justification.
- **Prerequisite Evaluation**: The enrollment engine (`enrollment_engine.py`) evaluates Program‑level prerequisites (`Program Course Prerequisite`) when checking course eligibility.
- **Repeatability Rules**: Program Course rows define `repeatable` and `max_attempts`; the enrollment engine enforces these limits against the student’s history.

### Assessment Configuration

- **Grade Scale**: The Program’s `grade_scale` is used as the default grading scheme for all assessments within the Program.
- **Assessment Categories**: The `assessment_categories` child table defines which categories are active, their weights (if Points enabled), and custom colors.
- **Multiple Schemes**: Programs can combine Points, Binary, Criteria, and Observations grading schemes simultaneously.

### Website Integration

- **Program Website Profile**: Each published Program can have multiple website profiles (one per school). The profile’s `status` syncs with the Program’s `is_published` flag.
- **Route Generation**: The `route` field is auto‑generated and used by the website router to serve the program’s public page.
- **Self‑Enrollment Portal**: If `allow_self_enroll` is enabled, the website portal shows an enrollment button that leads to the Program Offering’s enrollment flow.

### Permission & Visibility

- **Tree‑aware Access**: The nested‑set tree (`parent_program`) enables hierarchical navigation and filtering.
- **Coordinator Access**: Users listed in the `program_coordinators` child table gain additional permissions (e.g., view/edit rights) for that Program.
- **School‑scoped Visibility**: Program Offerings and Website Profiles are scoped to specific schools; user access is limited to their assigned school tree.

### Data Integrity

- **Active‑Course Guard**: Only courses with status “Active” can be added to a Program.
- **Duplicate Guards**: Duplicate courses and assessment categories are prevented both in the UI and server‑side validation.
- **Archive Lock**: Archived programs cannot be published; published programs cannot be archived without first unpublishing.