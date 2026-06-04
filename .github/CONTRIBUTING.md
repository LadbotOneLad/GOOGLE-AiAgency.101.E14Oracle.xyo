# Contributing to Te Papa Matihiko

Thank you for your interest in contributing to the Computational Tesla Coil!

## Before You Start

**Important**: Te Papa Matihiko is protected by the **Constitutional Identity Doctrine**. All contributions must respect the core doctrine and cannot dilute the system.

See [IDENTITY-DOCTRINE-CONSTITUTION.md](../docs/IDENTITY-DOCTRINE-CONSTITUTION.md) for the binding framework.

---

## What Can Be Contributed

### ✅ ALLOWED

- **Documentation improvements** — Clarifications, examples, tutorials
- **Bug reports** — Issues that don't violate doctrine
- **Test cases** — Validation and verification code
- **Deployment helpers** — Wrapper scripts, CI/CD configs
- **Examples** — How to use Te Papa Matihiko
- **Performance optimizations** — Without changing core behavior
- **Security improvements** — Bug fixes, hardening

### ❌ NOT ALLOWED

- **Wobble constant changes** — w_suu, w_aha, w_rere are immutable
- **Core architecture modifications** — すう/あは/れれ structure cannot change
- **Engine count reduction** — Must remain 14 engines
- **Doctrine dilution** — Constitutional articles are non-negotiable
- **Feature additions** that violate doctrine
- **Renaming core concepts** — Canonical names are fixed

---

## Contributing Process

### 1. Fork the Repository

```bash
git clone https://github.com/eric-hadfield/te-papa-matihiko.git
cd te-papa-matihiko
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming:
- `feature/` — New features (respecting doctrine)
- `bugfix/` — Bug fixes
- `docs/` — Documentation improvements
- `test/` — Test additions

### 3. Make Your Changes

Ensure:
- Code follows existing style
- Documentation is updated
- Tests pass
- No doctrine violations

### 4. Validate Doctrine Compliance

Before committing, run:

```bash
# Verify constitutional compliance
bash scripts/validate-doctrine.sh

# Run tests
npm test  # TypeScript
pytest    # Python

# Check locks
bash lock-status.sh
```

### 5. Commit Your Changes

```bash
git commit -m "Brief description of change

Longer explanation if needed.

Respects: [Article I/II/III/IV/V/VI]
Dilution: None
Doctrine: Compliant
"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a pull request on GitHub with:
- Clear title
- Description of changes
- How it respects the doctrine
- Test results
- Documentation updates

---

## Code Style

### TypeScript/JavaScript

```typescript
// Follow existing style in 4gr-fse.ts
// - Use readonly for immutable values
// - Explicit type annotations
// - Descriptive names (no abbreviations unless canonical)
// - Comments explaining why, not what
```

### Python

```python
# Follow existing style in digital_thymus_core.py
# - Type hints everywhere
# - docstrings for all functions
# - Meaningful variable names
# - Black formatting (88 chars)
```

### Documentation

```markdown
# Use clear headings
Follow existing patterns in documentation.
Keep the tri-language structure where applicable:
  日本語 (concept) / Te Reo Māori (relation) / English (science)
```

---

## Testing

All contributions must include tests:

```bash
# TypeScript tests
npm test

# Python tests
pytest tests/

# Integration tests
bash scripts/test-integration.sh
```

Coverage target: ≥ 80%

---

## Documentation

Update relevant documentation:

1. **Code changes** → Update docstrings
2. **Feature additions** → Add guide in `docs/`
3. **API changes** → Update API documentation
4. **Configuration** → Update setup guides

---

## Pull Request Review

Reviewers will check:

- ✅ Constitutional compliance
- ✅ No doctrine dilution
- ✅ Code quality
- ✅ Test coverage
- ✅ Documentation completeness
- ✅ No naming drift
- ✅ Coupling integrity (≥ 0.92)

Review timeline: 3-7 days

---

## Questions?

- **Architecture**: See [whitepaper.md](../whitepaper.md)
- **Constitutional Doctrine**: See [IDENTITY-DOCTRINE-CONSTITUTION.md](../docs/IDENTITY-DOCTRINE-CONSTITUTION.md)
- **Technical Details**: See relevant guides in `docs/`
- **Community**: Use GitHub Discussions

---

## Code of Conduct

See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)

---

Thank you for respecting the doctrine and contributing to the Computational Tesla Coil! 🔥
