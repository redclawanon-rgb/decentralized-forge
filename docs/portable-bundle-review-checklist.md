# Portable Bundle Review Checklist

Use this checklist before attaching, publishing, or describing `output/decentralized-forge-verification-bundle.zip` outside the repository.

The bundle is a local verification package. It is not a signed release, a durability proof, a security review, a SLSA compliance claim, or evidence that a production decentralized forge is running.

## Required Local Checks

Run these commands from a clean checkout before sharing the bundle:

```sh
python scripts/forge_registry.py export-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip
python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip --json
python scripts/forge_registry.py verify-local --skip-npm-ci
```

If dependencies may have changed or the checkout has not run `npm ci`, run the full local verification suite instead:

```sh
npm ci
python scripts/forge_registry.py verify-local
```

## Report Review

Read the `report-bundle` output before sharing the ZIP. Confirm that it shows:

- verification status is `valid`
- all expected registry projects are listed
- evidence entry count matches the live evidence index
- protocol and state counts are understandable
- non-claims are present and unchanged
- verification gaps are present and not softened
- suggested commands include `verify-bundle`, `verify-bundle-cleanroom`, and `report-bundle`

If a reviewer receives an extracted directory instead of the ZIP, they can run:

```sh
python scripts/forge_registry.py report-bundle path/to/extracted-bundle
python scripts/forge_registry.py report-bundle path/to/extracted-bundle --json
```

## Required Non-Claims

Any release note, discussion post, attachment description, or handoff text must preserve these boundaries:

- no protocol event was published by the bundle commands
- no event was signed by the bundle commands
- no private key, wallet, paid service, or spending path was used by the bundle commands
- no daemon, persistent service, pinning service, or gateway publication was started by the bundle commands
- no durability, censorship-resistance, broad availability, identity-trust, security, SLSA compliance, or production-readiness claim is made

The existing evidence rows may record earlier bounded live checks. Those rows are evidence-scoped to their exact files, dates, public identifiers, and non-claims.

## Attachments

If publishing a release-like update, attach or reference:

- `output/decentralized-forge-verification-bundle.zip`
- the exact commit SHA
- the GitHub Actions run URL, if the commit was pushed
- the `report-bundle` text output or a JSON report generated with `--json`
- the command list used to verify the bundle

Do not describe the bundle as a production release, signed release, durable storage proof, or censorship-resistant mirror.

## Stop Conditions

Stop and do not publish the bundle if:

- `verify-bundle` fails
- `verify-bundle-cleanroom` fails
- `report-bundle` shows `"valid": false`
- the working tree has unexpected content changes after regeneration
- evidence hashes are stale
- a release note would need stronger claims than the evidence supports
- publication would require spending, paid infrastructure, production/private personal keys, direct outreach, or persistent public services

## Maintainer Release Note Template

Use neutral wording:

```text
Portable verification bundle for decentralized-forge at <commit>.

Verified locally with:
- python scripts/forge_registry.py verify-bundle output/decentralized-forge-verification-bundle.zip
- python scripts/forge_registry.py verify-bundle-cleanroom output/decentralized-forge-verification-bundle.zip
- python scripts/forge_registry.py report-bundle output/decentralized-forge-verification-bundle.zip

Scope: local verification package over committed fixtures, generated outputs, source evidence files, and verifier scripts. This is not a production forge, signed release, durability proof, broad availability proof, censorship-resistance proof, security guarantee, or SLSA compliance claim.
```
