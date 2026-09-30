# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end data and agentic analytics pipeline that converts reseller order data into **validated business metrics, MoM growth alerts, reliable stakeholder narratives, and human-approved notification drafts**.

The system is designed around a simple principle:

> **Bad data should not produce business decisions.**

---

## 1. Problem Statement

Reseller performance data is generated continuously, but identifying meaningful category-level changes requires multiple steps:

- Aggregate raw orders into business metrics
- Validate incoming data
- Calculate month-over-month (MoM) growth
- Identify significant movements
- Prioritize the most important alerts
- Generate a concise business explanation
- Prevent unsupported claims
- Keep sensitive reseller information masked
- Require human approval before communication

This project implements that workflow as a modular pipeline.

---

## 2. Solution

```text
                    RAW DATA
                       │
                       ▼
              ┌─────────────────┐
              │   SQL Engine    │
              │ Revenue / AOV   │
              │ Region / Orders │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Python Guardrail│
              │   Validation    │
              └────────┬────────┘
                       │
                ┌──────┴──────┐
                │             │
             INVALID         VALID
                │             │
                ▼             ▼
           HARD STOP      MoM Growth
                              │
                              ▼
                       8% Business Rule
                              │
                 ┌────────────┼────────────┐
                 │            │            │
               Flagged     Not Flagged   Exact 8%
                 │                         │
                 ▼                         ▼
             Rank by                   Escalation
             |MoM %|                   (No Draft)
                 │
                 ▼
             Top 3 Alerts
                 │
                 ▼
        Narrative Generation
                 │
                 ▼
         Human Approval Gate
                 │
                 ▼
          Structured JSON
