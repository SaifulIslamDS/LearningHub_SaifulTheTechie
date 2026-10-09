# Product Requirements Document — SkillBridge

## Problem
Learners need one place to browse mentoring or learning services and manage purchases.

## Roles
- Visitor: browse public services.
- User: register, purchase, view own records.
- Moderator: manage content quality.
- Admin: manage users, services and payments.

## MVP
Authentication, service CRUD, search/list/detail, role-based dashboards, Stripe Checkout test flow, payment record, responsive UI, production deployment.

## Acceptance criteria
Every protected operation is enforced on the server; payment status is updated from a verified webhook, not from a browser redirect; secrets stay outside source control.
