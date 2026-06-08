# FoodLoop — Surplus Food Rescue & Redistribution Tracker

> Built as part of the Odoo Innovation Challenge conducted by Engineers Australia Society/UOWD Tech Club in collaboration with Odoo.

FoodLoop is a custom Odoo module that digitises the entire chain-of-custody for surplus food — from a donor logging a listing, to a charity claiming it, to a driver picking it up and delivering it, to impact metrics being recorded automatically. Built to address the UAE's AED 6 billion annual food waste crisis.

---

## The Problem

- **224 kg** of food wasted per person per year in the UAE
- **90%** of the UAE's food is imported — waste is doubly costly
- The UAE's **Ne'ma 2030** target is to halve food waste nationally
- The UAE Food Bank has delivered **70M+ meals** — but coordination is still largely manual

FoodLoop makes the coordination layer digital, auditable, and measurable.

---

## What FoodLoop Does

| Stage | Actor | Action |
|-------|-------|--------|
| **Listed** | Donor (restaurant/hotel) | Logs surplus food with items, quantities, best-before date |
| **Claimed** | Charity | Claims the listing for their beneficiaries |
| **Picked Up** | Driver | Confirms pickup; triggers chatter audit entry |
| **Delivered** | Driver | Marks delivery complete |
| **Closed** | Coordinator | Archives the listing |

Every state change is logged in Odoo's chatter with a timestamp and user. Nothing is lost.

---

## Key Features

- **Kanban board** — drag cards between stages to advance the workflow; columns always appear in workflow order (Listed → Claimed → Picked Up → Delivered → Closed)
- **Auto-reference** — every listing gets a unique `FL/0001` style reference from an `ir.sequence`
- **Workflow guards** — can't claim without a charity; can't pick up without a driver (enforced with `UserError`)
- **Impact metrics** — total meals rescued, total kg rescued, and CO₂ saved (2.5 kg CO₂ per kg rescued) computed automatically and shown as stat buttons
- **Expiry ribbon** — listings past their best-before date get a red "Expiring Soon" banner on the form and a danger badge on the kanban card
- **Priority flag** — urgent listings surface first (`_order = 'priority desc, available_from asc'`)
- **Full audit trail** — charity, driver, and state changes tracked via `mail.thread` chatter
- **14 demo listings** — covering all five stages with realistic UAE-context data (hotels, restaurants, bakeries, charities, drivers)
- **Search & filter** — by state, donor, charity, urgent, or expiring soon; group by state or donor

---

## Role Architecture

FoodLoop is designed for four user types, all using the same Odoo interface but interacting with different records:

| Role | What they do in FoodLoop |
|------|--------------------------|
| **Coordinator** | Full access; manages listings end-to-end; sees all records |
| **Donor** (restaurant/hotel) | Creates listings; fills in items and best-before; can see their own listings |
| **Charity** | Browses listed surpluses; claims them (sets `charity_id`) |
| **Driver** | Sees claimed listings assigned to them; advances to Picked Up → Delivered |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [Odoo Community 19.0](https://github.com/odoo/odoo) |
| Language | Python 3 (models), XML (views/data), CSV (security) |
| Database | PostgreSQL |
| Frontend | Odoo Web Client (OWL components, Bootstrap 5) |
| Audit | `mail.thread` + `mail.activity.mixin` |
| References | `ir.sequence` |

---

## Installation

### Prerequisites
- Odoo Community 19.0 installed and running
- PostgreSQL database configured
- Developer mode enabled (`?debug=1`)

### Steps

1. Clone this repo into your Odoo addons path:
   ```bash
   git clone https://github.com/<your-username>/foodloop.git /path/to/odoo/addons/foodloop
   ```

2. Add the parent directory to `addons_path` in your `odoo.conf`:
   ```ini
   addons_path = /path/to/odoo/odoo/addons,/path/to/odoo/addons
   ```

3. Restart the Odoo server:
   ```bash
   python odoo-bin -c odoo.conf
   ```

4. In Odoo, go to **Settings → Apps**, search for `FoodLoop`, and click **Install**.

5. Demo data (14 listings) loads automatically on install.

---

## Module Structure

```
foodloop/
├── __manifest__.py          # Module metadata and data load order
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── food_surplus_listing.py   # Main model (states, guards, totals, sequence)
│   └── food_surplus_line.py      # Line items (product, meals, kg)
├── views/
│   ├── food_surplus_listing_views.xml  # Kanban, list, form, search views
│   └── foodloop_menus.xml              # Top-level menu
├── data/
│   ├── foodloop_sequence.xml     # ir.sequence for FL/0001 references
│   └── foodloop_demo.xml         # 14 demo listings (noupdate="1")
└── security/
    └── ir.model.access.csv       # CRUD access for internal users
```

---

## Impact Calculation

CO₂ savings use the widely-cited industry average:

```
co2_saved_kg = total_kg_rescued × 2.5
```

Source: EPA / WRAP food waste carbon intensity estimates (average across food categories).

---

## License

[LGPL-3.0](LICENSE) — the standard license for Odoo community modules.
