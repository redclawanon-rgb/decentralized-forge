import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { CarReader, CarWriter } from '@ipld/car';
import * as raw from 'multiformats/codecs/raw';
import { sha256 } from 'multiformats/hashes/sha2';
import { CID } from 'multiformats/cid';

const ROOT = new URL('../', import.meta.url);
const artifactUrl = new URL('fixtures/local-release-artifact.txt', ROOT);
const evidenceUrl = new URL('evidence/local-car-cid-fixture-2026-06-22.json', ROOT);
const carUrl = new URL('evidence/local-release-artifact-2026-06-22.car', ROOT);

function toHex(bytes) {
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
}

async function carBytesForBlock(cid, bytes) {
  const { writer, out } = CarWriter.create([cid]);
  const chunks = [];
  const collect = (async () => {
    for await (const chunk of out) {
      chunks.push(chunk);
    }
  })();
  await writer.put({ cid, bytes });
  await writer.close();
  await collect;
  const carBytes = new Uint8Array(chunks.reduce((total, chunk) => total + chunk.length, 0));
  let offset = 0;
  for (const chunk of chunks) {
    carBytes.set(chunk, offset);
    offset += chunk.length;
  }
  return carBytes;
}

async function readAllBlocks(carReader) {
  const blocks = [];
  for await (const block of carReader.blocks()) {
    blocks.push(block);
  }
  return blocks;
}

async function existingCreatedUtc() {
  try {
    const existing = JSON.parse(await readFile(evidenceUrl, 'utf8'));
    if (
      existing.schema_version === 'decentralized-forge.local-car-cid-fixture.v1' &&
      existing.loop === 33 &&
      typeof existing.created_utc === 'string'
    ) {
      return existing.created_utc;
    }
  } catch {
    return null;
  }
  return null;
}

const artifactBytes = await readFile(artifactUrl);
const digest = await sha256.digest(artifactBytes);
const cid = CID.create(1, raw.code, digest);
const cidString = cid.toString();
const sha256Hex = createHash('sha256').update(artifactBytes).digest('hex');
const multihashDigestHex = toHex(digest.digest);
const carBytes = await carBytesForBlock(cid, artifactBytes);
const carReader = await CarReader.fromBytes(carBytes);
const roots = await carReader.getRoots();
const block = await carReader.get(cid);
const carBlocks = await readAllBlocks(carReader);
const carBlockCount = carBlocks.length;

const rootMatches = roots.length === 1 && roots[0].toString() === cidString;
const blockBytesMatch = Boolean(block) && Buffer.compare(Buffer.from(block.bytes), Buffer.from(artifactBytes)) === 0;
const blockCidMatches = Boolean(block) && block.cid.toString() === cidString;
const verificationPassed = rootMatches && blockBytesMatch && blockCidMatches && carBlockCount === 1;

await mkdir(new URL('evidence/', ROOT), { recursive: true });
await writeFile(carUrl, carBytes);

const evidence = {
  schema_version: 'decentralized-forge.local-car-cid-fixture.v1',
  loop: 33,
  created_utc: (await existingCreatedUtc()) ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  scope: 'local CAR/CID fixture verification only',
  permission: 'Permission I approved 2026-06-22 for one local CAR/CID fixture verification loop with project-scoped lockfile-backed dev dependencies.',
  input_artifact: 'fixtures/local-release-artifact.txt',
  input_size_bytes: artifactBytes.length,
  input_sha256: sha256Hex,
  cid: cidString,
  cid_version: cid.version,
  multibase: 'base32',
  multicodec: 'raw',
  multicodec_code: raw.code,
  multihash: 'sha2-256',
  multihash_digest_hex: multihashDigestHex,
  expected_cid_from_loop_6: 'bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua',
  expected_sha256_from_loop_6: '3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0',
  expected_cid_matches: cidString === 'bafkreibzglri2w3atm6k4jjbrsral2qsntj46ncgfdoeys436ckmkbtiua',
  expected_sha256_matches: sha256Hex === '3932e28d5b609b3cae25218ca205ea126cd3cf344628dc4c4b9bf094c50668a0',
  car_file: 'evidence/local-release-artifact-2026-06-22.car',
  car_size_bytes: carBytes.length,
  car_root_cids: roots.map((root) => root.toString()),
  car_block_count: carBlockCount,
  car_root_matches_cid: rootMatches,
  car_block_cid_matches: blockCidMatches,
  car_block_bytes_match_input: blockBytesMatch,
  dependencies: {
    '@ipld/car': '5.4.6',
    multiformats: '14.0.0'
  },
  lockfile: 'package-lock.json',
  verification_passed: verificationPassed,
  actions_not_taken: [
    'no IPFS daemon was started',
    'no IPFS add/fetch/pin command was run',
    'no public gateway was queried',
    'no wallet, Filecoin, Arweave, paid pinning, or paid storage action was used',
    'no durability, global availability, censorship-resistance, security, or production-readiness claim is made'
  ],
  claim_boundary: 'This verifies only that the local fixture bytes deterministically map to the recorded CID and can be packed into/read back from a local CAR file with project-scoped dev dependencies.'
};

await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);

if (!verificationPassed) {
  console.error(JSON.stringify(evidence, null, 2));
  process.exit(1);
}

console.log(`Local CAR/CID fixture verification passed: ${cidString}`);
