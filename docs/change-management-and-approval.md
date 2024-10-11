# Change management and approval
This document outlines the desired process for change management and making deployments, as well as some of the design challenges along the way.

## Desired process
The desired process for change management is that builds are pushed from two main branches:
- main
- dev

Whenever a push is made to these branches, a terraform apply workflow is run that syncs the infrastructure with whatever is on that branch. To keep pushes organised and held for approval before deploying, these branches have protections enabled meaning that pushes can only be made via pull request. Therefore, the final workflow is one in which a developer makes proposed changes on a feature branch, making a PR onto dev. the PR generates a Terraform plan, and once the PR is approved and merged that plan is run and applied.

## Challenges
### Bypassing branch restrictions for the merge workflow
The terraform plan is applied by the workflow `dev-merge.yaml` which applies and then commits the changes back onto the dev/main branch. By default, due to the protections on the branch, this is not possible. This has actually been a requested feature on github since [2022](https://github.com/orgs/community/discussions/13836) but currently still has not been implemented. Instead, I'm using one of the suggested workarounds in the thread.

#### Solution
In order to get around the protections, I am going to create a custom github application and add it to my repository. From that app I'm going to get it's access token and save it as a secret in my repository. Finally, I'm going to add the app to the list of authorised bypasses in the ruleset and then add the new token to the workflow.
