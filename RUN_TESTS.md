# 🧪 Running Tests - Quick Guide

## ✅ Tests Are Now Fixed!

All test errors have been resolved. The test suite should now run successfully.

---

## 🚀 How to Run Tests

### Option 1: Run All Tests
```bash
cd tests
python run_all_tests.py
```

### Option 2: Run Individual Test Files
```bash
# Database tests
python -m pytest tests/test_database.py -v

# ML model tests  
python -m pytest tests/test_ml_models.py -v

# API tests
python -m pytest tests/test_api.py -v

# Integration tests
python -m pytest tests/test_integration.py -v
```

---

## ✅ Expected Output

When tests run successfully, you should see:

```
============================================================
  VERITAS Command Center - Test Suite
============================================================

[OK] Loaded: test_database
[OK] Loaded: test_ml_models
[OK] Loaded: test_integration
[OK] Loaded: test_api

============================================================
  Running Tests...
============================================================

test_create_product ... ok
test_get_product ... ok
test_create_promise ... ok
test_statistics ... ok
...

============================================================
  Test Results
============================================================
  Tests run: X
  Failures: 0
  Errors: 0
  Skipped: Y

  [SUCCESS] ALL TESTS PASSED!
```

---

## ⚠️ Common Scenarios

### If Some Tests Are Skipped:
- **OK!** This is expected if dependencies are missing
- API tests may skip if FastAPI setup has issues
- ML tests may skip if transformers aren't installed

### If Tests Fail:
1. **Check database:** Make sure `setup_database.py` ran successfully
2. **Check dependencies:** Run `pip install -r requirements_upgraded.txt`
3. **Check paths:** Make sure you're in the project root

---

## 📋 Test Coverage

- ✅ Database operations (CRUD)
- ✅ ML models (extraction, sentiment, gap detection)
- ✅ API endpoints (if available)
- ✅ Full pipeline integration

---

## 🎯 What Tests Verify

1. **Database Tests:** Tables can be created, data can be saved/retrieved
2. **ML Tests:** Models can process data and return results
3. **API Tests:** Endpoints respond correctly (if FastAPI available)
4. **Integration Tests:** Full pipeline works end-to-end

---

## 💡 Tips

- Tests auto-initialize database tables
- Tests handle missing dependencies gracefully
- All tests use ASCII-safe output (Windows compatible)
- Failed tests provide clear error messages

---

**Your test suite is production-ready!** ✅
