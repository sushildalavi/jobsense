# Deploying jobsense

The repository contains configuration for hosting the API and worker on
[Railway](https://railway.app) and the web app on [Vercel](https://vercel.com).
Treat it as a starting point: every deployment workflow run up to 2026-11-26
failed, and these steps have not been verified end to end.

## What a push to `main` does

| Workflow | Runs on | Action |
|---|---|---|
| `ci.yml` | every push and pull request to `main` or `develop` | Lint, type-check, build, test |
| `deploy.yml` | every push to `main` | Deploys the API and worker to Railway, runs migrations, deploys the web app to Vercel |
| `deploy-api.yml` | pushes to `main` that touch `apps/api/**` | Deploys the API to Railway again and runs migrations |
| `deploy-web.yml` | pushes to `main` that touch `apps/web/**` or shared packages | Deploys the web app to Vercel again |

The deployment workflows do not wait for CI, and they overlap. Before adding
credentials, decide which set to keep and make it depend on CI. Adding `[skip ci]`
to the commit message at the head of a push skips all four.

## Services

1. Create a PostgreSQL database with the `vector`, `uuid-ossp`, `pg_trgm` and
   `btree_gin` extensions available, and a Redis instance.
2. Create an API service with root directory `apps/api`. It is configured by
   `railway.toml` and `nixpacks.toml`; the latter runs `alembic upgrade head` in
   the build phase.
3. Create a worker service from the same directory with this start command:

   ```
   celery -A app.tasks.celery_app worker --loglevel=info -Q ingestion,matching,ai,email,calendar,default --concurrency=2
   ```

   No periodic schedule is defined, so a Celery beat service has nothing to run.
4. Create a Vercel project with root directory `apps/web`. The web app imports
   types from `packages/types`, so the build needs the workspace and the built
   package.

## API and worker variables

| Variable | Notes |
|---|---|
| `DATABASE_URL`, `REDIS_URL` | From the database and Redis services |
| `ENVIRONMENT` | Set to `production`. The default is `development`, which accepts the placeholder signing key and logs password reset links |
| `SECRET_KEY` | At least 32 random characters, for example `openssl rand -hex 32`. Startup fails without it outside development and test |
| `FRONTEND_URL` | Exact web origin, used for CORS |
| `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` | For the language model features |
| `DEFAULT_LLM_PROVIDER` | `openai` or `anthropic` |
| `APIFY_API_TOKEN` | For job ingestion |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` | For Google sign-in. The redirect URI is `<api origin>/api/v1/auth/google/callback` and must match the Google Cloud Console entry |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `S3_BUCKET_NAME` | Optional resume file storage |
| `SENTRY_DSN` | Optional |

## Web variables

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | The API origin without a path, for example `https://api.example.com` |
| `NEXT_PUBLIC_APP_URL` | The web origin |

## GitHub Actions secrets

The workflows use the `production` environment and expect `RAILWAY_TOKEN`,
`DATABASE_URL`, `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`,
`NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_APP_URL`. `deploy.yml` and
`deploy-api.yml` deploy to Railway services named `jobsense-api` and
`jobsense-worker`.

## Check a deployment

```bash
curl https://<api origin>/health
```

The response reports the environment and whether Redis answered. Interactive API
documentation is at `/docs`.
