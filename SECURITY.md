# Security Policy

## Supported Versions

The following versions of Alex AI are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 4.1.x   | :white_check_mark: |
| 4.0.x   | :x:                |
| < 4.0   | :x:                |

## Reporting a Vulnerability

We take the security of Alex AI seriously. If you believe you have found a security vulnerability, please report it to us by following these steps:

1.  **Do not open a public GitHub issue.**
2.  Email your findings to `security@narilabs.org` (Placeholder - update with your real email).
3.  Include a detailed description of the vulnerability, steps to reproduce, and any potential impact.

We will acknowledge receipt of your report within 48 hours and provide a timeline for resolution.

## Zero-Trust Architecture

Alex AI is designed with a "Local-First" and "Zero-Trust" philosophy:
- **Local Execution**: All LLM processing (via LM Studio) and Speech-to-Text (via Vosk) happen on your local machine.
- **Biometric MFA**: High-risk actions require dual-factor biometric authentication (Face ID + Voice Fingerprint).
- **Transparency**: Every action taken by the AI is displayed in real-time on the Transparency HUD for user audit.
- **Sandboxed Skills**: Dynamically created skills are executed in a controlled environment to mitigate system-wide risks.

---
*Building a secure future for Autonomous Intelligence.*