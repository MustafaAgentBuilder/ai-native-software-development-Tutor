# Claude is Work to Build this Project
"""
Comprehensive Backend Testing Script

Tests all endpoints from every angle to ensure:
1. RAG is retrieving from book correctly
2. Responses are student-friendly
3. OLIVIA only answers from book content
4. Personalization works for different profiles
5. Caching works correctly
"""

import asyncio
import json
import requests
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:8000"

# Test results storage
test_results = []

def log_test(test_name: str, status: str, details: str = ""):
    """Log test result"""
    result = {
        "test": test_name,
        "status": status,  # PASS, FAIL, WARN
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    test_results.append(result)

    icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"{icon} {test_name}: {status}")
    if details:
        print(f"   {details}")

def print_separator(title: str):
    """Print test section separator"""
    print(f"\n{'='*80}")
    print(f" {title}")
    print(f"{'='*80}\n")


# ============================================================================
# Test 1: Health & Basic Endpoints
# ============================================================================

def test_health_endpoints():
    """Test basic health endpoints"""
    print_separator("TEST 1: Health & Basic Endpoints")

    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200 and "OLIVIA" in response.json().get("message", ""):
            log_test("Root endpoint", "PASS", f"Response: {response.json()['message']}")
        else:
            log_test("Root endpoint", "FAIL", f"Unexpected response: {response.text}")
    except Exception as e:
        log_test("Root endpoint", "FAIL", str(e))

    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            log_test("Health check", "PASS", "Server is healthy")
        else:
            log_test("Health check", "FAIL", f"Status: {response.json()}")
    except Exception as e:
        log_test("Health check", "FAIL", str(e))


# ============================================================================
# Test 2: Authentication Flow
# ============================================================================

def test_authentication():
    """Test complete authentication flow"""
    print_separator("TEST 2: Authentication Flow")

    # Test 2.1: Create beginner visual learner
    print("\n2.1 Testing beginner visual learner signup...")
    try:
        signup_data = {
            "email": f"beginner.visual.{datetime.now().timestamp()}@test.com",
            "password": "testpass123",
            "full_name": "Beginner Visual Learner",
            "programming_experience": "beginner",
            "ai_experience": "none",
            "learning_style": "visual",
            "preferred_language": "en"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)

        if response.status_code == 201:
            data = response.json()
            beginner_token = data["access_token"]
            log_test("Beginner signup", "PASS", f"User ID: {data['user']['id']}")
        else:
            log_test("Beginner signup", "FAIL", response.text)
            beginner_token = None
    except Exception as e:
        log_test("Beginner signup", "FAIL", str(e))
        beginner_token = None

    # Test 2.2: Create advanced practical learner
    print("\n2.2 Testing advanced practical learner signup...")
    try:
        signup_data = {
            "email": f"advanced.practical.{datetime.now().timestamp()}@test.com",
            "password": "testpass123",
            "full_name": "Advanced Practical Learner",
            "programming_experience": "advanced",
            "ai_experience": "advanced",
            "learning_style": "practical",
            "preferred_language": "en"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)

        if response.status_code == 201:
            data = response.json()
            advanced_token = data["access_token"]
            log_test("Advanced signup", "PASS", f"User ID: {data['user']['id']}")
        else:
            log_test("Advanced signup", "FAIL", response.text)
            advanced_token = None
    except Exception as e:
        log_test("Advanced signup", "FAIL", str(e))
        advanced_token = None

    # Test 2.3: Login with first user
    print("\n2.3 Testing login...")
    try:
        login_data = {
            "email": signup_data["email"],
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)

        if response.status_code == 200:
            log_test("User login", "PASS", "Login successful")
        else:
            log_test("User login", "FAIL", response.text)
    except Exception as e:
        log_test("User login", "FAIL", str(e))

    # Test 2.4: Get current user profile
    if advanced_token:
        print("\n2.4 Testing get current user...")
        try:
            headers = {"Authorization": f"Bearer {advanced_token}"}
            response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)

            if response.status_code == 200:
                user = response.json()
                log_test("Get current user", "PASS", f"Email: {user['email']}, Style: {user['learning_style']}")
            else:
                log_test("Get current user", "FAIL", response.text)
        except Exception as e:
            log_test("Get current user", "FAIL", str(e))

    return beginner_token, advanced_token


# ============================================================================
# Test 3: Summary Endpoint (Public, No Auth)
# ============================================================================

