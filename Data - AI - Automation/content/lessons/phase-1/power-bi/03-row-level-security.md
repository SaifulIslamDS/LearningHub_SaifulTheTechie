---
title: "Power BI Row-Level Security: Each Manager Sees Only Their Region"
order: 3
summary: "Restrict which rows each user can see with static and dynamic RLS roles, test them in Desktop, and assign members in the service."
level: Intermediate
time: "40 min"
topics: ["Row-level security"]
prerequisites: ["phase-1/power-pivot-dax/01-relationships"]
keywords: [row-level security, rls, roles, manage roles, view as, test as role, userprincipalname, dynamic rls, security, viewer role, workspace roles, data access]
reviewed: 2026-10-09
resources:
  - title: "Row-level security (RLS) with Power BI"
    url: "https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security"
    source: "Microsoft Learn"
    note: "Defining roles, assigning members and testing."
  - title: "Row-level security (RLS) guidance in Power BI Desktop"
    url: "https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance"
    source: "Microsoft Learn"
    note: "Design advice and common pitfalls."
  - title: "Roles in workspaces in Power BI"
    url: "https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-roles-new-workspaces"
    source: "Microsoft Learn"
    note: "Admin, Member, Contributor and Viewer: who RLS applies to."
files: [sales_model.xlsx, regions.csv]
---

## What is it?

**Row-level security (RLS)** filters the data **inside the model** according to who is looking. With one report and one model, the Dhaka manager sees only Dhaka's orders and targets, while the Head of Sales sees everything.

- **Static RLS:** one role per group, e.g. role *Dhaka* with the filter `[region] = "Dhaka"`.
- **Dynamic RLS:** one role for everyone. The filter compares a table column with the signed-in user: `[manager_email] = USERPRINCIPALNAME()`.

!!! job "Why it matters at work"
    Without RLS, companies copy the same report once per region, which is a maintenance nightmare. Data security is also a compliance requirement: salaries, customer data and regional figures must not leak. RLS appears in almost every enterprise Power BI project and on the PL-300 exam.

## Example 1: a static role

1. In Power BI Desktop: **Modeling → Manage roles → New**. Name it **Dhaka**.
2. Select the table **Regions**. Add the filter `[region] = "Dhaka"` (or use **Switch to DAX editor**).
3. **Save**.

```dax
[region] = "Dhaka"
```

Because Regions filters **both** Orders and Targets (from the relationships lesson), one rule on the **dimension** secures both facts.

**Test it:** **Modeling → View as** → tick **Dhaka** → **OK**. The overview now shows:

| Measure | Everyone (no role) | As role *Dhaka* |
|---|---|---|
| Net Revenue | 9,075 | 3,170 |
| Target | 9,600 | 3,600 |
| Achievement % | 94.5% | 88.1% |
| Orders Count | 12 | 5 |

A banner shows "Now viewing as: Dhaka". Click **Stop viewing** to return.

!!! tip "Filter the dimension, not the fact"
    Putting the rule on `Regions` (4 rows) instead of `Orders` is simpler, faster, and protects every fact table related to Regions. If you filtered only Orders, Targets would still show all regions.

## Example 2: dynamic RLS with the user's email

The **Regions** table has a `manager_email` column (e.g. `dhaka.manager@example.com`). Create **one** role, **Regional managers**, on Regions:

```dax
[manager_email] = USERPRINCIPALNAME ()
```

`USERPRINCIPALNAME()` returns the sign-in name (UPN) of the person viewing the report. Each manager automatically sees only the rows where their email matches. To add a new region, add a row to the Regions table, with no new role.

**Test it:** **Modeling → View as** → tick **Regional managers** and **Other user**, enter `narayanganj.manager@example.com` → **OK**. You'll see Net Revenue **1,230**, Target **1,500**, Achievement **82.0%**.

!!! note "UPN vs email"
    The value returned is the user's **sign-in name (UPN)**. It usually looks like an email, but isn't always the same as their email address. Ask IT for the UPN list when you build the mapping table.

## Example 3: assign people in the Power BI service

You **can't** assign users to roles in Desktop. After publishing (next lesson):

1. Open the workspace → the **semantic model** → **… (More options) → Security**.
2. Select a role → add people or security groups → **Save**.
3. Use **… → Test as role** to check.

!!! warning "RLS applies to Viewers only"
    RLS restricts users with the workspace **Viewer** role, and people you share the report or app with. Workspace **Admins, Members and Contributors see all the data**, whatever their role. Give report consumers Viewer access (or share an app), never Member.

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| Testing only as yourself (Admin) | "RLS doesn't work": admins see everything | Test with **View as** / **Test as role** |
| Giving managers the Member role | They bypass RLS | Viewer role, or share via an app |
| Rule on the fact table only | Other facts (Targets) aren't restricted | Filter the shared dimension |
| UPN in the mapping table doesn't match sign-in names | Users see nothing | Use the UPN values IT provides |
| Treating RLS as the only control | Hidden pages or columns can still expose data elsewhere | Combine with workspace roles, and design what's in the model |

## Try it yourself

**Task:** Create a static role **Chattogram Division** that shows all regions in that division (use the `division` column). Test it with View as. What Net Revenue and Achievement % do you see?

<details markdown="1">
<summary>Show a hint</summary>

Filter on Regions: `[division] = "Chattogram Division"`.
</details>

<details markdown="1">
<summary>Show the solution</summary>

```dax
[division] = "Chattogram Division"
```

Only **Chattogram** is in that division, so the role shows Net Revenue **2,155**, Target **2,100** and Achievement **102.6%**. A **Dhaka Division** role (Dhaka, Gazipur, Narayanganj) would show **6,920** vs **7,500** (92.3%).
</details>

## Quick quiz

<div class="quiz-q" markdown="1">
1\. Where do you add people to an RLS role?

1. Power BI Desktop → Manage roles
2. Power BI service → semantic model → Security
3. In the DAX filter

<details markdown="1"><summary>Show answer</summary>
**B.** Roles are defined in Desktop, and members are assigned in the service.
</details>
</div>

<div class="quiz-q" markdown="1">
2\. Which workspace role is restricted by RLS?

1. Admin
2. Member
3. Viewer

<details markdown="1"><summary>Show answer</summary>
**C — Viewer.** Admins, Members and Contributors see all data.
</details>
</div>

<div class="quiz-q" markdown="1">
3\. What does `[manager_email] = USERPRINCIPALNAME()` achieve?

1. Each viewer sees only rows matching their sign-in name
2. It sends emails to managers
3. It hides the email column

<details markdown="1"><summary>Show answer</summary>
**A.** That's dynamic RLS: one role, filtered per user.
</details>
</div>

## Summary

- **RLS** filters model rows per user: static roles (fixed values) or dynamic (`USERPRINCIPALNAME()`).
- Put the rule on a **dimension** so it flows to every related fact.
- Define and test roles in Desktop (**Manage roles**, **View as**), and assign members in the service (**Security**).
- RLS applies to **Viewers** and shared or app users, not to Admins, Members or Contributors.

!!! job "Job-ready check"
    **Interview question:** *"How would you let 20 regional managers use one report while seeing only their own region?"*

    **Strong answer:** "Dynamic RLS: a region dimension with each manager's UPN, and one role filtering `[manager_upn] = USERPRINCIPALNAME()`. The filter flows from the dimension to sales and targets. I'd test with View as, give managers Viewer access or an app, and assign the role to a security group so access is managed in one place."

    **Mini project:** Add a static role and a dynamic role to your model. Document both in your README, with a screenshot of View as for one manager.
