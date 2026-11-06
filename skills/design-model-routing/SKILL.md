---
name: Design model routing
description: >-
  Use when making a designed file (image, PDF, slide, carousel, lead magnet,
  pricing sheet, ad static, brand kit) for Achieve or IronBlueprint and
  deciding whether to stay in chat or launch a CloudAgent, which model, and
  how to keep the run cheap.
---
# Design model routing (Canvas owns)

Moved out of Canvas's profile 2026-11-01 (Lauren/@poteto ops: long playbooks live in skills). Ryne can override the tier or model by name.

## Pick the tier by complexity
1. **Light**: single frame, quick share card, rough draft. Stay in this chat. Image gen / local tools. No cloud agent.
2. **Standard**: clean story sets, carousels, one-pagers, flyers, polished social. CloudAgent with `claude-sonnet-5-5` or `gpt-5.6-sol`. Prefer Sonnet for layout and copy-in-design; Sol when he asks for OpenAI or a second pass is needed. Effort medium (not high).
3. **Serious**: multi-page lead magnets, pricing packets, brand kits, template systems, client/parent-facing finished work. CloudAgent `claude-opus-5-5` only. Effort high; xhigh only if he asks or a prior pass failed.

Named model: resolve it with CloudAgent models. Never invent ids. Prefer `new_repo: true` when there is no design repo. Say tier + model in one short line. Never claim Opus without running it.

## Token rules (always)
- Short briefs to cloud agents: brand, format/size, must-use facts, deliverable list. No essays.
- One clear pass per launch. If thin, escalate one tier instead of a long retry loop.
- Attach only the logos/refs needed. Never dump whole Drive folders.
- Light never opens a cloud agent. Standard never uses Opus. Serious never uses Sonnet/Sol as a warm-up.
- Quiet when there is no brief. No status filler.

## Changelog
- 2026-11-01: created from Canvas's profile ("Model routing" + "Token efficiency" blocks). Content unchanged.
