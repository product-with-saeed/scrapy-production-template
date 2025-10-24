#!/bin/bash

echo "=========================================="
echo "🔍 PROJECT VERIFICATION SCRIPT"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter
PASSED=0
FAILED=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "1. Checking Project Structure..."
echo "----------------------------"

if [ -d "scrapers/spiders" ]; then check_pass "Spider directory exists"; else check_fail "Spider directory missing"; fi
if [ -f "scrapers/items.py" ]; then check_pass "Items.py exists"; else check_fail "Items.py missing"; fi
if [ -f "scrapers/pipelines.py" ]; then check_pass "Pipelines.py exists"; else check_fail "Pipelines.py missing"; fi
if [ -f "scrapers/settings.py" ]; then check_pass "Settings.py exists"; else check_fail "Settings.py missing"; fi
if [ -f "scrapers/middlewares.py" ]; then check_pass "Middlewares.py exists"; else check_fail "Middlewares.py missing"; fi

echo ""
echo "2. Checking Spider Files..."
echo "----------------------------"

if [ -f "scrapers/spiders/hackernews_spider.py" ]; then check_pass "HackerNews spider exists"; else check_fail "HackerNews spider missing"; fi
if [ -f "scrapers/spiders/quotes_spider.py" ]; then check_pass "Quotes spider exists"; else check_fail "Quotes spider missing"; fi
if [ -f "scrapers/spiders/books_spider.py" ]; then check_pass "Books spider exists"; else check_fail "Books spider missing"; fi

echo ""
echo "3. Checking Documentation..."
echo "----------------------------"

if [ -f "README.md" ]; then check_pass "README.md exists"; else check_fail "README.md missing"; fi
if [ -f "CONTRIBUTING.md" ]; then check_pass "CONTRIBUTING.md exists"; else check_fail "CONTRIBUTING.md missing"; fi
if [ -f "LICENSE" ]; then check_pass "LICENSE exists"; else check_fail "LICENSE missing"; fi
if [ -f "docs/USAGE.md" ]; then check_pass "USAGE.md exists"; else check_fail "USAGE.md missing"; fi
if [ -f "docs/TROUBLESHOOTING.md" ]; then check_pass "TROUBLESHOOTING.md exists"; else check_fail "TROUBLESHOOTING.md missing"; fi
if [ -f "docs/DEPLOYMENT.md" ]; then check_pass "DEPLOYMENT.md exists"; else check_fail "DEPLOYMENT.md missing"; fi

echo ""
echo "4. Checking Configuration Files..."
echo "----------------------------"

if [ -f "requirements.txt" ]; then check_pass "requirements.txt exists"; else check_fail "requirements.txt missing"; fi
if [ -f "Dockerfile" ]; then check_pass "Dockerfile exists"; else check_fail "Dockerfile missing"; fi
if [ -f "docker-compose.yml" ]; then check_pass "docker-compose.yml exists"; else check_fail "docker-compose.yml missing"; fi
if [ -f ".env.example" ]; then check_pass ".env.example exists"; else check_fail ".env.example missing"; fi
if [ -f ".gitignore" ]; then check_pass ".gitignore exists"; else check_fail ".gitignore missing"; fi

echo ""
echo "5. Checking Sample Outputs..."
echo "----------------------------"

if [ -d "samples" ]; then check_pass "Samples directory exists"; else check_fail "Samples directory missing"; fi
if [ -f "samples/hackernews_sample.json" ]; then check_pass "HackerNews sample exists"; else check_fail "HackerNews sample missing"; fi
if [ -f "samples/quotes_sample.json" ]; then check_pass "Quotes sample exists"; else check_fail "Quotes sample missing"; fi
if [ -f "samples/books_sample.json" ]; then check_pass "Books sample exists"; else check_fail "Books sample missing"; fi

echo ""
echo "6. Checking Virtual Environment..."
echo "----------------------------"

if [ -d "venv" ]; then
    check_pass "Virtual environment exists"
    if [ -f "venv/bin/activate" ]; then
        check_pass "Activation script exists"
    else
        check_fail "Activation script missing"
    fi
else
    check_fail "Virtual environment missing"
fi

echo ""
echo "7. Checking Git Repository..."
echo "----------------------------"

if [ -d ".git" ]; then
    check_pass "Git repository initialized"
    COMMITS=$(git rev-list --count HEAD 2>/dev/null)
    if [ "$COMMITS" -gt 0 ]; then
        check_pass "Git commits present ($COMMITS commits)"
    else
        check_warn "No commits yet"
    fi
else
    check_fail "Git repository not initialized"
fi

echo ""
echo "8. Checking Database (if running)..."
echo "----------------------------"

if command -v psql &> /dev/null; then
    if psql -U scrapy -d scrapy_db -h localhost -c "\dt" &>/dev/null; then
        check_pass "PostgreSQL connection working"
        
        HN_COUNT=$(psql -U scrapy -d scrapy_db -h localhost -t -c "SELECT COUNT(*) FROM hackernews;" 2>/dev/null | tr -d ' ')
        Q_COUNT=$(psql -U scrapy -d scrapy_db -h localhost -t -c "SELECT COUNT(*) FROM quotes;" 2>/dev/null | tr -d ' ')
        B_COUNT=$(psql -U scrapy -d scrapy_db -h localhost -t -c "SELECT COUNT(*) FROM books;" 2>/dev/null | tr -d ' ')
        
        if [ "$HN_COUNT" -gt 0 ]; then check_pass "HackerNews data present ($HN_COUNT records)"; else check_warn "HackerNews table empty"; fi
        if [ "$Q_COUNT" -gt 0 ]; then check_pass "Quotes data present ($Q_COUNT records)"; else check_warn "Quotes table empty"; fi
        if [ "$B_COUNT" -gt 0 ]; then check_pass "Books data present ($B_COUNT records)"; else check_warn "Books table empty"; fi
    else
        check_warn "PostgreSQL not accessible (might be stopped)"
    fi
else
    check_warn "psql command not found"
fi

echo ""
echo "9. Checking for Placeholders (Need Personalization)..."
echo "----------------------------"

if grep -q "\[Your Name\]" README.md; then
    check_warn "[Your Name] placeholder found in README.md - needs personalization"
else
    check_pass "Name personalized in README.md"
fi

if grep -q "your.email@example.com" README.md; then
    check_warn "Email placeholder found in README.md - needs personalization"
else
    check_pass "Email personalized in README.md"
fi

if grep -q "@yourusername" README.md; then
    check_warn "GitHub username placeholder found - needs personalization"
else
    check_pass "GitHub username personalized in README.md"
fi

echo ""
echo "=========================================="
echo "📊 VERIFICATION SUMMARY"
echo "=========================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED!${NC}"
    echo ""
    echo "✅ Your project is ready for GitHub!"
    echo ""
    echo "Next steps:"
    echo "1. Create GitHub repository"
    echo "2. Add remote: git remote add origin <your-repo-url>"
    echo "3. Push: git push -u origin main"
    echo ""
else
    echo -e "${RED}⚠️  SOME CHECKS FAILED${NC}"
    echo ""
    echo "Please review the failed checks above and fix them before pushing to GitHub."
    echo ""
fi

echo "=========================================="
