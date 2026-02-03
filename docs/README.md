# SimpleLogin Documentation Index

Welcome to the SimpleLogin documentation! This index helps you find the information you need quickly.

## Getting Started

- 📚 [README](../README.md) - Main project overview and self-hosting instructions
- 🚀 [Quick Start Build Guide](./QUICK-START-BUILD.md) - Get up and running quickly
- 🤝 [Contributing Guide](./CONTRIBUTING.md) - How to contribute to SimpleLogin
- 🔒 [Security Policy](./SECURITY.md) - Report security issues

## Docker & Deployment

- 🏗️ [Build Documentation](./build-image.md) - Building Docker images for different platforms
- 🔄 [Alpine Migration Guide](./MIGRATION-ALPINE.md) - Migrating to Alpine-based images
- ⚠️ [Alpine Compatibility Notes](./ALPINE-COMPATIBILITY.md) - Known issues and workarounds
- 🏷️ [Build Release from Branch](./build-release-from-branch.md) - Release process
- ⬆️ [Upgrade Guide](./upgrade.md) - Upgrading SimpleLogin installations

## Configuration & Setup

- 🎨 [Static Assets & CDN](./STATIC-ASSETS-CDN.md) - Configuring CDN for static assets
- 📮 [Postfix Installation](./postfix-installation.png) - Mail server setup screenshots
- 🔐 [Postfix TLS Setup](./postfix-tls.md) - Securing mail with TLS
- 🚫 [SPF Enforcement](./enforce-spf.md) - Email authentication setup
- 📧 [Gmail Relay Setup](./gmail-relay.md) - Using Gmail for sending
- 📬 [Amazon SES Setup](./ses.md) - Using AWS SES for email delivery
- 🔒 [SSL/TLS Configuration](./ssl.md) - HTTPS setup

## Architecture & Development

- 🏗️ [Architecture Diagram](./archi.png) - System architecture overview
- 📊 [Detailed Diagram](./diagram.png) - Component relationships
- 💻 [Code Structure](./code-structure.md) - Project organization and code overview
- 🔑 [OAuth Implementation](./oauth.md) - OAuth2/OpenID Connect integration
- 🌐 [API Documentation](./api.md) - REST API reference

## Troubleshooting & Maintenance

- 🔧 [Troubleshooting Guide](./troubleshooting.md) - Common issues and solutions
- 🔥 [UFW Firewall Setup](./ufw.md) - Firewall configuration for Ubuntu

## Project Assets

- 🎨 [Banner](./banner.png) - Project banner image
- 🦸 [Hero Image](./hero.png) - Main hero graphic
- 🎯 [Hero SVG](./hero.svg) - Vector hero graphic
- 📸 [Custom Alias Screenshot](./custom-alias.png) - Feature demonstration
- 🎬 [One-Click Alias Demo](./one-click-alias.gif) - Animated feature demo

## File Organization

```
docs/
├── README.md                      # This file
├── CONTRIBUTING.md                # Contribution guidelines
├── SECURITY.md                    # Security policy
├── QUICK-START-BUILD.md          # Quick start guide
├── MIGRATION-ALPINE.md           # Alpine migration guide
├── ALPINE-COMPATIBILITY.md       # Alpine compatibility notes
├── STATIC-ASSETS-CDN.md          # Static asset CDN guide
├── build-image.md                 # Docker build guide
├── build-release-from-branch.md   # Release process
├── upgrade.md                     # Upgrade guide
├── code-structure.md              # Code organization
├── api.md                         # API documentation
├── oauth.md                       # OAuth setup
├── postfix-tls.md                 # Postfix TLS guide
├── enforce-spf.md                 # SPF setup
├── gmail-relay.md                 # Gmail relay guide
├── ses.md                         # AWS SES guide
├── ssl.md                         # SSL/TLS setup
├── troubleshooting.md             # Troubleshooting
├── ufw.md                         # Firewall setup
├── CHANGELOG                      # Version history
├── *.png                          # Image assets
├── *.gif                          # Animated demos
└── *.svg                          # Vector graphics
```

