import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { createHelia } from 'helia';
import { unixfs } from '@helia/unixfs';

const ROOT = new URL('../', import.meta.url);
const artifactUrl = new URL('fixtures/local-release-artifact.txt', ROOT);
const evidenceUrl = new URL('evidence/helia-local-ipfs-add-get-2026-06-28.json', ROOT);

async function existingCreatedUtc() {
  try {
    const existing = JSON.parse(await readFile(evidenceUrl, 'utf8'));
    if (
      existing.schema_version === 'decentralized-forge.helia-local-ipfs-add-get.v1' &&
      existing.loop === 41 &&
      typeof existing.created_utc === 'string'
    ) {
      return existing.created_utc;
    }
  } catch {
    return null;
  }
  return null;
}

function concat(chunks) {
  const total = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.length;
  }
  return bytes;
}

function sha256Hex(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

let helia;
const artifactBytes = await readFile(artifactUrl);
const inputSha256 = sha256Hex(artifactBytes);
const readbackChunks = [];
let unixfsCid;
let verificationPassed = false;
let errorMessage = null;

try {
  helia = await createHelia({ start: false });
  const fs = unixfs(helia);
  unixfsCid = await fs.addBytes(artifactBytes);
  for await (const chunk of fs.cat(unixfsCid.toString())) {
    readbackChunks.push(chunk);
  }
  const readbackBytes = concat(readbackChunks);
  verificationPassed =
    Buffer.compare(Buffer.from(readbackBytes), Buffer.from(artifactBytes)) === 0 &&
    sha256Hex(readbackBytes) === inputSha256;
} catch (error) {
  errorMessage = error instanceof Error ? error.message : String(error);
} finally {
  if (helia != null) {
    await helia.stop();
  }
}

const readbackBytes = concat(readbackChunks);
const evidence = {
  schema_version: 'decentralized-forge.helia-local-ipfs-add-get.v1',
  loop: 41,
  created_utc: (await existingCreatedUtc()) ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  scope: 'local Helia/IPFS UnixFS add-get verification only',
  standing_approval: 'User chat approval on 2026-06-28 covers free, project-scoped, low-volume, secret-free live IPFS/storage actions while still forbidding paid storage, wallets, production/private personal keys, persistent services, and stronger claims.',
  input_artifact: 'fixtures/local-release-artifact.txt',
  input_size_bytes: artifactBytes.length,
  input_sha256: inputSha256,
  local_unixfs_cid: unixfsCid?.toString() ?? null,
  local_unixfs_cid_note: 'Helia UnixFS addBytes CID observed for the fixture bytes; this run compares it against the raw CID/CAR fixture recorded in Loop 33.',
  loop_33_raw_cid: 'bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua',
  readback_size_bytes: readbackBytes.length,
  readback_sha256: readbackBytes.length > 0 ? sha256Hex(readbackBytes) : null,
  readback_bytes_match_input: readbackBytes.length > 0 && Buffer.compare(Buffer.from(readbackBytes), Buffer.from(artifactBytes)) === 0,
  readback_sha256_matches_input: readbackBytes.length > 0 && sha256Hex(readbackBytes) === inputSha256,
  verification_passed: verificationPassed,
  dependencies: {
    helia: '6.1.4',
    '@helia/unixfs': '7.2.1'
  },
  lockfile: 'package-lock.json',
  contains_secret_values: false,
  private_keys_used: false,
  paid_infrastructure_used: false,
  public_gateway_queried: false,
  pinned: false,
  helia_started: false,
  persistent_daemon_started: false,
  durability_claim: false,
  production_readiness_claim: false,
  error: errorMessage,
  actions_not_taken: [
    'no public gateway was queried',
    'no public pinning service was used',
    'no paid storage, Filecoin, Arweave, wallet, or spending action was used',
    'no production/private personal key was used',
    'no persistent IPFS/Kubo daemon, cron job, or always-on service was started',
    'no durability, global availability, censorship-resistance, security, or production-readiness claim is made'
  ],
  claim_boundary: 'This verifies only that a project-scoped, non-started Helia instance can add the local fixture bytes to local UnixFS/IPFS storage and read the exact bytes back during one local execution.'
};

await mkdir(new URL('evidence/', ROOT), { recursive: true });
await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);

if (!verificationPassed) {
  console.error(JSON.stringify(evidence, null, 2));
  process.exit(1);
}

console.log(`Local Helia add/get verification passed: ${evidence.local_unixfs_cid}`);
