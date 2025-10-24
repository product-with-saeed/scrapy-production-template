#!/bin/bash

echo "=========================================="
echo "🔍 FINAL PROJECT VERIFICATION"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

check() {
    if [ "$1" = "true" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2"
        ((FAILED++))
    fi
}

echo "Core Project Files:"
check "$([ -d 'scrapers/spiders' ] && echo true || echo false)" "Spider directory exists"
check "$([ -f 'scrapers/items.py' ] && echo true || echo false)" "Items.py exists"
check "$([ -f 'scrapers/pipelines.py' ] && echo true || echo false)" "Pipelines.py exists"
check "$([ -f 'README.md' ] && echo true || echo false)" "README.md exists"
check "$([ -f 'Dockerfile' ] && echo true || echo false)" "Dockerfile exists"
check "$([ -f 'requirements.txt' ] && echo true || echo false)" "requirements.txt exists"

echo ""
echo "Spiders:"
check "$([ -f 'scrapers/spiders/hackernews_spider.py' ] && echo true || echo false)" "HackerNews spider"
check "$([ -f 'scrapers/spiders/quotes_spider.py' ] && echo true || echo false)" "Quotes spider"
check "$([ -f 'scrapers/spiders/books_spider.py' ] && echo true || echo false)" "Books spider"

echo ""
echo "Documentation:"
check "$([ -f 'docs/USAGE.md' ] && echo true || echo false)" "USAGE.md"
check "$([ -f 'docs/DEPLOYMENT.md' ] && echo true || echo false)" "DEPLOYMENT.md"
check "$([ -f 'LICENSE' ] && echo true || echo false)" "LICENSE"

echo ""
echo "Personalization Check:"
if ! grep -q "\[Your Name\]" README.md && ! grep -q "your.email@example.com" README.md; then
    echo -e "${GREEN}✓${NC} README personalized"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠${NC} Placeholders still found in README"
fi

echo ""
echo "Git Status:"
check "$([ -d '.git' ] && echo true || echo false)" "Git initialized"

if [ -d ".git" ]; then
    COMMITS=$(git rev-list --count HEAD 2>/dev/null)
    check "$([ $COMMITS -gt 0 ] && echo true || echo false)" "Commits present ($COMMITS)"
fi

echo ""
echo "=========================================="
echo -e "Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"
echo "=========================================="

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ PROJECT READY FOR GITHUB!${NC}"
fi
