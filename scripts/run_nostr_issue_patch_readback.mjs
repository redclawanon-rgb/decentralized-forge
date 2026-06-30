import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { basename, isAbsolute, relative as relativePath } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { finalizeEvent, generateSecretKey, getPublicKey, verifyEvent } from 'nostr-tools/pure';
import { SimplePool } from 'nostr-tools/pool';

const ROOT = new URL('../', import.meta.url);
const ROOT_PATH = fileURLToPath(ROOT);
const fixtureUrl = new URL('fixtures/nostr-collaboration-events.json', ROOT);
const defaultEvidenceUrl = new URL('evidence/nostr-loop43-issue-patch-readback-2026-06-28.json', ROOT);
const draftEvidenceUrl = new URL('evidence/nostr-draft-collaboration-readback.json', ROOT);
const defaultSelectedRelays = ['wss://relay.damus.io', 'wss://nos.lol'];
const accidentalSmokeEventId = '152e6dcd3d377f36e1e350c512397eba1c6c193b03f9013fbea57c0e64f0b358';
const supersededEventIds = [
  '541af61ee7cee778f89f2be491a66e1a73e71925d10c8f5df319a09b975dc805',
  'bb9156282ecfcd4b5ea715d1c435766aaddb2ad2c2ef067ee497e959f9d41f53'
];

function usage() {
  return [
    'usage: node scripts/run_nostr_issue_patch_readback.mjs [options]',
    '',
    'Options:',
    '  --draft PATH       Use an unsigned export-nostr-draft JSON file; may be repeated',
    '  --output PATH      Evidence JSON to write',
    '  --relay URL        Selected relay to publish/read back from; may be repeated',
    '  --plan-only        Validate/build the plan without signing, publishing, or relay readback',
    '  --created-at SEC   Override base created_at for signed events',
    '  --help             Show this help'
  ].join('\n');
}