def test_summary_endpoint():
    """Test AI summary generation"""
    print_separator("TEST 3: Summary Endpoint (Public)")

    test_page = "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything"

    # Clear cache first to ensure clean test
    print("\n   Clearing cache for clean test...")
    try:
        requests.delete(f"{BASE_URL}/api/v1/content/cache/summary/{test_page}")
    except:
        pass  # Cache endpoint may not exist yet

    # Test 3.1: Generate summary (first time - should generate)
    print("\n3.1 Testing summary generation (first time)...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/content/summary/{test_page}")

        if response.status_code == 200:
            data = response.json()
            summary = data["summary_content"]
            cached = data["cached"]
            word_count = data["word_count"]

            # Check if summary is from book
            if len(summary) > 100 and not cached:
                log_test("Summary generation", "PASS",
                        f"Generated {word_count} words, cached={cached}")

                # Check if summary mentions book content
                book_indicators = ["AI", "software", "development", "chapter", "agent"]
                found_indicators = sum(1 for word in book_indicators if word.lower() in summary.lower())

                if found_indicators >= 2:
                    log_test("Summary content check", "PASS",
                            f"Found {found_indicators} book-related terms")
                else:
                    log_test("Summary content check", "WARN",
                            "Summary may not be from book content")

                print(f"\nSummary Preview (first 200 chars):\n{summary[:200]}...\n")
            else:
                log_test("Summary generation", "FAIL", "Summary too short or unexpectedly cached")
        else:
            log_test("Summary generation", "FAIL", response.text)
    except Exception as e:
        log_test("Summary generation", "FAIL", str(e))

    # Test 3.2: Request same summary (should be cached)
    print("\n3.2 Testing summary caching...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/content/summary/{test_page}")

        if response.status_code == 200:
            data = response.json()
            if data["cached"]:
                log_test("Summary caching", "PASS", "Summary served from cache instantly")
            else:
                log_test("Summary caching", "WARN", "Summary not cached (may be first run)")
        else:
            log_test("Summary caching", "FAIL", response.text)
    except Exception as e:
        log_test("Summary caching", "FAIL", str(e))


# ============================================================================
# Test 4: Personalized Content (Auth Required)
# ============================================================================

