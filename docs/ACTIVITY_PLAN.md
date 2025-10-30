ACTIVITY_PLAN.md
# 🧭 Contribution & Activity Plan

**Owner:** Saeed Mohammadpour
**Duration:** Rolling 4-Week Cycle
**Applies To:**  `scrapy-production-template`
**Last Updated:** 2025-10-30 (Comprehensive Audit)
**Completion Status:** ~45% Overall | 75% Core Features | 0% Testing/Automation

---

## 🎯 Objective

Maintain continuous, meaningful contribution activity demonstrating **engineering depth**, **documentation leadership**, and **production-readiness**.

This plan defines automated or semi-automated contributions for Copilot AI or GitHub-based agents.

---

## ✅ Current Implementation Status

### Already Completed (Core Infrastructure)
- ✅ **3 Production Spiders**: HackerNews, Quotes, Books
- ✅ **PostgreSQL Pipeline**: Full CRUD with duplicate prevention
- ✅ **Docker Setup**: `docker-compose.yml` with PostgreSQL + healthchecks
- ✅ **Custom Middleware**: Stats tracking, error logging (2 middlewares)
- ✅ **Documentation Suite**:
  - [README.md](../README.md) with badges & architecture
  - [USAGE.md](USAGE.md) - Execution guide
  - [DEPLOYMENT.md](DEPLOYMENT.md) - Multi-platform deployment
  - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Debug guide
  - [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- ✅ **Visual Assets**: 4 architecture diagrams (light/dark mode)
- ✅ **Helper Scripts**: `run_all_spiders.sh`, `verify_project.sh`
- ✅ **Production Config**: Rate limiting, retries, robots.txt compliance
- ✅ **License & Project Summary**: MIT license, comprehensive stats

### Missing (Per This Plan) - **AUDIT CONFIRMED 2025-10-30**
- ❌ **ENTIRE `.github/` DIRECTORY** - No CI/CD infrastructure exists
  - ❌ `.github/workflows/ci.yml` - Not created
  - ❌ `.github/ISSUE_TEMPLATE/` - Not created
  - ❌ `.github/dependabot.yml` - Not created
- ❌ **ENTIRE `tests/` DIRECTORY** - No test infrastructure exists
  - ❌ `pytest.ini` - Not created
  - ❌ `tests/conftest.py` - Not created
  - ❌ Any test files (test_*.py) - Not created
- ❌ **Pre-commit hooks** - `.pre-commit-config.yaml` - Not created
- ❌ **Dev dependencies in requirements.txt**:
  - pytest, pytest-cov, pytest-mock
  - black, isort, flake8, pre-commit
- ❌ **Community files**: `CODE_OF_CONDUCT.md`, `SECURITY.md`
- ❌ **README.md "Recent Updates" section** - Not added

---

## 🗂️ Phase 1 — Commit Cadence & Automation Baseline

**Goal:** Establish predictable, small commits (2–3× per week per repo).
**Status:** 🔴 Not Started (5% Complete) - **AUDIT UPDATE: Only commit prefixes exist**

### Tasks
1. ❌ **TODO**: Create `.github/workflows/ci.yml` → run `pytest` + lint
   - Action: Add pytest, flake8, black to CI pipeline
   - Files needed: `.github/workflows/ci.yml`

2. ❌ **TODO**: Add `pre-commit` hooks: Black, isort, flake8
   - Action: Create `.pre-commit-config.yaml`
   - Add to `requirements.txt`: pre-commit, black, isort, flake8

3. ❌ **TODO**: Schedule Dependabot weekly for dependency updates
   - Action: Create `.github/dependabot.yml`
   - Config: weekly pip updates

4. ✅ **DONE**: Commit prefix convention established
   - Evidence: Recent commits use proper prefixes

5. 🟡 **PARTIAL**: Docstrings exist but incomplete
   - Current: Spiders and pipelines documented
   - Needs: Type hints throughout, middleware docs enhancement

**Cadence:**
- **Mon:** auto-lint & docstring pass *(automation pending)*
- **Wed:** dependency update PR *(Dependabot needed)*
- **Fri:** merge verified PRs *(manual currently)*  

---

## 🗂️ Phase 2 — Documentation & Showcase Commits

**Goal:** Keep documentation evolving and signal thought leadership.
**Status:** 🟢 Mostly Complete (80% Complete)

### Tasks
1. ✅ **DONE**: Core documentation established
   - Completed: [USAGE.md](USAGE.md), [DEPLOYMENT.md](DEPLOYMENT.md), [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - ❌ **TODO**: Add weekly micro-articles:
     - "Optimizing Crawl Efficiency with AutoThrottle"
     - "PostgreSQL Pipeline Performance Tuning"
     - "Error Recovery Strategies"
     - "Multi-Spider Orchestration Patterns"

2. 🟡 **PARTIAL**: [README.md](../README.md) has good structure
   - ✅ Has: Features, architecture, quick start
   - ❌ **TODO**: Add `### Recent Updates` section with timestamps

3. ❌ **TODO**: Generate weekly issue `#activity-week-XX` summarizing commits
   - Requires: GitHub Actions workflow for automated issue creation
   - Template needed in `.github/`

**Copilot Cue:**
> On Thursdays, create a new markdown section under `/docs` describing a micro-improvement, reference a commit, and update the README's Recent Updates section.

**Next Documentation Priorities:**
- Add `/docs/CRAWL_OPTIMIZATION.md`
- Add `/docs/DATABASE_SCHEMA.md`
- Create `### Recent Updates` footer in README

---

## 🗂️ Phase 3 — Testing & Quality Evolution

**Goal:** Improve visible test coverage.
**Status:** 🔴 Not Started (0% Complete)

### Tasks
1. ❌ **TODO**: Set up pytest framework
   - Create `tests/` directory structure:
     - `tests/test_spiders.py`
     - `tests/test_pipelines.py`
     - `tests/test_middlewares.py`
     - `tests/test_items.py`
   - Add `pytest.ini` configuration
   - Add `conftest.py` with fixtures

2. ❌ **TODO**: Add unit test for [pipelines.py](../scrapers/pipelines.py) (mock DB insert)
   - Mock PostgreSQL connections with pytest-mock
   - Test duplicate handling (ON CONFLICT)
   - Test connection error recovery

3. ❌ **TODO**: Add spider tests
   - Test HackerNews item parsing
   - Test Quotes pagination logic
   - Test Books price extraction
   - Use `scrapy.http.Response` fixtures

4. ❌ **TODO**: Update coverage badge in [README.md](../README.md)
   - Integrate pytest-cov
   - Add badge: `![Coverage](https://img.shields.io/badge/coverage-XX%25-green)`

5. ❌ **TODO**: Generate `/docs/coverage.md` summary each Tuesday
   - Automate via GitHub Actions
   - Track coverage trends over time

**Copilot Cue:**
> Each Tuesday, scan untested files, create minimal pytest tests, and update coverage.md and badges.

**Priority Testing Targets:**
- `scrapers/pipelines.py:PostgresPipeline` (critical path)
- `scrapers/spiders/hackernews_spider.py` (most complex parsing)
- `scrapers/middlewares.py:ScraperStatsMiddleware`

---

## 🗂️ Phase 4 — Issue Templates & Community Signals

**Goal:** Make repositories appear open, active, and professionally maintained.
**Status:** 🔴 Not Started (10% Complete) - **AUDIT UPDATE: Only CONTRIBUTING.md exists**

### Tasks
1. ❌ **TODO**: Create `.github/ISSUE_TEMPLATE/` templates
   - `bug_report.yml` - Structured bug reporting
   - `feature_request.yml` - Feature proposals
   - `spider_addition.yml` - New spider contribution template
   - `config.yml` - Template configuration

2. ✅ **DONE**: [CONTRIBUTING.md](../CONTRIBUTING.md) exists
   - Has: PR rules, branching strategy, code style
   - 🟡 **ENHANCE**: Add pytest testing requirements before PR

3. ❌ **TODO**: Add `.github/workflows/stale.yml`
   - Auto-close stale issues after 30 days
   - Auto-label after 15 days of inactivity
   - Exclude pinned issues

4. ❌ **TODO**: Generate monthly "📈 Contribution Summary" issue
   - Automate via GitHub Actions (cron: monthly)
   - Template: merged PRs, commits, documentation updates, coverage delta

**Copilot Cue:**
> On the first of each month, create an issue summarizing merged PRs, commits, and doc updates.

**Community Enhancements Needed:**
- Add `CODE_OF_CONDUCT.md`
- Add `SECURITY.md` (vulnerability reporting)
- Create discussion templates

---

## 🗂️ Phase 5 — Visibility & SEO Proof (optional, month 2+)

**Goal:** Reinforce public visibility and search signals.
**Status:** 🟡 Partially Complete (40% Complete)

### Tasks
1. ❌ **TODO**: Create `.github/social-preview.png`
   - Use existing architecture diagrams from `/docs/assets/`
   - Dimensions: 1280x640px
   - Update: weekly with latest diagram version

2. 🟡 **PARTIAL**: GitHub Topics need refresh
   - Current topics unknown
   - **Recommended**: `scrapy`, `web-scraping`, `etl`, `python`, `postgresql`, `docker`, `production-template`, `data-pipeline`, `crawler`, `scraping-framework`

3. ✅ **N/A**: Django-specific (not applicable to this Scrapy project)

4. ❌ **TODO**: Create `stats.json` snapshot
   - Location: `/docs/stats.json`
   - Content: Total records scraped, spider run counts, database sizes
   - Update: weekly via automated spider runs

5. ❌ **TODO**: Pin "Release Highlights" issue monthly
   - Create GitHub Action for monthly release summary
   - Highlight: new spiders, performance improvements, bug fixes

**SEO Enhancement Checklist:**
- Add comprehensive keywords to [README.md](../README.md)
- Create `/docs/EXAMPLES.md` with sample outputs
- Add "Star History" badge
- Link to related projects/alternatives

---

## 📆 Weekly Schedule Overview

| Day | Action | Output | Status |
|-----|---------|---------|--------|
| **Mon** | Lint & docstrings | Clean baseline | 🔴 Pre-commit needed |
| **Tue** | Unit test refresh | Updated coverage | 🔴 Pytest setup needed |
| **Wed** | Dependency PR | Updated libraries | 🔴 Dependabot needed |
| **Thu** | Docs addition | Knowledge signal | 🟡 Manual currently |
| **Fri** | Merge & changelog | Stable closure | 🟡 Manual currently |
| **1st of month** | Digest issue | Public continuity | 🔴 Automation needed |

**Legend:**
🟢 Automated | 🟡 Manual/Partial | 🔴 Not Implemented

---

## 🧩 README Footer Template (auto-update)

**Current Status:** Not yet added to [README.md](../README.md)

```markdown
---

### 🕓 Recent Updates
- 2025-10-26 — Completed activity plan status audit.
- 2025-10-24 — Added visual architecture diagrams (dark/light modes).
- 2025-10-22 — Implemented 3 production spiders with PostgreSQL pipeline.
- 2025-10-20 — Established deployment guides and Docker configuration.
*Updated weekly.*
```

**Action Required:** Add this section to the bottom of [README.md](../README.md)

---

## 🎯 Next 3 Priority Actions

Based on the current implementation status, here are the immediate next steps:

### 1. **Set Up Testing Infrastructure** (Phase 3 - Critical)
- Create `tests/` directory structure
- Add `pytest.ini` and `conftest.py`
- Write first test for [pipelines.py:56-120](../scrapers/pipelines.py#L56-L120) PostgreSQL connection
- **Impact:** Enables CI/CD, improves code quality, demonstrates professionalism

### 2. **Implement CI/CD Pipeline** (Phase 1 - High Priority)
- Create `.github/workflows/ci.yml`
- Configure: pytest, flake8, black checks
- Add coverage reporting to GitHub Actions
- **Impact:** Automated quality checks, professional project signal

### 3. **Add Pre-Commit Hooks** (Phase 1 - Quick Win)
- Create `.pre-commit-config.yaml`
- Configure Black (line-length: 100), isort, flake8
- Update [CONTRIBUTING.md](../CONTRIBUTING.md) with hook installation
- **Impact:** Code consistency, prevents bad commits

---

## 📊 Overall Progress Summary

**⚠️ AUDIT UPDATE (2025-10-30): Actual implementation verified against codebase**

| Phase | Claimed | **ACTUAL** | Priority | Blockers |
|-------|---------|------------|----------|----------|
| **Phase 1** (Automation) | 30% | **5%** 🔴 | 🔴 Critical | Entire .github/ missing |
| **Phase 2** (Documentation) | 80% | **80%** 🟢 | 🟢 Low | Minor enhancements only |
| **Phase 3** (Testing) | 0% | **0%** 🔴 | 🔴 Critical | Entire tests/ missing |
| **Phase 4** (Community) | 25% | **10%** 🔴 | 🟡 Medium | Only CONTRIBUTING.md exists |
| **Phase 5** (Visibility) | 40% | **40%** 🟡 | 🟢 Low | Optional enhancements |

**Overall Project Health:** 🟡 **~45% Complete (Not 75%)**

**Reality Check:**
- ✅ **Core Infrastructure (Scrapers/Pipelines):** 100% Complete - Production-ready
- ✅ **Documentation:** 80% Complete - Professional quality
- ❌ **Testing:** 0% Complete - **Completely absent**
- ❌ **CI/CD:** 0% Complete - **Completely absent**
- ❌ **Community Infra:** 10% Complete - **Mostly absent**

**The main gap:** Professional automation and testing infrastructure that demonstrates sustainable engineering practices. The scraping functionality is excellent, but the project **cannot demonstrate code quality** without tests and CI/CD.

---

## 📝 File Creation Checklist

**⚠️ STATUS: All items below are UNIMPLEMENTED as of 2025-10-30 audit**

### Immediate (Week 1) - **BLOCKING CRITICAL PATH**
- [ ] **Create `.github/` directory** ← Start here!
- [ ] **Create `tests/` directory** ← Start here!
- [ ] `.github/workflows/ci.yml` - CI/CD pipeline
- [ ] `.pre-commit-config.yaml` - Pre-commit hooks
- [ ] `tests/conftest.py` - Test fixtures
- [ ] `tests/test_pipelines.py` - Pipeline tests
- [ ] `pytest.ini` - Pytest configuration
- [ ] **Update `requirements.txt`** - Add dev dependencies:
  - [ ] pytest>=7.4.0
  - [ ] pytest-cov>=4.1.0
  - [ ] pytest-mock>=3.11.0
  - [ ] black>=23.0.0
  - [ ] isort>=5.12.0
  - [ ] flake8>=6.0.0
  - [ ] pre-commit>=3.3.0

### Short-term (Week 2-3)
- [ ] `.github/ISSUE_TEMPLATE/bug_report.yml`
- [ ] `.github/ISSUE_TEMPLATE/feature_request.yml`
- [ ] `.github/dependabot.yml`
- [ ] `tests/test_spiders.py`
- [ ] `/docs/coverage.md`

### Medium-term (Week 4+)
- [ ] `.github/workflows/stale.yml`
- [ ] `.github/workflows/monthly-digest.yml`
- [ ] `/docs/CRAWL_OPTIMIZATION.md`
- [ ] `/docs/DATABASE_SCHEMA.md`
- [ ] `/docs/stats.json`
- [ ] `CODE_OF_CONDUCT.md`
- [ ] `SECURITY.md`

---

## 🔍 Audit History

- **2025-10-30**: Comprehensive codebase audit - Confirmed 0% testing/CI infrastructure exists
  - Updated completion from claimed 75% → actual 45%
  - Verified all Phase 1 & 3 items are not implemented
  - Confirmed only CONTRIBUTING.md exists from Phase 4
- **2025-10-26**: Initial activity plan created

---

## 🚨 CRITICAL NEXT STEPS (2025-10-30)

Based on the audit, here's the **mandatory immediate action plan**:

### **Day 1 (Today): Foundation Setup** ⏱️ 2-3 hours
1. Create directory structure:
   ```bash
   mkdir -p .github/workflows tests
   touch tests/__init__.py
   ```

2. Update `requirements.txt` with dev dependencies:
   ```
   pytest>=7.4.0
   pytest-cov>=4.1.0
   pytest-mock>=3.11.0
   black>=23.0.0
   isort>=5.12.0
   flake8>=6.0.0
   pre-commit>=3.3.0
   ```

3. Create `pytest.ini` - Basic test configuration

4. Create `tests/conftest.py` - Test fixtures for database mocking

5. Install dependencies: `pip install -r requirements.txt`

### **Day 2: First Tests** ⏱️ 3-4 hours
6. Create `tests/test_pipelines.py` - Test PostgreSQL pipeline (3-5 tests)
7. Create `tests/test_items.py` - Test item models
8. Verify: `pytest tests/ -v` (should show green)

### **Day 3: CI/CD** ⏱️ 2 hours
9. Create `.github/workflows/ci.yml` - GitHub Actions workflow
10. Push to GitHub - Verify CI runs and passes

### **Day 4: Code Quality** ⏱️ 2 hours
11. Create `.pre-commit-config.yaml`
12. Run: `pre-commit install` and `pre-commit run --all-files`

### **Day 5: Community** ⏱️ 1-2 hours
13. Create `.github/ISSUE_TEMPLATE/bug_report.yml`
14. Create `.github/ISSUE_TEMPLATE/feature_request.yml`
15. Create `CODE_OF_CONDUCT.md` and `SECURITY.md`

**Expected Result:** Jump from 45% → 85% completion in 5 days

---

*Last audit: 2025-10-30 by Claude Code - Comprehensive codebase verification*
