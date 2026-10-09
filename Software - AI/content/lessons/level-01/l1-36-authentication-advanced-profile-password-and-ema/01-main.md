---
title: Profiles, Password Reset & Email Verification
order: 1
summary: Extend authentication beyond login with profile changes, password lifecycle, verification flows and safe error handling.
level: Intermediate
time: 80–110 min
curriculum_level: Level 01
source_module: '36'
source_type: source-curriculum
topics:
- 'Module Intro: What we''ll build — profile update, password'
- 'Update Profile: Build profile update form and change'
- 'Profile Image Upload: Upload image to server, save URL to database'
- 'Change Password: Old password verify, new password set'
- 'Forgot Password Flow: Request reset link, generate token, send email'
- 'Reset Password Page: Validate token, set new password'
- 'Email Verification: Send verification email on registration and verify'
- 'Resend Verification Email: Handle resend logic and expiry'
- 'Error Handling: Global error messages, edge cases'
- 'Module Summary: Full auth system recap, best practices'
prerequisites:
- level-01/l1-35-security-and-authentication-in-next-js-with-bett/01-main
keywords:
- profile
- password reset
- email verification
- upload
- token
- authentication
reviewed: '2026-10-09'
files:
- level-01/nextjs-fullstack-reference.zip
resources:
- title: Better Auth installation
  url: https://better-auth.com/docs/installation
  source: Better Auth
  note: Official installation and database adapter guidance.
- title: Better Auth basic usage
  url: https://better-auth.com/docs/basic-usage
  source: Better Auth
  note: Official email/password and social-provider usage.
- title: MongoDB adapter
  url: https://better-auth.com/docs/adapters/mongo
  source: Better Auth
  note: Official current MongoDB adapter setup.
- title: Next.js example
  url: https://better-auth.com/docs/examples/next-js
  source: Better Auth
  note: Official Next.js integration example.
---
## Start here

A production authentication experience continues after registration. Users change names, replace profile images, forget passwords and need email verification. Each feature combines **identity, data ownership, expiry and failure handling**.

The durable mental model is:

```text
user requests identity change
       ↓
prove or recover authority
       ↓
validate input/token
       ↓
perform server-side change
       ↓
revoke/refresh state when needed
       ↓
show safe result
```

## What you will learn

- profile update ownership;
- profile image upload boundaries;
- password change vs password reset;
- reset-link/token flow;
- email verification and resend/expiry;
- designing global error states without exposing sensitive details.

## 1. Profile update: identify the user from the session

Do not accept this as trusted input:

```json
{ "userId": "someone-else", "name": "New Name" }
```

The server should derive the user identity from the authenticated session and treat submitted data as fields to update **for that user**.

The same principle will reappear throughout backend development: object ownership is not proved by a hidden input field.

## 2. Profile image upload is two systems

An upload often has two operations:

```text
binary image
   ↓
storage service / server filesystem
   ↓
public or signed URL
   ↓
user profile record stores URL/metadata
```

Validate file type and size before trusting it. Later, Level 02 will deepen storage security and signed URLs; here the goal is to see that MongoDB usually stores metadata/URL rather than blindly embedding a huge browser upload into the user document.

## 3. Change password and reset password are different

**Change password:** the signed-in user knows the old password and wants a new one.

**Forgot/reset password:** the user cannot authenticate with the old password, so the system needs a separate recovery proof, often a time-limited token delivered to a verified email channel.

Do not merge these flows into one “password update” endpoint.

## 4. Password-reset flow

```text
Forgot password form
   ↓
request reset
   ↓
server issues time-limited recovery token
   ↓
email contains reset URL
   ↓
user opens reset page
   ↓
server validates token + expiry
   ↓
new password stored
```

The browser should not invent or validate the token by itself. The server/auth provider owns that trust decision.

## 5. Email verification

Verification answers: “Does this user control the email address associated with the account?” A common flow sends a verification token after registration and updates the account only when that token is accepted.

A resend feature needs throttling and expiry awareness. Otherwise a user can accidentally or deliberately generate large amounts of email.

## 6. Error design

Authentication errors need two properties at the same time:

1. enough information for a real user to recover;
2. not so much information that an attacker learns sensitive account state.

Design application error categories such as:

```text
VALIDATION_ERROR
UNAUTHENTICATED
FORBIDDEN
TOKEN_EXPIRED
RATE_LIMITED
SERVER_ERROR
```

Then map them to friendly UI rather than printing raw database/library errors.

## 7. Build the account settings page

A useful settings screen can contain three independent forms:

```text
Profile
  name + image

Security
  change password

Email
  verification status + resend
```

Keeping them separate produces clearer loading/error state and smaller server actions.

## Reference boundary

The Better Auth example linked below currently demonstrates profile updates, password reset, email verification and session management. Use it as the authoritative API reference while implementing. Email delivery, storage upload and token flows were **not executed in this release environment**; no success output is fabricated.
