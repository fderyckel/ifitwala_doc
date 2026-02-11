---
title: "Programs: How We Structure Learning"
slug: program
category: Academics
doc_order: 20
summary: "Set up academic programs that group courses, define how students are assessed, and control what appears on your website."
---

# Programs: How We Structure Learning

A program is simply a container for a complete course of study. Whether you're running an IB Diploma, a national curriculum track, or a vocational certificate, the Program DocType is where you define what students will learn, how they'll be assessed, and who oversees the whole thing.

We know schools are complex. Some programs run across multiple campuses. Some have strict prerequisite chains. Some need detailed websites for prospective families, while others are internal-only. This system handles all of that without making you jump through hoops.

## What a Program Actually Contains

Think of a program as the blueprint for a student's academic journey. It holds:

- **The courses** that make up the program — what's required, what's optional, what can be repeated
- **How students are assessed** — points-based grades, pass/fail, criteria-based, or simple observations
- **Who's in charge** — program coordinators who can manage enrollments and see reports
- **What the public sees** — website pages, gallery images, self-enrollment options

<Callout type="tip">
**Did you know?** Programs can be nested. You might have a "High School" parent program containing "Grade 9," "Grade 10," and so on. This keeps things organized without creating a mess of separate records.
</Callout>

## Setting Up a Program (For Admins)

### Step 1: Create the Basic Record

Start with the essentials:

- **Program Name** — what everyone calls it (e.g., "IB Diploma Programme")
- **Abbreviation** — for reports and tight spaces (e.g., "IB-DP")
- **Parent Program** — if this belongs inside a larger structure
- **Grade Scale** — the default grading scheme (you can override per assessment)

Mark it as a **Group** if this is just a container (like "High School") that won't have its own courses directly.

### Step 2: Define How You'll Assess

Here's where you set the rules for grading. A program can use multiple assessment types:

| Type | When to use it |
|------|----------------|
| **Points** | Traditional percentage or point-based grading with weighted categories |
| **Binary** | Simple Complete/Incomplete or Pass/Fail |
| **Criteria** | Standards-based grading against specific learning criteria |
| **Observations** | Comments-only feedback without numeric scores |

<Callout type="info">
**You can combine types.** Many schools use Points for academic work but Criteria for soft skills or project-based assessments. The system handles both.
</Callout>

#### If You're Using Points

When you enable Points, you'll set up **Assessment Categories** — things like "Exams," "Coursework," "Participation." Each gets a weight that adds up to 100%.

The system tracks this for you. As you add or adjust weights, a live counter shows your running total. Go over 100% and it turns red. Hit exactly 100% and it turns green. No surprises at report card time.

<Callout type="tip">
**Inheriting from a parent:** If your program is part of a larger structure, you can copy assessment categories from the parent program with one click. Set it up once, use it everywhere.
</Callout>

### Step 3: Add Your Courses

The **Courses** table is where you list what belongs to this program:

- Which courses are required vs. optional
- What subject group each belongs to (useful for scheduling)
- Whether a course can be repeated if a student doesn't pass
- Whether it's a core program requirement or an elective

The system won't let you add the same course twice, and it only shows you active courses — no accidentally adding something you've retired.

### Step 4: Set Prerequisites (If Needed)

Some programs have entry requirements. Maybe students need to complete "Introduction to Programming" before taking "Advanced Computer Science."

You define these in the **Prerequisites** table. The system supports alternative paths — for example, students can enter the Advanced program if they've completed EITHER "Intro to Programming" OR "Fundamentals of Coding." Just give those two courses the same group number.

### Step 5: Assign Coordinators

Program Coordinators are your go-to people for this program. They can:
- See all enrollments and reports
- Manage program-specific settings
- Access coordinator-only dashboards

Add them in the **Program Coordinators** table. They don't need to be system administrators — just give them the coordinator role for this specific program.

## Publishing to Your Website

When you're ready to show this program to the world (or just to prospective families):

1. **Check "Is Published"** — this makes it visible
2. **Set a URL Slug** — the web address (e.g., "ib-diploma" becomes `yourschool.edu/ib-diploma`)
3. **Add the content** — description, aims, intro video, gallery images
4. **Decide on self-enrollment** — can families apply directly through the website?
5. **Mark it featured** — highlight it on your homepage?

<Callout type="warning">
**Archived programs can't be published.** If a program is no longer running, check the Archive box. This keeps historical records intact but prevents accidental new enrollments.
</Callout>

### Website Profiles

Each published program needs a **Program Website Profile** for each school that delivers it. This links the program to your school's branding and handles school-specific details like contact information and location.

The profile's publish status automatically syncs with the main program — no double-handling.

## How Assessment Categories Work

Assessment Categories deserve their own explanation because they trip people up.

When you use Points grading, you typically have different types of work:
- Exams (40% of the grade)
- Coursework (30%)
- Class participation (20%)
- Homework (10%)

In the system, you:
1. Create these categories in the **Assessment Category** master list
2. Add them to your program with their default weights
3. Override colors if you want different visuals on reports
4. Mark them active or inactive

The system validates that your active weights don't exceed 100%. It also prevents you from adding the same category twice — one less thing to worry about.

<Callout type="tip">
**Color coding:** Each assessment category can have a color. These appear on dashboards and reports, making it easy to spot patterns — like if a student consistently struggles with "Exams" but excels at "Coursework."
</Callout>

## Tree Structure: Keeping Organized

Programs can be nested, which is useful for:

- Grouping by level (Primary → Elementary → Upper Elementary)
- Grouping by type (Academic → Sciences → Biology)
- Separating campuses or divisions

