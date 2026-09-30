# Meesho Reseller Growth & Alert Intelligence Pipeline

## 1. Project Overview

This project implements a reliable data pipeline for monitoring monthly
category revenue performance for Meesho resellers.

The pipeline follows:

SQL Business Analysis
        ↓
Python Validation & Growth Engine
        ↓
Reliable AI Narrative
        ↓
Agentic Workflow
        ↓
Human Approval

The system identifies significant month-over-month revenue movements,
creates stakeholder-ready narrative drafts, and holds those drafts for
human approval.

The system does not automatically send emails or messages.

---

## 2. Objective

The pipeline is designed to:

- Analyze reseller order data using SQL.
- Calculate category-level monthly revenue.
- Identify month-over-month revenue changes.
- Validate incoming revenue feeds before calculations.
- Flag categories whose absolute MoM movement exceeds 8%.
- Handle the exact 8% boundary separately.
- Generate reliable stakeholder narratives.
- Limit automated drafting to the top 3 flagged categories.
- Suppress additional flagged categories for manual review.
- Stop immediately when input data fails validation.
- Keep all drafted messages for human approval.

---

## 3. Dataset

The dataset contains:

- 24 resellers.
- 900 orders.
- April, May, and June 2026 data.
- 4 regions.
- 5 product categories.

### Input files

```text
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db