## Quick Links by Use Case

### I want to...

**Deploy SimpleLogin**
1. Start with [README](../README.md) for prerequisites
2. Follow [Quick Start Build Guide](./QUICK-START-BUILD.md)
3. Configure email with [Postfix TLS](./postfix-tls.md) or [SES](./ses.md)
4. Set up [SSL/TLS](./ssl.md)
5. Review [Troubleshooting](./troubleshooting.md) if issues arise

**Contribute to Development**
1. Read [Contributing Guide](./CONTRIBUTING.md)
2. Understand [Code Structure](./code-structure.md)
3. Review [API Documentation](./api.md)
4. Build with [Build Documentation](./build-image.md)

**Migrate to Alpine Images**
1. Read [Alpine Compatibility Notes](./ALPINE-COMPATIBILITY.md)
2. Follow [Migration Guide](./MIGRATION-ALPINE.md)
3. Review [Build Documentation](./build-image.md) for new Dockerfiles

**Optimize Performance**
1. Set up [Static Assets CDN](./STATIC-ASSETS-CDN.md)
2. Review [Architecture Diagram](./archi.png)
3. Follow [Upgrade Guide](./upgrade.md) for latest optimizations

**Secure My Installation**
1. Configure [SSL/TLS](./ssl.md)
2. Set up [SPF Enforcement](./enforce-spf.md)
3. Enable [Postfix TLS](./postfix-tls.md)
4. Review [Security Policy](./SECURITY.md)
5. Configure [Firewall](./ufw.md)

**Troubleshoot Issues**
1. Check [Troubleshooting Guide](./troubleshooting.md)
2. Review [Alpine Compatibility](./ALPINE-COMPATIBILITY.md) if using Alpine
3. Check [GitHub Issues](https://github.com/simple-login/app/issues)
4. Ask in [GitHub Discussions](https://github.com/simple-login/app/discussions)

## External Resources

- 🌐 [Official Website](https://simplelogin.io)
- 📦 [GitHub Repository](https://github.com/simple-login/app)
- 🐛 [Issue Tracker](https://github.com/simple-login/app/issues)
- 💬 [Community Forum](https://github.com/simple-login/app/discussions)
- 📋 [Project Roadmap](https://github.com/simple-login/app/projects/1)
- 🐦 [Twitter](https://twitter.com/simplelogin)
- 🔧 [Browser Extension](https://chrome.google.com/webstore/detail/dphilobhebphkdjbpfohgikllaljmgbn)
- 📱 [Firefox Add-on](https://addons.mozilla.org/firefox/addon/simplelogin/)

## Need Help?

- **Bug Reports**: Use [GitHub Issues](https://github.com/simple-login/app/issues)
- **Security Issues**: Follow [Security Policy](./SECURITY.md)
- **Questions**: Ask in [GitHub Discussions](https://github.com/simple-login/app/discussions)
- **Feature Requests**: Vote or propose in [Discussions](https://github.com/simple-login/app/discussions)

## Recent Updates

See [CHANGELOG](./CHANGELOG) for detailed version history.

### Latest Changes (Current Refactor)
- ✅ Alpine-based Docker images (experimental)
- ✅ Multi-stage Docker builds for smaller images
- ✅ Updated to Ubuntu 24.04, Node 20, PostgreSQL 16
- ✅ Non-root user in containers
- ✅ Health checks in Dockerfiles
- ✅ Static asset CDN configuration
- ✅ Improved documentation structure
- ✅ Portable shell scripts

## Contributing to Documentation

Found an error or want to improve the docs?

1. Fork the repository
2. Make your changes in the `docs/` directory
3. Submit a pull request
4. Follow the [Contributing Guide](./CONTRIBUTING.md)

## License

SimpleLogin is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

---

**Last Updated**: 2026-02-03  
**SimpleLogin Version**: 4.x (current development)
