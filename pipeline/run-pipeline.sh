#!/usr/bin/env bash
# Coverage Desk orchestrator — sequences Steps 1 through 5, checkpointing to
# git along the way, then hands off to the owner for Step 6.
#
# Usage: ./run-pipeline.sh "<slug>" "<topic>" "<notes>"
#
# Requires: jq, gtimeout (coreutils), codex, claude, agy, git, osascript —
# all on PATH — and CLAUDE_CODE_OAUTH_TOKEN set (run `claude setup-token`
# and export the result; see COVERAGE-DESK-SPEC.md section 4).
#
# What this does NOT do (see COVERAGE-DESK-SPEC.md section 8, Phase 2 scope):
# retry/back off on a failed CLI call (fails loud instead), full JSON Schema
# validation (structural jq checks only), Step 6 automation (owner's read,
# edit, and lock to Shared/ stays manual), or resuming a partial run.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/prompts"

trap 'echo "FAILED at line $LINENO: $BASH_COMMAND" >&2' ERR

# ---- config -----------------------------------------------------------

TIMEOUT_DRAFT=300
TIMEOUT_REVIEW=180
TIMEOUT_FEEDBACK=600   # Step 3 now runs Step 2.5's agy -p grounding calls
                        # itself, one per accuracy candidate — needs real room
TIMEOUT_RECONCILE=240
TIMEOUT_ARBITRATE=300  # includes Step 5's own git commit+push, and a
                        # possible PR-as-flag on a 5b
TIMEOUT_CHECKPOINT=120

# Branch every checkpoint/self-checkpointing step pushes to. Defaults to
# main for real runs; override with PUSH_BRANCH=<branch> for testing so a
# smoke-test run never touches main. The branch must already exist/be
# checked out locally before this script runs — it doesn't create one.
PUSH_BRANCH="${PUSH_BRANCH:-main}"

# ---- small helpers ------------------------------------------------------

