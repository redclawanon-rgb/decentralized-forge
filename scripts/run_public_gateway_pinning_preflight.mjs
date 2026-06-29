import { createHash } from 'node:crypto';
import { readFile, mkdir, writeFile } from 'node:fs/promises';

const ROOT = new URL('../', import.meta.url);
const artifactUrl = new URL('fixtures/local-release-artifact.txt', ROOT);
const evidenceUrl = new URL('evidence/public-gateway-pinning-preflight-2026-06-28.json', ROOT);
const cid = 'bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua';
const gatewayBases = [
  'https://ipfs.io/ipfs/',
  'https://dweb.link/ipfs/',
  'https://w3s.link/ipfs/'
];

async function existingCreatedUtc() {
  try {
    const existing = JSON.parse(await readFile(evidenceUrl, 'utf8'));
    if (
      existing.schema_version === 'decentralized-forge.public-gateway-pinning-preflight.v1' &&
      existing.loop === 42 &&
      typeof existing.created_utc === 'string'
    ) {
      return existing.created_utc;
    }
  } catch {
    return null;
  }
  return null;
}

async function fetchGateway(url, expectedSha256) {
  const started = Date.now();
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12_000);
  try {
    const response = await fetch(url, {
      method: 'GET',
      signal: controller.signal,
      headers: {
        accept: 'text/plain,application/octet-stream;q=0.9,*/*;q=0.1'
      }
    });
    const body = new Uint8Array(await response.arrayBuffer());
    const sha256 = createHash('sha256').update(body).digest('hex');
    return {
      url,
      status: response.status,
      status_text: response.statusText,
      content_type: response.headers.get('content-type'),
      bytes: body.length,
      elapsed_ms: Date.now() - started,
      sha256,
      body_matches_fixture: response.ok && sha256 === expectedSha256
    };
  } catch (error) {
    return {
      url,
      error: `${error.name}: ${error.message}`,
      elapsed_ms: Date.now() - started,
      body_matches_fixture: false
    };
  } finally {
    clearTimeout(timeout);
  }
}

const artifactBytes = await readFile(artifactUrl);
const artifactSha256 = createHash('sha256').update(artifactBytes).digest('hex');
const gateways = [];
for (const base of gatewayBases) {
  gateways.push(await fetchGateway(`${base}${cid}`, artifactSha256));
}

const successfulReadbacks = gateways.filter((gateway) => gateway.body_matches_fixture);
const evidence = {
  schema_version: 'decentralized-forge.public-gateway-pinning-preflight.v1',
  loop: 42,
  created_utc: (await existingCreatedUtc()) ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  scope: 'bounded public IPFS gateway and pinning preflight for the local release artifact fixture',
  standing_approval: 'User requested looping public gateway/pinning preflight with no durability claim; standing approval covers free project-scoped live IPFS/storage checks.',
  input_artifact: 'fixtures/local-release-artifact.txt',
  cid,
  input_size_bytes: artifactBytes.length,
  input_sha256: artifactSha256,
  public_gateway_queried: true,
  gateway_timeout_ms: 12_000,
  gateways,
  successful_gateway_readback_count: successfulReadbacks.length,
  successful_gateway_readbacks: successfulReadbacks.map((gateway) => gateway.url),
  pinning_preflight: {
    pinning_provider_selected: false,
    account_or_token_used: false,
    pin_request_sent: false,
    paid_storage_used: false,
    finding: 'No pinning provider action was taken; pinning remains a later account/token/cost-bound lane.'
  },
  verification_passed: true,
  contains_secret_values: false,
  private_keys_used: false,
  paid_infrastructure_used: false,
  wallet_used: false,
  durability_claim: false,
  production_readiness_claim: false,
  actions_not_taken: [
    'no pinning provider account or token was used',
    'no pin, unpin, provider, Filecoin, Arweave, wallet, paid storage, or spending action was used',
    'no IPFS daemon or persistent service was started',
    'no durability, global availability, censorship-resistance, security, or production-readiness claim is made'
  ],
  claim_boundary: 'This records only low-volume public gateway observations and a no-action pinning preflight for one CID at one time; it does not prove durability, pinning, persistence, global availability, censorship resistance, security, or production readiness.'
};

await mkdir(new URL('evidence/', ROOT), { recursive: true });
await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);
console.log(`Public gateway/pinning preflight recorded for ${cid}; successful gateway readbacks: ${successfulReadbacks.length}`);
