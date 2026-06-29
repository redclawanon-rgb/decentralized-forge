import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { finalizeEvent, generateSecretKey, getPublicKey, verifyEvent } from 'nostr-tools/pure';
import { SimplePool } from 'nostr-tools/pool';

const ROOT = new URL('../', import.meta.url);
const fixtureUrl = new URL('fixtures/nostr-collaboration-events.json', ROOT);
const evidenceUrl = new URL('evidence/nostr-loop43-issue-patch-readback-2026-06-28.json', ROOT);
const selectedRelays = ['wss://relay.damus.io', 'wss://nos.lol'];
const accidentalSmokeEventId = '152e6dcd3d377f36e1e350c512397eba1c6c193b03f9013fbea57c0e64f0b358';
const supersededEventIds = [
  '541af61ee7cee778f89f2be491a66e1a73e71925d10c8f5df319a09b975dc805',
  'bb9156282ecfcd4b5ea715d1c435766aaddb2ad2c2ef067ee497e959f9d41f53'
];

async function existingCreatedUtc() {
  try {
    const existing = JSON.parse(await readFile(evidenceUrl, 'utf8'));
    if (
      existing.schema_version === 'decentralized-forge.nostr-issue-patch-readback.v1' &&
      existing.loop === 43 &&
      typeof existing.created_utc === 'string'
    ) {
      return existing.created_utc;
    }
  } catch {
    return null;
  }
  return null;
}

function liveTemplateFromFixture(fixtureEvent, pubkey, createdAt) {
  const sanitizedContent = fixtureEvent.content
    .replace(/\n\nDry-run issue body only; this event has not been signed or relayed\./g, '')
    .replace(/Dry-run issue body only; this event has not been signed or relayed\./g, '')
    .trim();
  const tags = fixtureEvent.tags
    .filter((tag) => Array.isArray(tag) && tag.every((item) => typeof item === 'string'))
    .map((tag) => [...tag]);
  tags.push(['client', 'decentralized-forge-loop43-nostr-tools']);
  tags.push(['alt', 'Decentralized Forge prototype NIP-34 issue/patch readback evidence']);
  tags.push(['published_at', String(createdAt)]);
  return {
    kind: fixtureEvent.kind,
    created_at: createdAt,
    tags,
    content: [
      'Decentralized Forge prototype/research live NIP-34 collaboration readback.',
      `Fixture source: ${fixtureEvent.fixture_name}.`,
      'This event is disposable evidence only and does not claim production readiness, identity trust, durability, global propagation, censorship resistance, security, or full NIP-34/forge compatibility.',
      '',
      sanitizedContent
    ].join('\n')
  };
}

async function publishAndReadback(pool, relays, event) {
  const publishResults = await Promise.allSettled(pool.publish(relays, event, { maxWait: 8_000 }));
  const publish = publishResults.map((result, index) => ({
    relay: relays[index],
    ok: result.status === 'fulfilled',
    reason: result.status === 'fulfilled' ? result.value : String(result.reason)
  }));

  const readback = [];
  for (const relay of relays) {
    const got = await pool.get([relay], { ids: [event.id] }, { maxWait: 8_000 });
    readback.push({
      relay,
      matched: got?.id === event.id,
      field_match: Boolean(got) && got.kind === event.kind && got.pubkey === event.pubkey && got.sig === event.sig,
      verify_readback: Boolean(got) && verifyEvent(got),
      event: got ?? null
    });
  }
  return { publish, readback };
}

const fixture = JSON.parse(await readFile(fixtureUrl, 'utf8'));
const sourceEvents = fixture.events.filter((event) => event.kind === 1621 || event.kind === 1617);
const secretKey = generateSecretKey();
const pubkey = getPublicKey(secretKey);
const createdAt = Math.floor(Date.now() / 1000);
const signedEvents = sourceEvents.map((event, index) => finalizeEvent(liveTemplateFromFixture(event, pubkey, createdAt + index), secretKey));
const pool = new SimplePool({ enablePing: false, enableReconnect: false, maxWaitForConnection: 8_000 });

