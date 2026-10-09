---
title: Build an Authenticated News App — Part 2
order: 1
summary: Add account identity, server-side mutations, user-owned posts, comments, optimistic feedback and production states to the project.
level: Intermediate
time: 3–4 hours
curriculum_level: Level 01
source_module: '38'
source_type: source-curriculum
topics:
- Integrating BetterAuth in Project
- Server Actions — Create Post (Form + Validation )
- User-Specific Data (My Posts)
- Delete Post (Server Action + Optimistic UI)
- Comments System (Form + Action + UI)
- Loading Skeleton UX (loading.js + Hero UI Skeleton)
- Error Handling & Empty State Managing (error.js + Custom
- Deployment (Vercel + Environment Variable Setup in Dashboard)
- Final Testing Checklist + Common Bugs
prerequisites:
- level-01/l1-37-next-js-project-with-authentication-part-1/01-main
keywords:
- server actions
- optimistic ui
- comments
- authenticated project
- deployment
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
## Project goal

Part 2 turns a public content viewer into an application where identity changes what a user can do.

The key architecture is:

```text
signed-in user
    ↓
create / delete / comment action
    ↓
server verifies session + input + ownership
    ↓
database mutation
    ↓
UI refresh / optimistic feedback
```

Do not let optimistic UI change the trust model: the server still decides whether the action is valid.

## What you will build

- integrate Better Auth into the project;
- create posts through a server-owned mutation;
- list “My Posts” from the current user's identity;
- delete a user-owned post;
- comment on content;
- add loading skeletons, empty states and failure UI;
- prepare environment variables and final deployment checks.

## 1. Integrate auth before adding protected mutations

Make session reading work first. Add a page that displays the signed-in user's basic identity. Then build features that depend on it.

This isolates a major source of bugs: if post creation fails, you want to know whether the problem is authentication, validation or database logic.

## 2. Create post: treat form input as untrusted

```text
form data
  ↓
server action / route
  ↓
read session
  ↓
validate title/body
  ↓
write userId from session
  ↓
return result
```

Never accept `authorId` from a browser form as the authoritative owner ID.

## 3. “My Posts” is a scoped query

Conceptually:

```js
find({ authorId: session.user.id })
```

That filter belongs on the server/database query. Downloading every user's posts and filtering in the browser would expose data unnecessarily.

## 4. Delete with optimistic feedback

Optimistic UI can make a deletion feel immediate: remove the item from the visible list before the server responds. But preserve a recovery path if the server rejects the action.

Think in two states:

```text
optimistic view: item hidden
server result:
  success → keep it hidden
  failure → restore item + show error
```

## 5. Comments are another ownership relationship

A comment needs at least a content ID, author ID, body and timestamp. The server should populate the author from session state and validate that the target content exists.

## 6. Loading, empty and error are separate UI states

“My Posts” can legitimately return zero items. That should show an **empty state**, not an error. A network/database failure should show an error with a retry/recovery path.

## 7. Deployment environment

A deployed auth app usually needs its public base URL, database connection and provider credentials adjusted for the production domain. Add those values in the host configuration, not the repository.

Before declaring success, test:

```text
register / login
session persists
logout
create post
my posts only
unauthorized delete rejected
comment
loading/empty/error UI
deployment callback URLs
```

## Verification boundary

Better Auth, MongoDB and Vercel were not connected from the release environment, so the project-specific integration is **REFERENCE-ONLY**. The tutorial deliberately gives you a test checklist rather than invented screenshots or output.
