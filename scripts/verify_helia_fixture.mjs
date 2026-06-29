import { createHash } from 'node:crypto';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createHelia } from 'helia';
import { unixfs } from '@helia/unixfs';
import { createLibp2p } from 'libp2p';
import { MemoryBlockstore } from 'blockstore-core';
import { MemoryDatastore } from 'datastore-core';

const ROOT = new URL('../', import.meta.url);
const artifactUrl = new URL('fixtures/local-release-artifact.txt', ROOT);
const evidenceUrl = new URL('evidence/helia-local-ipfs-add-get-2026-06-28.json', ROOT);
const expectedCid = 'bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua';
const expectedSha256 = '3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0';

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

async function createOfflineHelia() {
  const datastore = new MemoryDatastore();
  const blockstore = new MemoryBlockstore();
  const libp2p = await createLibp2p({
    datastore,
    addresses: { listen: [] },
    transports: [],
    connectionEncrypters: [],
    streamMuxers: [],
    peerDiscovery: [],
    services: {}
  });

  const helia = await createHelia({
    datastore,
    blockstore,
    libp2p,
    routers: [],
    blockBrokers: [],
    start: false
  });

  return helia;
}

async function readAll(asyncIterable) {
  const chunks = [];
  for await (const chunk of asyncIterable) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}

const artifactBytes = await readFile(artifactUrl);
const inputSha256 = createHash('sha256').update(artifactBytes).digest('hex');
let helia;
let evidence;

try {
  helia = await createOfflineHelia();
  const fs = unixfs(helia);
  const cid = await fs.addBytes(artifactBytes, { rawLeaves: true, cidVersion: 1 });
  const cidString = cid.toString();
  const readbackBytes = await readAll(fs.cat(cidString, { offline: true }));
  const readbackSha256 = createHash('sha256').update(readbackBytes).digest('hex');

  const byteLengthMatches = readbackBytes.length === artifactBytes.length;
  const byteContentMatches = Buffer.compare(Buffer.from(artifactBytes), readbackBytes) === 0;
  const verificationPassed =
    cidString === expectedCid &&
    inputSha256 === expectedSha256 &&
    readbackSha256 === expectedSha256 &&
    byteLengthMatches &&
    byteContentMatches;

  evidence = {
    schema_version: 'decentralized-forge.helia-local-ipfs-add-get.v1',
    loop: 41,
    created_utc: (await existingCreatedUtc()) ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
    scope: 'local Helia/IPFS UnixFS add-get verification only',
    standing_approval: 'User chat approval on 2026-06-28 covers free, project-scoped, low-volume, secret-free live IPFS/storage actions while still forbidding paid storage, wallets, production/private personal keys, persistent services, and stronger claims.',
    input_artifact: 'fixtures/local-release-artifact.txt',
    input_size_bytes: artifactBytes.length,
    input_sha256: inputSha256,
    expected_cid_from_loop_6: expectedCid,
    expected_sha256_from_loop_6: expectedSha256,
    local_unixfs_cid: cidString,
    local_unixfs_cid_note: 'Helia UnixFS addBytes CID observed for the fixture bytes using raw leaves and CIDv1; this run compares it against the raw CID/CAR fixture recorded in Loop 33.',
    loop_33_raw_cid: expectedCid,
    readback_size_bytes: readbackBytes.length,
    readback_sha256: readbackSha256,
    readback_bytes_match_input: byteContentMatches,
    readback_sha256_matches_input: readbackSha256 === inputSha256,
    helia_add: {
      cid: cidString,
      cid_version: cid.version,
      raw_leaves: true,
      unixfs_method: 'addBytes',
      expected_cid_matches: cidString === expectedCid
    },
    helia_readback: {
      method: 'cat',
      input: cidString,
      offline: true,
      output_size_bytes: readbackBytes.length,
      output_sha256: readbackSha256,
      output_sha256_matches_input: readbackSha256 === inputSha256,
      byte_length_matches_input: byteLengthMatches,
      byte_content_matches_input: byteContentMatches
    },
    offline_node_configuration: {
      implementation: 'helia',
      libp2p_listen_addresses: [],
      transports: [],
      peer_discovery: [],
      services: [],
      routers: [],
      block_brokers: [],
      in_memory_blockstore: true,
      in_memory_datastore: true,
      public_gateway_queried: false,
      pinning_performed: false
    },
    dependencies: {
      helia: '6.1.4',
      '@helia/unixfs': '7.2.1',
      'blockstore-core': 'transitive via helia',
      'datastore-core': 'transitive via helia'
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
    error: null,
    verification_passed: verificationPassed,
    actions_not_taken: [
      'no persistent IPFS/Kubo daemon was started',
      'no default Helia network routers or block brokers were enabled',
      'no public gateway was queried',
      'no public pinning service was used',
      'no pin, unpin, provider, or paid storage action was used',
      'no paid storage, Filecoin, Arweave, wallet, or spending action was used',
      'no production/private personal key was used',
      'no wallet, Filecoin, Arweave, paid pinning, or paid infrastructure action was used',
      'no durability, global availability, censorship-resistance, security, SLSA, or production-readiness claim is made'
    ],
    claim_boundary: 'This verifies only that the exact local fixture bytes can be added to and read back from an offline, in-memory Helia UnixFS node with the expected CID during one local execution.'
  };
} finally {
  if (helia != null) {
    await helia.stop();
  }
}

await mkdir(new URL('evidence/', ROOT), { recursive: true });
await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);

if (!evidence.verification_passed) {
  console.error(JSON.stringify(evidence, null, 2));
  process.exit(1);
}

console.log(`Helia local add/readback verification passed: ${evidence.helia_add.cid}`);
