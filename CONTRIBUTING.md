# CONTRIBUTING

## How to Contribute to Atmospheric Truth Layer

Atmospheric Truth Layer is an open-source project under MIT license. Contributions are welcome and encouraged.

### Code of Conduct

All contributors agree to maintain professional, respectful communication. The project operates under institutional standards of conduct.

### Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/atmospheric-truth-layer.git
   cd atmospheric-truth-layer
   ```
3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test thoroughly**
   ```bash
   docker-compose up -d
   # Run tests
   ```
6. **Commit with clear messages**
   ```bash
   git commit -m "Feature: Clear description of changes"
   ```
7. **Push to your fork**
8. **Open a pull request**

### Pull Request Process

- Reference the issue number if applicable
- Include a clear description of changes
- Ensure all tests pass
- Add documentation for new features
- Maintain code style consistency

### Reporting Issues

Use GitHub Issues with:
- Clear title and description
- Steps to reproduce
- Expected vs. actual behavior
- System information (Docker version, OS, etc.)

### Code Standards

- **Python:** PEP 8 compliant
- **Documentation:** Clear, professional English
- **Commits:** Atomic, well-described
- **Tests:** All new features require tests

### Architecture Contributions

Major architectural changes require discussion in Issues before implementation. The project maintains:

- **Byzantine Consensus:** 14-engine architecture with K-value convergence
- **Cryptographic Verification:** SHA256, HMAC-SHA256, RFC3161 standards
- **XYO Integration:** Bound-witness ledger and invariant layer
- **Cycle Locking:** 90-day auto-renewal mechanism

### Documentation Contributions

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for technical changes
- Update API.md for endpoint changes
- Maintain consistent formatting

### Testing

```bash
# Build locally
docker-compose up -d

# Run health checks
curl http://localhost:8080/health

# Test pipeline
curl -X POST http://localhost:8080/process-satellite-frame \
  -G \
  --data-urlencode "satellite_source=Himawari" \
  --data-urlencode "region=Japan" \
  --data-urlencode "band=IR" \
  --data-urlencode "pixel_data=test" \
  --data-urlencode "latitude=35.6762" \
  --data-urlencode "longitude=139.6503"
```

### Licensing

All contributions must comply with MIT License. By contributing, you agree your work will be released under MIT.

### Questions?

Open a GitHub Discussion or Issue. Professional communication only.

---

**Status:** Production Ready  
**Architect:** AiAgency101  
**Mission:** Cryptographic verification of atmospheric truth