const eventResults = [];
let smokeReadback = [];
try {
  for (const event of signedEvents) {
    const result = await publishAndReadback(pool, selectedRelays, event);
    eventResults.push({
      fixture_name: sourceEvents[signedEvents.indexOf(event)].fixture_name,
      mapped_registry_path: sourceEvents[signedEvents.indexOf(event)].mapped_registry_path,
      kind: event.kind,
      id: event.id,
      pubkey: event.pubkey,
      local_signature_verified: verifyEvent(event),
      publish: result.publish,
      readback: result.readback
    });
  }
  smokeReadback = await Promise.all(
    selectedRelays.map(async (relay) => {
      const got = await pool.get([relay], { ids: [accidentalSmokeEventId] }, { maxWait: 5_000 });
      return {
        relay,
        matched: got?.id === accidentalSmokeEventId,
        verify_readback: Boolean(got) && verifyEvent(got),
        event: got ?? null
      };
    })
  );
} finally {
  pool.destroy();
}

const acceptedRelays = [...new Set(eventResults.flatMap((result) => result.publish.filter((item) => item.ok).map((item) => item.relay)))];
const readbackVerifiedRelays = [...new Set(eventResults.flatMap((result) => result.readback.filter((item) => item.matched && item.verify_readback).map((item) => item.relay)))];
const allEventsVerified = eventResults.every((result) => result.local_signature_verified && result.readback.some((item) => item.matched && item.verify_readback));

const evidence = {
  schema_version: 'decentralized-forge.nostr-issue-patch-readback.v1',
  loop: 43,
  created_utc: (await existingCreatedUtc()) ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
  scope: 'disposable Nostr NIP-34 issue and patch publish/readback',
  standing_approval: 'User requested looping Nostr issue/patch readback; standing approval covers low-volume disposable project-scoped Nostr publish/readback.',
  tool: {
    package: 'nostr-tools',
    version: '2.23.8',
    license: 'Unlicense'
  },
  source_fixture: 'fixtures/nostr-collaboration-events.json',
  selected_relays: selectedRelays,
  disposable_pubkey: pubkey,
  event_count: eventResults.length,
  event_ids: eventResults.map((result) => result.id),
  accepted_relays: acceptedRelays,
  readback_verified_relays: readbackVerifiedRelays,
  events: eventResults,
  extra_accidental_smoke_readback: {
    note: 'A one-event API smoke was published before switching from Relay to SimplePool readback; it is recorded here to keep live actions auditable.',
    event_id: accidentalSmokeEventId,
    readback: smokeReadback
  },
  superseded_events: {
    note: 'An earlier Loop 43 run published two disposable events that still contained dry-run fixture wording. They are superseded by event_ids above and retained here only as an audit trail.',
    event_ids: supersededEventIds
  },
  verification_passed: allEventsVerified,
  contains_secret_values: false,
  private_keys_recorded: false,
  production_or_personal_key_used: false,
  paid_infrastructure_used: false,
  direct_outreach_used: false,
  actions_not_taken: [
    'no secret key material is recorded',
    'no production/private personal key was used',
    'no paid relay, paid infrastructure, wallet, or spending action was used',
    'no direct outreach was used',
    'no durability, global propagation, censorship-resistance, identity-trust, full NIP-34/forge compatibility, security, or production-readiness claim is made'
  ],
  non_claims: [
    'not proof of global propagation',
    'not proof of relay durability',
    'not proof of censorship resistance',
    'not proof of identity trust',
    'not proof of full NIP-34 or forge protocol compatibility',
    'not a security guarantee',
    'not production readiness'
  ],
  claim_boundary: 'This proves only that two disposable prototype NIP-34-shaped collaboration events were accepted by and read back from at least one selected public relay during this run.'
};

await mkdir(new URL('evidence/', ROOT), { recursive: true });
await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);

if (!evidence.verification_passed) {
  console.error(JSON.stringify(evidence, null, 2));
  process.exit(1);
}

console.log(`Nostr issue/patch readback passed for ${evidence.event_count} events: ${evidence.event_ids.join(', ')}`);
