# API Security Checklist Guard
# Estimated tokens: ~250
# Category: Domain-Specific

## Directive

When generating or reviewing API code, automatically apply security best practices.

### Pre-Deployment Checklist

**Authentication & Authorization**
- [ ] All endpoints require authentication (unless intentionally public)
- [ ] JWT tokens have reasonable expiration times
- [ ] API keys are not exposed in URLs (use headers)
- [ ] Role-based access control (RBAC) is enforced
- [ ] OAuth scopes are minimally permissive

**Input Validation**
- [ ] All inputs validated for type, length, range, and format
- [ ] Request body size limits enforced
- [ ] File upload restrictions (type, size) in place
- [ ] No SQL/NoSQL injection vectors
- [ ] Path traversal attempts blocked

**Rate Limiting & Abuse Prevention**
- [ ] Rate limiting per user/IP
- [ ] Pagination on list endpoints (no unbounded queries)
- [ ] Request throttling on expensive operations
- [ ] CAPTCHA or proof-of-work on public endpoints

**Data Protection**
- [ ] HTTPS only (no HTTP fallback)
- [ ] Sensitive data excluded from logs
- [ ] Response filtering (no excessive data exposure)
- [ ] CORS properly configured
- [ ] Security headers set (HSTS, CSP, X-Frame-Options)

### Output Format
```
[API SECURITY REVIEW]
Score: N/20 checks passed
Critical issues: <list>
Recommendations: <prioritized list>
```
