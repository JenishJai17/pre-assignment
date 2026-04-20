from pydriller import Repository
from pydriller.domain.commit import ModificationType

# Input
repo_url = "https://github.com/apache/jclouds"
issue_ids = ["JCLOUDS-27", "JCLOUDS-43", "JCLOUDS-276", "JCLOUDS-435", "JCLOUDS-1548"]

# Storage
unique_commits = set()
total_unique_files_changed = 0
total_dmm_score = 0
valid_commit_count = 0

# Traverse repository
for commit in Repository(repo_url).traverse_commits():

    # Check if commit message contains any issue ID
    if any(issue_id in commit.msg for issue_id in issue_ids):

        unique_commits.add(commit.hash)

        # Track unique file paths per commit
        file_paths = set()

        for m in commit.modified_files:
            if m.change_type in {
                ModificationType.ADD,
                ModificationType.MODIFY,
                ModificationType.DELETE
            }:
                if m.new_path:
                    file_paths.add(m.new_path)
                elif m.old_path:
                    file_paths.add(m.old_path)

        total_unique_files_changed += len(file_paths)

        # DMM Metrics (if available)
        if (
            commit.dmm_unit_size is not None and
            commit.dmm_unit_complexity is not None and
            commit.dmm_unit_interfacing is not None
        ):
            dmm_score = (
                commit.dmm_unit_size +
                commit.dmm_unit_complexity +
                commit.dmm_unit_interfacing
            ) / 3

            total_dmm_score += dmm_score
            valid_commit_count += 1

# Final calculations
total_commits = len(unique_commits)

avg_files_changed = (
    total_unique_files_changed / total_commits
    if total_commits > 0 else 0
)

avg_dmm = (
    total_dmm_score / valid_commit_count
    if valid_commit_count > 0 else 0
)

# Output
print(f"Total Commits analyzed: {total_commits}")
print(f"Average number of files changed: {avg_files_changed:.2f}")
print(f"Average DMM metrics: {avg_dmm:.4f}")