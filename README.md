# Supabase Auth API

A secure FastAPI backend using Supabase as an Identity Provider (IdP) for authentication.
Instead of handling passwords or JWT signing manually, this API delegates signup, login,
and token verification to Supabase, and only guards protected routes by verifying tokens
against Supabase.

## Setup

1. Clone the repo
2. Create a virtual environment and activate it:
3. Install dependencies:
4. Copy `.env.example` to `.env` and fill in your own Supabase project URL and anon key:
5. Run the server:
6. Visit `http://localhost:8000/docs` for interactive Swagger UI.

## API Reference

| Method | Endpoint | Auth Required | Success | Errors |
|---|---|---|---|---|
| POST | /auth/signup | No | 201 | 400 |
| POST | /auth/login | No | 200 | 400, 401 |
| POST | /auth/logout | Yes (Bearer token) | 204 | 401 |
| GET | /protected/profile | Yes (Bearer token) | 200 | 401 |
| GET | /protected/dashboard | Yes (Bearer token) | 200 | 401 |
| GET | /public/info | No | 200 | – |

## Example
curl -X POST http://localhost:8000/auth/signup
-H "Content-Type: application/json"
-d '{"email":"test@example.com","password":"password123"}'
## Architecture note

Token verification is extracted into a reusable FastAPI dependency (`verify_token`),
applied to every protected route, so no route repeats auth logic.

## Honest note on logout

`supabase.auth.sign_out()` signs out the client's active session rather than explicitly
invalidating the specific bearer token passed in the header. A more precise implementation
would use the Supabase Admin API to revoke that exact token, but this requires the
service_role key, which is out of scope for this assignment's anon-key-only setup.
