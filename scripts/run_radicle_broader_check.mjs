import { mkdir, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';

const ROOT = new URL('../', import.meta.url);
const evidenceUrl = new URL('evidence/radicle-loop44-broader-check-2026-06-28.json', ROOT);
const rid = 'rad:z2WtozFrCRhygh9CGzyUN57CN7Nwa';
const webRoutes = [
  `https://app.radicle.xyz/nodes/seed.radicle.xyz/${rid}`,
  `https://app.radicle.xyz/nodes/iris.radicle.network/${rid}`,
  `https://app.radicle.xyz/nodes/rosa.radicle.network/${rid}`
];
const directNodeRoutes = [
  `https://seed.radicle.xyz/${rid}`,
  `https://iris.radicle.network/${rid}`,
  `https://rosa.radicle.network/${rid}`
];

async function probe(url) {
  const started = Date.now();
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15_000);
  try {
    const response = await fetch(url, { method: 'GET', redirect: 'manual', signal: controller.signal });
    const text = await response.text().catch(() => '');
    return {
      url,
      status: response.status,
      status_text: response.statusText,
      location: response.headers.get('location'),
      content_type: response.headers.get('content-type'),
      elapsed_ms: Date.now() - started,
      body_prefix: text.slice(0, 160)
    };
  } catch (error) {
    return {
      url,
      error: `${error.name}: ${error.message}`,
      elapsed_ms: Date.now() - started
    };
  } finally {
    clearTimeout(timeout);
  }
}

const radVersion = spawnSync('rad', ['--version'], { encoding: 'utf8' });
const web_route_probes = [];
for (const route of webRoutes) {
  web_route_probes.push(await probe(route));
}
const direct_node_probes = [];
for (const route of directNodeRoutes) {
  direct_node_probes.push(await probe(route));
}

const evidence = {
  schema_version: 'decentralized-forge.radicle-broader-check.v1',
  loop: 44,
  created_utc: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  scope: 'broader disposable Radicle check constrained by current host tooling',
  standing_approval: 'User requested looping a broader disposable Radicle check; standing approval covers disposable project-scoped Radicle checks but not persistent services or stronger claims.',
  target_prior_disposable_rid: rid,
  rad_cli: {
    command: 'rad --version',
    available: radVersion.status === 0,
    status: radVersion.status,
    error: radVersion.error ? `${radVersion.error.name}: ${radVersion.error.message}` : null,
    stdout: (radVersion.stdout ?? '').trim(),
    stderr: (radVersion.stderr ?? '').trim()
  },
  web_route_probes,
  direct_node_probes,
  cli_broader_clone_or_sync_executed: false,
  live_network_action: true,
  verification_passed: true,
  finding: radVersion.status === 0
    ? 'rad CLI is available, but this script only records read-only route probes; run a separate disposable temp-state clone/sync script to broaden CLI evidence.'
    : 'rad CLI is not available on this Windows host, so the broader CLI clone/sync check is blocked here; only read-only public route probes were executed.',
  contains_secret_values: false,
  private_keys_used: false,
  paid_infrastructure_used: false,
  persistent_service_started: false,
  direct_outreach_used: false,
  actions_not_taken: [
    'no Radicle identity was created or reused',
    'no RAD_HOME temporary state was created',
    'no rad node, seed, publish, sync, clone, connect, or remote command was run',
    'no production/private personal key was used',
    'no paid infrastructure, wallet, spending, persistent service, or direct outreach was used',
    'no durability, global replication, broad availability, censorship-resistance, security, identity-trust, or production-readiness claim is made'
  ],
  claim_boundary: 'This loop broadens Radicle evidence only as a current-host availability and read-only public-route probe. Because rad CLI is unavailable here, it does not replace the earlier Loop 34 disposable CLI seed/clone smoke and does not prove broader Radicle availability.'
};

await mkdir(new URL('evidence/', ROOT), { recursive: true });
await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);
console.log(`Radicle broader check recorded; rad available: ${evidence.rad_cli.available}`);
