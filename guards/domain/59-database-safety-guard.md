# Database Safety Guard
# Estimated tokens: ~220
# Category: Domain-Specific

## Directive

When generating or reviewing database queries and schema designs, enforce safety and best practices.

### Destructive Operation Warnings

Before generating any of the following, display a warning:
```
[DATABASE SAFETY WARNING]
This operation is: <DESTRUCTIVE/IRREVERSIBLE/HIGH-IMPACT>
Action: <what it does>
Risk: <what could go wrong>
Recommendation: <safer approach>
```

**Always warn for**:
- `DROP TABLE`, `DROP DATABASE`, `TRUNCATE`
- `DELETE` without `WHERE` clause
- `UPDATE` without `WHERE` clause
- Schema migrations that drop columns
- Changes to production connection strings

### Best Practices to Enforce

1. **Always use parameterized queries** — Never concatenate user input into SQL strings.
2. **Backup before migration** — Recommend backup steps before schema changes.
3. **Transaction wrapping** — Recommend wrapping multi-step operations in transactions.
4. **Least privilege** — Application database users should have minimal required permissions.
5. **Index awareness** — Flag queries that scan full tables without indexes on large tables.
6. **Connection security** — SSL/TLS for database connections, no plaintext passwords in config.

### Migration Protocol
```
Step 1: Backup current state
Step 2: Test migration on staging
Step 3: Apply migration with transaction
Step 4: Verify data integrity
Step 5: Document the change
```
