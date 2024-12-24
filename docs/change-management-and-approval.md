# Change Management & Approval
This document outlines the branching method, repository restrictions, and how changes and improvements to the code-base get made.

## Branching
This repository uses the git-flow branching method with the following branches available:
- main
- dev
- feat/*
- hotfix/*

### Branch Protections
Both the 'main' and 'dev' branches have restrictions setup so that they cannot be pushed to directly by anyone; the only way to make changes is via pull-request. Pull-requests are configured so that they can only be merged once all CI checks have passed. This mechanism ensures that only code of a good quality is allowed to be merged into protected branches.

### Tag Protections
Because of the way tags are used to trigger release workflows, it's important that not anyone can push them to the repo. The risk is that they could upload arbitrary code that gets executed by the workflows. So, a GitHub ruleset is used to restrict tag creation to either workflows using a deploy key or by a repository admin.