function parseArgs(argv) {
  const args = {
    drafts: [],
    output: null,
    relays: [],
    planOnly: false,
    createdAt: null
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--help') {
      console.log(usage());
      process.exit(0);
    }
    if (arg === '--draft') {
      args.drafts.push(argv[++index]);
    } else if (arg === '--output') {
      args.output = argv[++index];
    } else if (arg === '--relay') {
      args.relays.push(argv[++index]);
    } else if (arg === '--plan-only') {
      args.planOnly = true;
    } else if (arg === '--created-at') {
      args.createdAt = Number(argv[++index]);
      if (!Number.isInteger(args.createdAt)) {
        throw new Error('--created-at must be Unix seconds');
      }
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  return args;
}

function repoRelative(pathOrUrl) {
  const value = fileURLToPath(pathUrl(pathOrUrl));
  return relativePath(ROOT_PATH, value).replaceAll('\\', '/');
}

function pathUrl(path) {
  if (path instanceof URL) {
    return path;
  }
  return isAbsolute(path) ? pathToFileURL(path) : new URL(path.replaceAll('\\', '/'), ROOT);
}

function mappedRegistryPath(sourceRecord, fallbackIndex) {
  const type = sourceRecord?.type ?? 'collaboration';
  const id = sourceRecord?.id ?? fallbackIndex;
  if (type === 'issue') {
    return `issues.${id}`;
  }
  if (type === 'patch') {
    return `patches.${id}`;
  }
  return `${type}s.${id}`;
}

async function existingCreatedUtc(evidenceUrl) {
  try {
    const existing = JSON.parse(await readFile(evidenceUrl, 'utf8'));
    if (
      existing.schema_version === 'decentralized-forge.nostr-issue-patch-readback.v1' &&
      typeof existing.created_utc === 'string'
    ) {
      return existing.created_utc;
    }
  } catch {
    return null;
  }
  return null;
}

function eventTags(event) {
  return (event.tags ?? [])
    .filter((tag) => Array.isArray(tag) && tag.every((item) => typeof item === 'string'))
    .map((tag) => [...tag]);
}

function liveTemplateFromFixture(fixtureEvent, createdAt) {
  const sanitizedContent = fixtureEvent.content
    .replace(/\n\nDry-run issue body only; this event has not been signed or relayed\./g, '')
    .replace(/Dry-run issue body only; this event has not been signed or relayed\./g, '')
    .trim();
  const tags = eventTags(fixtureEvent);
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

function liveTemplateFromDraft(draft, sourcePath, createdAt) {
  if (draft.schema_version !== 'decentralized-forge.nostr-collaboration-draft.v1') {
    throw new Error(`unsupported draft schema in ${sourcePath}`);
  }
  if (![1621, 1617].includes(draft.event?.kind)) {
    throw new Error(`draft event kind must be 1621 or 1617 in ${sourcePath}`);
  }
  const tags = eventTags(draft.event).filter((tag) => tag[0] !== 'client' && tag[0] !== 'published_at');
  tags.push(['client', 'decentralized-forge-loop43-nostr-tools']);
  tags.push(['alt', 'Decentralized Forge project-specific NIP-34 issue/patch readback evidence']);
  tags.push(['published_at', String(createdAt)]);
  return {
    kind: draft.event.kind,
    created_at: createdAt,
    tags,
    content: [
      'Decentralized Forge project-specific live NIP-34 collaboration readback.',
      `Draft source: ${repoRelative(sourcePath)}.`,
      'This event is disposable evidence only and does not claim production readiness, identity trust, durability, global propagation, censorship resistance, security, or full NIP-34/forge compatibility.',
      '',
      draft.event.content ?? ''
    ].join('\n')
  };
}

async function loadFixtureSpecs(createdAt) {
  const fixture = JSON.parse(await readFile(fixtureUrl, 'utf8'));
  return fixture.events
    .filter((event) => event.kind === 1621 || event.kind === 1617)
    .map((event, index) => ({
      source_type: 'fixture',
      source_name: event.fixture_name,
      source_file: repoRelative(fixtureUrl),
      mapped_registry_path: event.mapped_registry_path,
      template: liveTemplateFromFixture(event, createdAt + index)
    }));
}

async function loadDraftSpecs(draftPaths, createdAt) {
  const specs = [];
  for (const [index, draftPath] of draftPaths.entries()) {
    const draft = JSON.parse(await readFile(draftPath, 'utf8'));
    specs.push({
      source_type: 'draft',
      source_name: `${draft.source_record?.type ?? 'record'}:${draft.source_record?.id ?? basename(draftPath)}`,
      source_file: repoRelative(draftPath),
      mapped_registry_path: mappedRegistryPath(draft.source_record, index),
      source_record: draft.source_record,
      template: liveTemplateFromDraft(draft, draftPath, createdAt + index)
    });
  }
  return specs;
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

function plannedEvent(spec, index) {
  return {
    source_type: spec.source_type,
    source_name: spec.source_name,
    source_file: spec.source_file,
    mapped_registry_path: spec.mapped_registry_path,
    kind: spec.template.kind,
    created_at: spec.template.created_at,
    tag_count: spec.template.tags.length,
    content_size_bytes: Buffer.byteLength(spec.template.content, 'utf8'),
    planned_index: index
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const selectedRelays = args.relays.length > 0 ? args.relays : defaultSelectedRelays;
  const createdAt = args.createdAt ?? Math.floor(Date.now() / 1000);
  const evidenceUrl = pathUrl(args.output ?? (args.drafts.length > 0 ? repoRelative(draftEvidenceUrl) : repoRelative(defaultEvidenceUrl)));
  const specs = args.drafts.length > 0 ? await loadDraftSpecs(args.drafts, createdAt) : await loadFixtureSpecs(createdAt);

  if (specs.length === 0) {
    throw new Error('no Nostr issue/patch events selected');
  }

  if (args.planOnly) {
    const evidence = {
      schema_version: 'decentralized-forge.nostr-issue-patch-readback-plan.v1',
      created_utc: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
      scope: args.drafts.length > 0 ? 'plan project-specific Nostr draft publish/readback' : 'plan fixture Nostr issue/patch publish/readback',
      selected_relays: selectedRelays,
      source_mode: args.drafts.length > 0 ? 'drafts' : 'fixtures',
      source_files: [...new Set(specs.map((spec) => spec.source_file))],
      event_count: specs.length,
      events: specs.map(plannedEvent),
      actions_not_taken: [
        'no Nostr event was signed',
        'no Nostr event was published',
        'no relay readback was attempted',
        'no secret key material was generated or recorded',
        'no durability, global propagation, censorship-resistance, identity-trust, security, full NIP-34/forge compatibility, or production-readiness claim is made'
      ],
      non_claims: [
        'plan only',
        'not signed',
        'not published',
        'no relay readback',
        'not production readiness'
      ],
      verification_passed: true
    };
    if (args.output) {
      await mkdir(new URL('.', evidenceUrl), { recursive: true });
      await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);
      console.log(`wrote Nostr issue/patch readback plan: ${repoRelative(evidenceUrl)}`);
    } else {
      console.log(JSON.stringify(evidence, null, 2));
    }
    return;
  }

  const secretKey = generateSecretKey();
  const pubkey = getPublicKey(secretKey);
  const signedEvents = specs.map((spec) => finalizeEvent(spec.template, secretKey));
  const pool = new SimplePool({ enablePing: false, enableReconnect: false, maxWaitForConnection: 8_000 });

  const eventResults = [];
  let smokeReadback = [];
  try {
    for (const [index, event] of signedEvents.entries()) {
      const spec = specs[index];
      const result = await publishAndReadback(pool, selectedRelays, event);
      eventResults.push({
        source_type: spec.source_type,
        source_name: spec.source_name,
        ...(spec.source_type === 'fixture' ? { fixture_name: spec.source_name } : {}),
        source_file: spec.source_file,
        mapped_registry_path: spec.mapped_registry_path,
        source_record: spec.source_record,
        kind: event.kind,
        id: event.id,
        pubkey: event.pubkey,
        local_signature_verified: verifyEvent(event),
        publish: result.publish,
        readback: result.readback
      });
    }
    if (args.drafts.length === 0) {
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
    }
  } finally {
    pool.destroy();
  }

  const acceptedRelays = [...new Set(eventResults.flatMap((result) => result.publish.filter((item) => item.ok).map((item) => item.relay)))];
  const readbackVerifiedRelays = [...new Set(eventResults.flatMap((result) => result.readback.filter((item) => item.matched && item.verify_readback).map((item) => item.relay)))];
  const allEventsVerified = eventResults.every((result) => result.local_signature_verified && result.readback.some((item) => item.matched && item.verify_readback));

  const evidence = {
    schema_version: 'decentralized-forge.nostr-issue-patch-readback.v1',
    loop: args.drafts.length > 0 ? 'project-draft-live-replay' : 43,
    created_utc: (await existingCreatedUtc(evidenceUrl)) ?? new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
    scope: args.drafts.length > 0 ? 'disposable Nostr project-specific draft publish/readback' : 'disposable Nostr NIP-34 issue and patch publish/readback',
    standing_approval: 'User requested looping Nostr issue/patch readback; standing approval covers low-volume disposable project-scoped Nostr publish/readback.',
    tool: {
      package: 'nostr-tools',
      version: '2.23.8',
      license: 'Unlicense'
    },
    source_fixture: args.drafts.length > 0 ? null : 'fixtures/nostr-collaboration-events.json',
    source_drafts: args.drafts.map(repoRelative),
    selected_relays: selectedRelays,
    disposable_pubkey: pubkey,
    event_count: eventResults.length,
    event_ids: eventResults.map((result) => result.id),
    accepted_relays: acceptedRelays,
    readback_verified_relays: readbackVerifiedRelays,
    events: eventResults,
    extra_accidental_smoke_readback: args.drafts.length > 0 ? null : {
      note: 'A one-event API smoke was published before switching from Relay to SimplePool readback; it is recorded here to keep live actions auditable.',
      event_id: accidentalSmokeEventId,
      readback: smokeReadback
    },
    superseded_events: args.drafts.length > 0 ? null : {
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
    claim_boundary: args.drafts.length > 0
      ? 'This proves only that the selected project-specific draft events were signed with disposable state and accepted/read back from at least one selected public relay during this run.'
      : 'This proves only that two disposable prototype NIP-34-shaped collaboration events were accepted by and read back from at least one selected public relay during this run.'
  };

  await mkdir(new URL('.', evidenceUrl), { recursive: true });
  await writeFile(evidenceUrl, `${JSON.stringify(evidence, null, 2)}\n`);

  if (!evidence.verification_passed) {
    console.error(JSON.stringify(evidence, null, 2));
    process.exit(1);
  }

  console.log(`Nostr issue/patch readback passed for ${evidence.event_count} events: ${evidence.event_ids.join(', ')}`);
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
