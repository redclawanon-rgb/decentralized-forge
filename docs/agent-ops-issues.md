# Agent Ops Issues

Operational issues noticed while running autonomous loops for this project.

## AOP-001: Large delegate_task timed out during overnight kickoff

**Date observed:** 2026-06-21 / 2026-06-22 overnight kickoff

**Symptom:**

A large `delegate_task(background=true)` request for the full decentralized forge overnight research/prototype loop timed out after 600 seconds with this tool-level result:

```text
Subagent timed out after 600.0s with 5 API call(s) completed — likely stuck on a slow API call or unresponsive network request.
```

No repo files were changed by that subagent. Parent verification showed the repo still clean at commit `171e578`.

**Immediate mitigation:**

- Converted the overnight work into a durable `cronjob` controller instead of relying on the timed-out delegated child.
- Created cron job `d798b0f9971b` / `Decentralized Forge Overnight Research Loop` with workdir `/home/openclaw/projects/decentralized-forge`.

**Follow-up diagnostic already run:**

A tiny no-tool `delegate_task` smoke test completed successfully in ~4 seconds and returned:

```text
- status: ok
- cwd_assumption: /home/openclaw/projects/decentralized-forge
- 2+2: 4
```

**Preliminary assessment:**

Delegation itself is not globally broken. The timeout appears related to the size/complexity/network behavior of the delegated overnight research task, not a total subagent outage.

**Hypotheses to investigate:**

1. Delegated child spent too long in web/API calls without producing a final summary.
2. The prompt was too broad for one subagent and should be split into smaller lanes.
3. Background delegate has a 600s hard cap unsuitable for overnight missions.
4. Long-running work should use cron, terminal background jobs, or spawned Hermes processes, while `delegate_task` should stay focused/bounded.
5. Toolset or model choice for delegation may need tuning in Hermes config.

**Recommended process change:**

Use `delegate_task` for bounded sub-10-minute lanes:

- research one protocol,
- review one doc,
- implement one small task,
- run one focused quality review.

Use cron/background Hermes/tmux for durable overnight controller loops.

**Open action:**

After the overnight job completes, run a focused delegation reliability check:

1. no-tool smoke test — already passed.
2. file-only child: read/write a small diagnostic file in a temp dir.
3. web-only child: fetch one known official doc and summarize.
4. terminal+file child: run a trivial command and write result.
5. 3 parallel short children using `tasks=[...]`.
6. one 8–10 minute bounded research child to see if timeout correlates with long web work.

Record results here and, if needed, update Hermes config or create a reusable skill for safe delegation sizing.
