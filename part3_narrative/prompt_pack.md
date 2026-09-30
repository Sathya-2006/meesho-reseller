# Prompt Pack — Reliable AI Narrative

## 1. Trigger

Generate a stakeholder narrative when a category's `is_flagged` result is `"flagged"`.

## 2. Input List

The narrative template requires the following verified inputs:

- `{category}` — category name
- `{previous_revenue}` — previous month's revenue
- `{current_revenue}` — current month's revenue
- `{mom_pct}` — verified month-over-month percentage
- `{month}` — current month
- `{prev_month}` — previous month

## 3. Prompt

Create a concise stakeholder-ready narrative using the following structure:

### Context

State what is being measured and the comparison period using:
`{category}`, `{prev_month}`, and `{month}`.

### Insight

State the exact revenue movement using the supplied values:
`{previous_revenue}`, `{current_revenue}`, and `{mom_pct}`.

Label this statement explicitly as **FACT**.

Do not introduce any numerical value that is not present in the supplied inputs.

### Implication

Provide a specific and actionable next step for the stakeholder.

If a possible cause or explanation is proposed but is not proven by the supplied data, label it explicitly as **HYPOTHESIS**.

Do not present a hypothesis as a confirmed fact.

### Reliability Rules

- Use only the supplied input placeholders.
- Do not invent numbers.
- Do not invent causes.
- Do not change the supplied MoM percentage.
- Preserve the direction of the movement, including positive or negative growth.
- Keep factual observations separate from hypotheses.
- Do not expose raw reseller names.

## 4. Checklist

Before accepting the generated narrative, verify:

- [ ] The category name matches `{category}`.
- [ ] The comparison months match `{prev_month}` and `{month}`.
- [ ] The revenue values match `{previous_revenue}` and `{current_revenue}`.
- [ ] The MoM percentage matches `{mom_pct}` exactly.
- [ ] Every factual claim is supported by the supplied inputs and labeled **FACT** where appropriate.
- [ ] Any proposed but unproven cause is labeled **HYPOTHESIS**.
- [ ] No raw reseller name appears in the narrative.