The system uses a nested-set structure, which is just a fancy way of saying "it handles the hierarchy automatically." You set the parent; the system handles the rest.

## What Links to Programs

Programs sit at the center of your academic ecosystem. Here's what connects to them:

**Student-facing:**
- **Program Offerings** — specific instances of a program at a specific school in a specific year
- **Program Enrollments** — a student's registration in an offering
- **Student Logs** — pastoral and academic notes can reference a student's current program

**Staff-facing:**
- **Courses** — linked through the program's course list
- **Assessment Categories** — defined per program
- **Instructor Logs** — teaching activity tied to a program
- **Student Groups** — class groupings filtered by program

**Public-facing:**
- **Website Profiles** — school-specific program pages
- **Self-enrollment** — applications coming through your website

**Administrative:**
- **Reports** — enrollment trends, attendance summaries, term reports
- **Billing** — tuition invoices linked to program offerings
- **Communication** — messages and interactions tracked by program

## Common Workflows

### Setting Up a New Academic Year

1. Copy your existing program or use the same one (programs persist across years)
2. Create a new **Program Offering** for this year
3. Set capacity and seat policies
4. Open enrollment

### Updating Assessment Methods

1. Edit the program
2. Adjust your assessment categories or weights
3. The system validates totals before letting you save
4. Existing student grades aren't affected — this only applies going forward

### Archiving an Old Program

1. Check the **Archive** box
2. The program immediately unpublishes from the website
3. Existing enrollments and records remain intact
4. New offerings can't be created for archived programs

## Reports and Dashboards

Once you have programs set up, you'll want to see how they're performing:

**Enrollment Reports**
- How many students in each program by school and year
- Trends over time — are your STEM programs growing?
- Gap analysis — which students should be enrolled but aren't?

**Academic Reports**
- Student term reports include program context
- Attendance summaries by program
- Referral patterns — are certain programs seeing more pastoral issues?

**Dashboard Cards**
- Total programs at your institution
- Current enrollment by program (visual chart)
- Quick links to active offerings

> **Screenshot:** The Current Enrollment Dashboard showing program breakdown by school

---

## Technical Details (For IT)

### DocType Structure
- **Core DocType:** `Program` (`ifitwala_ed/curriculum/doctype/program/`)
- **Tree Configuration:** `is_tree = true`, `nsm_parent_field = "parent_program"`
- **Autoname:** `field:program_name`
- **Child Tables:**
  - `Program Course` — course listings with required/repeatable flags
  - `Program Assessment Category` — weighted categories with color overrides
  - `Program Coordinator` — assigned staff
  - `Program Course Prerequisite` — prerequisite rules with OR-group support
  - `Gallery Image` — website gallery

### Key Backend Logic

**Validation (`validate` method):**
- Duplicate course guard — prevents adding same course twice
- Active course guard — only "Active" status courses allowed
- Publication guard — archived programs cannot be published; published requires slug
- Assessment category default colors — auto-fetched from master if not overridden
- Assessment category validation — duplicate guard, weight bounds [0-100], points-specific rules (at least one active, sum ≤ 100)

**Server Method (`inherit_assessment_categories`):**
- Whitelisted method for copying parent program's categories
- Deduplicates by assessment category link
- Optional overwrite (default true)
- Returns counts of inherited rows

### Client Interactions

**Field Queries (`onload`):**
- Course link filtered to exclude already-picked courses, status = "Active"
- Assessment category link filtered to exclude already-selected categories

**UI Enhancements (`onload_post_render`):**
- Multiple add enabled for courses table
- "Inherit from Parent" button (blue primary) in assessment categories toolbar
- Live weight tracking badge in toolbar
  - Red if total > 100
  - Green if points enabled and total = 100
  - Grey otherwise
- Weight clamping [0-100] on all default_weight fields

**Dashboard Warnings (`refresh`):**
- Published + Archived conflict
- Published without slug
- Published without website profile

**Client Validation (`before_save`):**
- Repeats server-side validation for points mode
- Prevents save if validations fail

### Ecosystem Connections

**Downstream DocTypes:**
- `Program Offering` — concrete delivery instances
- `Program Enrollment` — student registrations
- `Program Website Profile` — school-specific public pages
- `Student Log` — pastoral notes via enrollment
- `Sales Invoice` — tuition billing via offering
- `Instructor Log`, `Student Group`, `Course Enrollment Tool`, `Program Enrollment Tool`
- `Student Applicant`, `Registration of Interest` — admissions
- `Student Attendance`, `Student Term Report`, `Referral Case` — student services

**Upstream References:**
- `Course` — via Program Course child table (active-only)
- `Assessment Category` — via Program Assessment Category child table
- `Grade Scale` — grading scheme for program
- `School`, `Academic Year` — via offerings

### Integration Points

**Enrollment Engine (`schedule/enrollment_engine.py`):**
- Validates offering courses against program catalog
- Evaluates Program Course Prerequisite rules (AND within groups, OR between groups)
- Enforces repeatability rules (Program Course `repeatable`, `max_attempts`)

**Website Integration:**
- Route auto-generated from `program_slug`
- Program Website Profile status syncs with `is_published`
- Self-enrollment portal respects `allow_self_enroll` and offering seat policies

**Permissions:**
- Tree-aware access via nested-set
- Coordinator access via `program_coordinators` child table
- School-scoped visibility via offerings and profiles

### API Endpoints
- `program_course_options` — catalog rows for offering-course selection
- `hydrate_catalog_rows` — map course names to Program Course defaults
- `inherit_assessment_categories` — copy parent categories (whitelisted)
- `compute_program_offering_defaults` — compute dates and title from abbreviation
