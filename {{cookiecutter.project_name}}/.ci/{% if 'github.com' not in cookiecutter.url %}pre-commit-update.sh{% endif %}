#!/bin/bash
set -ex
pre-commit autoupdate
git status
git diff --quiet -- .pre-commit-config.yaml && git diff --staged --quiet -- .pre-commit-config.yaml || exit_code=$?

if [[ ${exit_code} -ne 0 ]]; then
  PRE_COMMIT_CI_BRANCH="pre-commit-ci-update-config-$(date +'%Y%m%d')"

  git config --global user.email "git@gitlab.com"
  git config --global user.name "GitLab CI"
  git remote set-url origin "https://__pre-commit_ci_token:${PRE_COMMIT_CI_JOB_TOKEN}@${CI_SERVER_HOST}:${CI_SERVER_PORT}/${CI_PROJECT_PATH}.git"
  git remote -v
  git add .pre-commit-config.yaml
  git checkout -b "${PRE_COMMIT_CI_BRANCH}"
  git commit -m "chore: [pre-commit.ci] pre-commit autoupdate"
  git push -u origin "${PRE_COMMIT_CI_BRANCH}":"${PRE_COMMIT_CI_BRANCH}" \
           -o merge_request.create \
           -o merge_request.target="$CI_DEFAULT_BRANCH" \
           -o merge_request.remove_source_branch \
           -o merge_request.title="chore: [pre-commit.ci] pre-commit autoupdate"
fi
