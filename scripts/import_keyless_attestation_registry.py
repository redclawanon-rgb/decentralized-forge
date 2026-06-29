#!/usr/bin/env python3
"""Import hosted keyless attestation evidence into registry-shaped rows."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence" / "github-keyless-attestation-2026-06-28.json"
OUTPUT = ROOT / "fixtures" / "keyless-attestation.registry-verification.json"


def main() -> int:
    evidence = json.loads(SOURCE.read_text(encoding="utf-8"))
    subjects = evidence["attestation"]["subjects"]
    payload = {
        "schema_version": "decentralized-forge.registry-verification-import.v1",
        "loop": 45,
        "created_at": "2026-06-28",
        "source_evidence": "evidence/github-keyless-attestation-2026-06-28.json",
        "source_workflow_run": evidence["workflow_run"]["url"],
        "source_commit": evidence["workflow_run"]["commit"],
        "subject_count": len(subjects),
        "subjects": subjects,
        "verification_states": [
            {
                "scope": "github-actions.keyless_artifact_attestation",
                "state": "live-verified",
                "evidence": (
                    f"GitHub Actions run {evidence['workflow_run']['id']} generated hosted keyless "
                    f"artifact attestations for {len(subjects)} prototype artifacts with predicate "
                    f"{evidence['attestation']['predicate_type']}."
                ),
                "live_verified": True,
                "synthetic": False,
                "claim_boundary": (
                    "Hosted GitHub keyless attestation generation/import only; does not replace the "
                    "registry fixture ci.provenance row, does not claim SLSA compliance, production "
                    "supply-chain security, consumer policy verification, or production readiness."
                ),
                "last_checked_at": "2026-06-28",
                "notes": "Registry-shaped import row kept outside project-registry fixtures to avoid upgrading synthetic fixture provenance fields."
            }
        ],
        "registry_fixture_provenance_replaced": False,
        "contains_secret_values": False,
        "private_keys_used": False,
        "production_readiness_claim": False,
        "non_claims": [
            "does not make fixtures/example-project.registry.json ci.provenance live-verified",
            "does not claim SLSA compliance",
            "does not claim production supply-chain security",
            "does not claim consumer policy verification",
            "does not use production/private personal signing keys"
        ]
    }
    OUTPUT.write_text(f"{json.dumps(payload, indent=2)}\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
