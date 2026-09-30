# Agent Specification — Meesho Reseller Growth & Alert Intelligence Pipeline

## 1. Goal

Keep category managers informed of any category whose month-over-month
revenue movement exceeds the 8% threshold, while requiring human approval
before any drafted message is considered sent.

The agent does not automatically send messages.

Its responsibility is to validate the incoming revenue feed, calculate
verified month-over-month growth, identify flagged categories, draft
stakeholder-ready notifications, and hold those drafts for human approval.

---

## 2. Tools

The agent uses the following existing project functions:

### Part 2 — Python Guardrail & Growth Engine

- `validate_feed(csv_path)`
  - Validates the monthly revenue feed.
  - Returns validation status and validation errors.

- `mom_growth(previous, current)`
  - Calculates the verified month-over-month percentage.

- `is_flagged(mom_pct, threshold=8.0)`
  - Applies the 8% business rule.
  - Returns:
    - `flagged`
    - `not_flagged`
    - `escalate_exact_boundary`

These functions are imported from
`part2_engine/growth_engine.py` and are reused without re-implementing
their logic.

### Part 3 — Narrative Template

The agent uses the Part 3 prompt-pack structure to create a stakeholder
draft using:

- Context
- Insight
- Implication

The draft uses verified values from the pipeline and does not invent
numbers or causes.

---

## 3. Memory / State

The agent requires the previous month's revenue for each category.

This previous-month revenue is used as the baseline for calculating
month-over-month growth for the current monthly feed.

For example:

- Previous month: April
- Current month: May
- Previous revenue for Ethnic Wear: 104520.77
- Current revenue for Ethnic Wear: 185107.61

The agent uses these values to calculate the verified MoM percentage.

The current monthly feed becomes the input for the next monthly comparison.

---

## 4. Planner

The agent follows this ordered workflow:

1. Load the monthly revenue feed.

2. Run `validate_feed()` on the current feed.

3. If the feed is invalid:

   - Stop immediately.
   - Report the validation errors.
   - Do not calculate MoM.
   - Do not flag categories.
   - Do not suppress categories.
   - Do not draft messages.

4. If the feed is valid:

   - Compute `mom_growth()` for every category against the previous month.

5. Run `is_flagged()` on every category using the 8% threshold.

6. Process the results:

   - Categories returning `flagged` are collected for further processing.
   - Categories returning `escalate_exact_boundary` are added to
     `escalated_categories`.
   - Exact-boundary categories do not receive a narrative draft.
   - Categories returning `not_flagged` do not receive a narrative draft.

7. Process flagged categories:

   - Sort flagged categories by absolute MoM percentage in descending order.
   - Draft stakeholder-ready messages for at most the top 3 flagged categories.
   - Preserve the exact verified MoM value in each draft.
   - Use the Part 3 Context → Insight → Implication structure.
   - Flagged categories beyond the top-3 drafting cap are added to
     `suppressed_categories` for manual review.
   - Suppressed categories do not receive a draft message.

8. Hold all drafted messages for human approval.

   - No message is automatically sent.
   - No email, SMTP, API, or messaging operation is performed.
   - The human reviewer must inspect the draft before deciding whether it
     should be sent.

9. Return one structured JSON result containing:

   - `run_month`
   - `validation_status`
   - `validation_errors`
   - `flagged_categories`
   - `suppressed_categories`
   - `escalated_categories`
   - `action_taken`

   Drafted messages are included inside the applicable objects in
   `flagged_categories`.

---

## 5. Feedback Loop

Human approval is required before any drafted message is considered sent.

The agent therefore stops at:

`drafted_and_held_for_approval`

It does not perform real email, SMTP, API, or message-sending operations.

The human reviewer can inspect the drafted message before deciding
whether it should be sent.

---

## 6. Guardrails

### Input Guardrail

The incoming monthly revenue feed must pass `validate_feed()` before
any MoM calculation or category flagging occurs.

If validation fails, the agent performs a hard stop.

### Action Guardrail

The agent never sends messages automatically.

All drafted messages remain held for human approval.

### Output Guardrail

The final result must follow the required structured JSON schema.

The output must contain verified values only.

The agent must not invent numerical values, causes, or unsupported claims.

---

## 7. Success Condition

A successful run requires:

- The input feed is valid.
- MoM is calculated for all categories.
- The 8% flag rule is applied.
- Flagged categories are sorted by absolute MoM percentage.
- At most the top 3 flagged categories receive stakeholder-ready drafts.
- Flagged categories beyond the top-3 cap are placed in
  `suppressed_categories` for manual review.
- Exact 8% boundary categories are placed in
  `escalated_categories` without a draft.
- Non-flagged categories do not receive drafts.
- No message is automatically sent.
- The final result follows the required JSON structure.

---

## 8. Error / Hard-Stop Condition

If `validate_feed()` returns invalid:

- `validation_status` is `"invalid"`.
- `action_taken` is `"hard_stop"`.
- `validation_errors` contains the validation errors.
- `flagged_categories` is empty.
- `suppressed_categories` is empty.
- `escalated_categories` is empty.
- No MoM calculation is attempted.
- No narrative drafts are created.
- No message is sent.

---

## 9. Given–When–Then Specifications

### Scenario 1 — Valid feed with flagged category

**Given:**

A valid monthly revenue feed is provided and a category's MoM percentage
is greater than 8% in absolute value.

**When:**

The agent validates the feed, calculates MoM, and applies `is_flagged()`.

**Then:**

The category is included in `flagged_categories` and a stakeholder-ready
draft is created and held for human approval.

---

### Scenario 2 — Exact 8% boundary

**Given:**

A valid feed produces an MoM value of exactly 8.0%.

**When:**

The agent applies `is_flagged()` to the category.

**Then:**

The category is assigned `escalate_exact_boundary` and is included in
`escalated_categories`.

The category does not receive a narrative draft.

---

### Scenario 3 — Valid feed with non-flagged category

**Given:**

A valid monthly revenue feed produces an absolute MoM percentage below
8% for a category.

**When:**

The agent applies `is_flagged()`.

**Then:**

The category is assigned `not_flagged` and does not receive a draft.

It is not included in `flagged_categories` or `escalated_categories`.

---

### Scenario 4 — Invalid feed

**Given:**

The current monthly revenue feed contains validation errors.

**When:**

The agent runs `validate_feed()`.

**Then:**

The agent performs a hard stop, reports the validation errors, and does
not calculate MoM, flag categories, suppress categories, or draft messages.