log() {
  echo "[$(date '+%H:%M:%S')] $*" >&2
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

check_file_exists() {
  local f="$1" label="$2"
  [[ -s "$f" ]] || die "$label did not produce expected file: $f"
}

check_json_keys() {
  local f="$1"
  shift
  local key
  for key in "$@"; do
    jq -e "has(\"$key\")" "$f" >/dev/null || die "$f is missing required key: $key"
  done
}

# Renders a prompt template: replaces every literal "<slug>" with the
# episode slug, then any "{{key}}" placeholders from key=value args.
# Writes to stdout — caller redirects to a file.
render_prompt() {
  local template_file="$1" slug="$2"
  shift 2
  local content
  content="$(cat "$template_file")"
  content="${content//<slug>/$slug}"
  local kv key val
  for kv in "$@"; do
    key="${kv%%=*}"
    val="${kv#*=}"
    content="${content//\{\{$key\}\}/$val}"
  done
  # Always end with a newline — command substitution above already stripped
  # any trailing newline from the source file, and callers that concatenate
  # this output with another file (Step 3) need a clean line break at the
  # join, not the template's last line glued to the next file's first line.
  printf '%s\n' "$content"
}

preflight_check() {
  local missing=() cmd
  for cmd in jq gtimeout codex claude agy git osascript; do
    command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    die "Missing required tools: ${missing[*]}. Install with: brew install jq yq coreutils (codex/claude/agy must already be installed and authenticated)."
  fi
  if [[ -z "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]]; then
    die "CLAUDE_CODE_OAUTH_TOKEN is not set — claude -p can't authenticate headlessly. Run 'claude setup-token', export the result in your shell profile, then re-run."
  fi
}

# ---- CLI wrappers -------------------------------------------------------

run_codex() {
  local prompt_text="$1" timeout_s="$2" step_name="$3"
  log "$step_name: running codex exec (timeout ${timeout_s}s)..."
  gtimeout "$timeout_s" codex exec --skip-git-repo-check -s workspace-write "$prompt_text"
}

# Prompt is always read from a file and piped via stdin — never passed
# positionally. --allowedTools greedily consumes the next argv as more
# comma-separated tool rules if a prompt follows it positionally, shredding
# the prompt (see COVERAGE-DESK-SPEC.md section 9).
run_claude() {
  local prompt_file="$1" allowed_tools="$2" timeout_s="$3" step_name="$4"
  log "$step_name: running claude -p (timeout ${timeout_s}s)..."
  gtimeout "$timeout_s" claude -p --allowedTools "$allowed_tools" < "$prompt_file"
}

# ---- paths ----------------------------------------------------------------

paths_init() {
  local slug="$1"
  EPISODE_ROOT="$REPO_ROOT/Projects/$slug"
  CODEX_DIR="$EPISODE_ROOT/Codex"
  CLAUDE_DIR="$EPISODE_ROOT/Claude"
  SHARED_DIR="$EPISODE_ROOT/Shared"
  PRODUCTION_DIR="$EPISODE_ROOT/Production"
  mkdir -p "$CODEX_DIR" "$CLAUDE_DIR" "$SHARED_DIR" "$PRODUCTION_DIR"
}

# ---- steps ----------------------------------------------------------------

run_step1_draft() {
  local slug="$1" topic="$2" notes="$3"
  local rendered="$CODEX_DIR/.step1-prompt.txt"
  local prompt_text

  [[ -e "$CODEX_DIR/draft-v01.md" ]] && die "Projects/$slug/Codex/draft-v01.md already exists — this script doesn't support resuming/overwriting an existing episode. Pick a new slug."

  render_prompt "$PROMPTS_DIR/01-codex-draft.md" "$slug" "topic=$topic" "notes=$notes" > "$rendered"
  prompt_text="$(cat "$rendered")"
  run_codex "$prompt_text" "$TIMEOUT_DRAFT" "Step 1 (Codex draft)"
  check_file_exists "$CODEX_DIR/draft-v01.md" "Step 1 (Codex draft)"
  log "Step 1 done: $CODEX_DIR/draft-v01.md"
}

run_checkpoint() {
  local slug="$1" step_label="$2"
  local rendered="$CLAUDE_DIR/.checkpoint-prompt.txt"
  local head_before head_after

  render_prompt "$PROMPTS_DIR/checkpoint.md" "$slug" "step_label=$step_label" "push_branch=$PUSH_BRANCH" > "$rendered"
  head_before="$(git -C "$REPO_ROOT" rev-parse HEAD)"
  run_claude "$rendered" "Bash,Read,Edit" "$TIMEOUT_CHECKPOINT" "Checkpoint ($step_label)"
  head_after="$(git -C "$REPO_ROOT" rev-parse HEAD)"

  if [[ "$head_before" == "$head_after" ]]; then
    log "WARNING: checkpoint for '$step_label' produced no new commit (HEAD unchanged)"
  else
    log "Checkpoint committed: $head_after"
  fi
}

run_step2_review() {
  local slug="$1"
  local rendered="$CLAUDE_DIR/.step2-prompt.txt"

  render_prompt "$PROMPTS_DIR/02-claude-review.md" "$slug" > "$rendered"
  run_claude "$rendered" "Bash,Read,Edit" "$TIMEOUT_REVIEW" "Step 2 (Claude review)" > "$CLAUDE_DIR/.step2-notes.txt"
  check_file_exists "$CLAUDE_DIR/.step2-notes.txt" "Step 2 (Claude review)"
  log "Step 2 done: review notes captured"
}

run_step3_feedback() {
  local slug="$1"
  local template="$CLAUDE_DIR/.step3-template.txt"
  local rendered="$CLAUDE_DIR/.step3-prompt.txt"
  local point_count

  render_prompt "$PROMPTS_DIR/03-claude-feedback.md" "$slug" "push_branch=$PUSH_BRANCH" > "$template"
  # Step 2's raw notes are appended by file concatenation, never string
  # interpolation — they're unpredictable AI-generated prose that could
  # contain $, backticks, or ! that would get shell-interpreted otherwise.
  cat "$template" "$CLAUDE_DIR/.step2-notes.txt" > "$rendered"

  run_claude "$rendered" "Bash,Read,Write,Edit" "$TIMEOUT_FEEDBACK" "Step 3 (Claude feedback, self-grounding + self-checkpoint)"

  check_file_exists "$CLAUDE_DIR/feedback.json" "Step 3 (Claude feedback)"
  check_json_keys "$CLAUDE_DIR/feedback.json" episode_slug draft_version generated_by points
  jq -e '(.points | length) > 0' "$CLAUDE_DIR/feedback.json" >/dev/null || die "feedback.json has no points"

  point_count="$(jq '.points | length' "$CLAUDE_DIR/feedback.json")"
  log "Step 3 done: $point_count feedback points (Claude self-checkpointed)"
}

run_step4_reconcile() {
  local slug="$1"
  local rendered="$CODEX_DIR/.step4-prompt.txt"
  local prompt_text decision_count missing

  render_prompt "$PROMPTS_DIR/04-codex-reconcile.md" "$slug" > "$rendered"
  prompt_text="$(cat "$rendered")"
  run_codex "$prompt_text" "$TIMEOUT_RECONCILE" "Step 4 (Codex reconcile)"

  check_file_exists "$CODEX_DIR/draft-v02.md" "Step 4 (Codex reconcile)"
  check_file_exists "$CLAUDE_DIR/decision.json" "Step 4 (Codex reconcile)"
  check_json_keys "$CLAUDE_DIR/decision.json" episode_slug draft_version decisions
  jq -e '(.decisions | length) > 0' "$CLAUDE_DIR/decision.json" >/dev/null || die "decision.json has no decisions"

  missing="$(jq -n --slurpfile fb "$CLAUDE_DIR/feedback.json" --slurpfile dec "$CLAUDE_DIR/decision.json" \
    '(($fb[0].points | map(.id)) - ($dec[0].decisions | map(.feedback_id))) | length')"
  [[ "$missing" -eq 0 ]] || die "decision.json is missing $missing feedback point(s) present in feedback.json"

  decision_count="$(jq '.decisions | length' "$CLAUDE_DIR/decision.json")"
  log "Step 4 done: $decision_count decisions, all feedback points accounted for"
}

decisions_all_agree() {
  jq -e '(.decisions | length) > 0 and ([.decisions[].codex_response] | all(. == "agree"))' \
    "$CLAUDE_DIR/decision.json" >/dev/null
}

run_step5_arbitrate() {
  local slug="$1"
  local rendered="$CLAUDE_DIR/.step5-prompt.txt"
  local unresolved

  render_prompt "$PROMPTS_DIR/05-claude-arbitrate.md" "$slug" "push_branch=$PUSH_BRANCH" > "$rendered"
  run_claude "$rendered" "Bash,Read,Edit" "$TIMEOUT_ARBITRATE" "Step 5 (Claude arbitrate, self-checkpoint)"

  unresolved="$(jq '[.decisions[] | select(.codex_response == "disagree" and (.claude_arbitration == null))] | length' "$CLAUDE_DIR/decision.json")"
  [[ "$unresolved" -eq 0 ]] || die "Step 5 finished but $unresolved disagreement(s) still lack claude_arbitration"

  log "Step 5 done (Claude self-checkpointed; PR-as-flag opened for any 5b)"
}

notify_owner() {
  local kind="$1" message="$2"
  local safe_message="${message//\"/\\\"}"
  log "NOTIFY [$kind]: $message"
  osascript -e "display notification \"$safe_message\" with title \"Coverage Desk\"" \
    || log "WARNING: macOS notification failed to fire"
}

# ---- main -----------------------------------------------------------------

main() {
  if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <slug> <topic> <notes>" >&2
    exit 1
  fi

  local slug="$1" topic="$2" notes="$3"
  preflight_check
  paths_init "$slug"

  log "=== Coverage Desk pipeline: $slug (pushing to origin/$PUSH_BRANCH) ==="

  run_step1_draft "$slug" "$topic" "$notes"
  run_checkpoint "$slug" "Step 1 — Codex draft (draft-v01.md)"

  run_step2_review "$slug"
  run_step3_feedback "$slug"

  run_step4_reconcile "$slug"
  run_checkpoint "$slug" "Step 4 — Codex reconcile (draft-v02.md + decision.json)"

  if decisions_all_agree; then
    notify_owner "ready_for_review" \
      "$slug: all feedback points agreed, auto-finalized. Ready for your Step 6 read of draft-v02.md."
  else
    run_step5_arbitrate "$slug"
    local flagged_count
    flagged_count="$(jq '[.decisions[] | select(.status == "flagged")] | length' "$CLAUDE_DIR/decision.json")"
    if [[ "$flagged_count" -gt 0 ]]; then
      notify_owner "flagged" \
        "$slug: $flagged_count point(s) still disagreed after arbitration. See decision.json and the PR-as-flag."
    else
      notify_owner "ready_for_review" \
        "$slug: all disagreements resolved. Ready for your Step 6 read of draft-v02.md."
    fi
  fi

  log "=== Pipeline run complete for $slug. Step 6 (your read, edit, lock to Shared/) is next — not automated. ==="
}

main "$@"