def test_personalized_endpoint(beginner_token, advanced_token):
    """Test personalized content generation with RAG"""
    print_separator("TEST 4: Personalized Content (Auth Required)")

    test_page = "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything"

    if not beginner_token or not advanced_token:
        log_test("Personalized content tests", "FAIL", "Missing auth tokens from signup")
        return

    # Test 4.1: Beginner visual learner personalization
    print("\n4.1 Testing beginner visual learner personalization...")
    try:
        headers = {"Authorization": f"Bearer {beginner_token}"}
        response = requests.get(
            f"{BASE_URL}/api/v1/content/personalized/{test_page}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            content = data["personalized_content"]
            profile = data["profile_snapshot"]

            # Check for visual learner content
            has_diagrams = "```mermaid" in content or "diagram" in content.lower()
            is_beginner_friendly = any(word in content.lower() for word in ["simple", "basic", "introduction", "let's start"])

            if len(content) > 200:
                log_test("Beginner personalization", "PASS",
                        f"Generated {len(content)} chars for {profile['learning_style']} learner")

                if has_diagrams:
                    log_test("Visual content check", "PASS", "Contains Mermaid diagrams for visual learner")
                else:
                    log_test("Visual content check", "WARN", "No diagrams found for visual learner")

                if is_beginner_friendly:
                    log_test("Beginner-friendly check", "PASS", "Content uses beginner-friendly language")
                else:
                    log_test("Beginner-friendly check", "WARN", "Content may be too advanced")

                print(f"\nBeginner Content Preview (first 300 chars):\n{content[:300]}...\n")
            else:
                log_test("Beginner personalization", "FAIL", "Content too short")
        else:
            log_test("Beginner personalization", "FAIL", response.text)
    except Exception as e:
        log_test("Beginner personalization", "FAIL", str(e))

    # Test 4.2: Advanced practical learner personalization
    print("\n4.2 Testing advanced practical learner personalization...")
    try:
        headers = {"Authorization": f"Bearer {advanced_token}"}
        response = requests.get(
            f"{BASE_URL}/api/v1/content/personalized/{test_page}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            content = data["personalized_content"]
            profile = data["profile_snapshot"]

            # Check for advanced practical content
            has_code = "```" in content
            is_advanced = any(word in content.lower() for word in ["advanced", "architecture", "pattern", "implementation"])

            if len(content) > 200:
                log_test("Advanced personalization", "PASS",
                        f"Generated {len(content)} chars for {profile['learning_style']} learner")

                if has_code:
                    log_test("Practical content check", "PASS", "Contains code examples for practical learner")
                else:
                    log_test("Practical content check", "WARN", "No code examples found")

                if is_advanced:
                    log_test("Advanced level check", "PASS", "Content uses advanced terminology")
                else:
                    log_test("Advanced level check", "WARN", "Content may be too basic for advanced learner")

                print(f"\nAdvanced Content Preview (first 300 chars):\n{content[:300]}...\n")
            else:
                log_test("Advanced personalization", "FAIL", "Content too short")
        else:
            log_test("Advanced personalization", "FAIL", response.text)
    except Exception as e:
        log_test("Advanced personalization", "FAIL", str(e))

    # Test 4.3: Cache validation
    print("\n4.3 Testing personalized content caching...")
    try:
        headers = {"Authorization": f"Bearer {beginner_token}"}
        response = requests.get(
            f"{BASE_URL}/api/v1/content/personalized/{test_page}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if data["cached"]:
                log_test("Personalized caching", "PASS", "Content served from cache")
            else:
                log_test("Personalized caching", "WARN", "Content regenerated (may be first run)")
        else:
            log_test("Personalized caching", "FAIL", response.text)
    except Exception as e:
        log_test("Personalized caching", "FAIL", str(e))


# ============================================================================
# Test 5: RAG Functionality
# ============================================================================

def test_rag_functionality(beginner_token):
    """Test that OLIVIA uses RAG and book content"""
    print_separator("TEST 5: RAG & Book Content Verification")

    if not beginner_token:
        log_test("RAG tests", "FAIL", "Missing auth token")
        return

    # Test 5.1: Ask a question that MUST use RAG
    print("\n5.1 Testing RAG search for book-specific content...")
    try:
        headers = {"Authorization": f"Bearer {beginner_token}"}

        # Use the test endpoint to ask a direct question
        params = {
            "query": "What is RAG and how does it work in the book?",
            "page_path": "test"
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/content/test-olivia",
            params=params
        )

        if response.status_code == 200:
            data = response.json()
            answer = data["response"]

            # Check if OLIVIA correctly refuses non-book topics
            refusal_phrases = ["not covered in our book", "not in the book", "isn't covered",
                             "not covered in the book", "isn't in our book", "topic isn't covered",
                             "isn't directly covered", "outside the scope", "seems to be outside"]
            has_refusal = any(phrase in answer.lower() for phrase in refusal_phrases)

            # Check if answer cites book sections (for topics that ARE in the book)
            has_citations = any(phrase in answer.lower() for phrase in
                              ["chapter", "section", "according to", "from the book", "the book explains"])

            # Check if RAG content indicators are present
            rag_indicators = ["retrieval", "augmented", "generation", "embedding", "search", "vector"]
            has_rag_content = sum(1 for word in rag_indicators if word in answer.lower())

            if len(answer) > 50:
                log_test("RAG search", "PASS", f"Generated answer with {len(answer)} chars")

                # CORRECT BEHAVIOR: OLIVIA should refuse topics not in book
                if has_refusal:
                    log_test("Book-only teaching check", "PASS", "OLIVIA correctly refuses non-book topics")
                elif has_citations:
                    log_test("Book citation check", "PASS", "Answer cites book sections")
                else:
                    log_test("Book citation check", "WARN", "No book citations or refusal found")

                if has_rag_content >= 2:
                    log_test("RAG content check", "PASS", f"Found {has_rag_content} RAG-related terms")
                else:
                    log_test("RAG content check", "WARN", "May not be using book content")

                print(f"\nOLIVIA's Answer Preview:\n{answer[:400]}...\n")
            else:
                log_test("RAG search", "FAIL", "Answer too short")
        else:
            log_test("RAG search", "FAIL", response.text)
    except Exception as e:
        log_test("RAG search", "FAIL", str(e))


# ============================================================================
# Test 6: Preferences Update & Cache Invalidation
# ============================================================================

def test_preferences_update(beginner_token):
    """Test preferences update and cache invalidation"""
    print_separator("TEST 6: Preferences Update & Cache Invalidation")

    if not beginner_token:
        log_test("Preferences tests", "FAIL", "Missing auth token")
        return

    # Test 6.1: Update preferences
    print("\n6.1 Testing preferences update...")
    try:
        headers = {"Authorization": f"Bearer {beginner_token}"}
        update_data = {
            "learning_style": "practical",
            "programming_experience": "intermediate"
        }

        response = requests.put(
            f"{BASE_URL}/api/v1/content/preferences",
            headers=headers,
            json=update_data
        )

        if response.status_code == 200:
            data = response.json()
            if data["success"] and data["cache_invalidated"]:
                log_test("Preferences update", "PASS",
                        f"Updated and invalidated {data['invalidated_count']} cached items")
            else:
                log_test("Preferences update", "WARN", "Update succeeded but cache not invalidated")
        else:
            log_test("Preferences update", "FAIL", response.text)
    except Exception as e:
        log_test("Preferences update", "FAIL", str(e))

    # Test 6.2: Verify new personalization reflects changes
    print("\n6.2 Testing personalization after preference update...")
    try:
        headers = {"Authorization": f"Bearer {beginner_token}"}
        test_page = "01-Introducing-AI-Driven-Development/01-ai-development-revolution/01-moment_that_changed_everything"

        response = requests.get(
            f"{BASE_URL}/api/v1/content/personalized/{test_page}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            profile = data["profile_snapshot"]

            if profile["learning_style"] == "practical" and not data["cached"]:
                log_test("Profile update reflection", "PASS",
                        "New content generated with updated profile")
            else:
                log_test("Profile update reflection", "WARN",
                        f"Profile: {profile}, Cached: {data['cached']}")
        else:
            log_test("Profile update reflection", "FAIL", response.text)
    except Exception as e:
        log_test("Profile update reflection", "FAIL", str(e))


# ============================================================================
# Test 7: Error Handling
# ============================================================================

def test_error_handling():
    """Test error handling"""
    print_separator("TEST 7: Error Handling")

    # Test 7.1: Unauthorized access to personalized content
    print("\n7.1 Testing unauthorized access...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/content/personalized/test-page"
        )

        if response.status_code == 403 or response.status_code == 401:
            log_test("Unauthorized access block", "PASS", "Correctly blocks unauthenticated users")
        else:
            log_test("Unauthorized access block", "FAIL",
                    f"Expected 401/403, got {response.status_code}")
    except Exception as e:
        log_test("Unauthorized access block", "FAIL", str(e))

    # Test 7.2: Invalid page path
    print("\n7.2 Testing invalid page path...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/content/summary/nonexistent/page/path"
        )

        if response.status_code == 404:
            log_test("Invalid page handling", "PASS", "Correctly returns 404 for invalid pages")
        else:
            log_test("Invalid page handling", "WARN",
                    f"Expected 404, got {response.status_code}")
    except Exception as e:
        log_test("Invalid page handling", "FAIL", str(e))


# ============================================================================
# Run All Tests
# ============================================================================

def run_all_tests():
    """Run comprehensive test suite"""
    print("\n" + "="*80)
    print(" COMPREHENSIVE BACKEND TESTING")
    print(" Testing all endpoints from every angle")
    print("="*80)

    start_time = datetime.now()

    # Run tests
    test_health_endpoints()
    beginner_token, advanced_token = test_authentication()
    test_summary_endpoint()
    test_personalized_endpoint(beginner_token, advanced_token)
    test_rag_functionality(beginner_token)
    test_preferences_update(beginner_token)
    test_error_handling()

    # Print summary
    print_separator("TEST SUMMARY")

    passed = sum(1 for r in test_results if r["status"] == "PASS")
    failed = sum(1 for r in test_results if r["status"] == "FAIL")
    warned = sum(1 for r in test_results if r["status"] == "WARN")
    total = len(test_results)

    print(f"Total Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Warnings: {warned}")
    print(f"\nSuccess Rate: {(passed/total*100):.1f}%")

    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"Elapsed Time: {elapsed:.2f}s")

    # Show failed tests
    if failed > 0:
        print("\n" + "="*80)
        print(" FAILED TESTS")
        print("="*80)
        for result in test_results:
            if result["status"] == "FAIL":
                print(f"\n❌ {result['test']}")
                print(f"   {result['details']}")

    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(test_results, f, indent=2)

    print(f"\n📊 Full results saved to: test_results.json")
    print("\n" + "="*80)


if __name__ == "__main__":
    run_all_tests()
