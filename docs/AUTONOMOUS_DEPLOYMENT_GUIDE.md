# Autonomous GitHub Pages & Edge Deployment Guide

This guide details how to run the project with **100% autonomy**, zero monthly hosting fees, and zero dependency on a fragile single origin server.

---

## 1. Automated GitHub Pages Deployment (Frontend & Static Core)

The repository includes a ready-to-run GitHub Actions workflow:
[`.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml)

### How It Updates Automatically & Instantly:
1. **Instant On Commit (`push: [main]`)**: Any change or new release committed to `web/` deploys live to GitHub Pages within ~60 seconds.
2. **Instant On Pipeline Completion (`workflow_run`)**: When the hourly episode generation pipeline (`publish-episode.yml`) finishes creating new episodes, it triggers Pages deployment immediately.
3. **Daily Scheduled Heartbeat (`schedule: '0 4 * * *'`)**: Runs automatically at 04:00 UTC every single day, keeping all manifests, cached assets, and builds fresh.
4. **Manual Dispatch (`workflow_dispatch`)**: Can be triggered manually at any moment with one click in the GitHub Actions tab.

### Enabling GitHub Pages in Your Repo:
1. Go to your repository on GitHub.
2. Navigate to **Settings** → **Pages**.
3. Under **Build and deployment** → **Source**, select **GitHub Actions**.
4. That's it! Every push or hourly release will deploy automatically.

---

## 2. Autonomous Edge Backend: Cloudflare Workers + D1 (SQLite)

When you need dynamic features (payments, subscriptions, licenses, user ratings, or private audio streaming) to survive if your main server ever goes down, the ideal solution is **Edge SQLite**.

### Why Cloudflare D1 + Workers?
* **D1 is real SQLite**: Global, fast, replicated SQLite database.
* **100% Serverless**: No virtual machines, no Docker, no maintenance, no patching.
* **Free Tier**:
  * Cloudflare Workers: 100,000 requests / day free.
  * Cloudflare D1 (SQLite): 5,000,000 read units / day free, 100,000 write units / day free.
  * Cloudflare R2 (Audio storage): 10 GB free storage, zero egress fees (unlimited free bandwidth).

---

## 3. Edge Architecture Blueprint

```
┌────────────────────────────────┐        ┌──────────────────────────────────┐
│   GitHub Pages (Frontend)      │        │  Cloudflare Worker (Edge API)    │
│  - Static UI, Audio Player     │───────▶│  - Handles /api/pay & webhooks   │
│  - Episode Manifests & Text    │        │  - Validates Square / Crypto     │
│  - High-Speed CDN Caching      │        │  - Issues signed streaming URLs  │
└────────────────────────────────┘        └─────────────────┬────────────────┘
                                                            │
                                        ┌───────────────────┴────────────────┐
                                        ▼                                    ▼
                          ┌───────────────────────────┐        ┌───────────────────────────┐
                          │   Cloudflare D1 (SQLite)  │        │   Cloudflare R2 Storage   │
                          │   - Orders & Licenses     │        │   - Full protected MP3s   │
                          │   - Supporter records     │        │   - Zero egress cost      │
                          └───────────────────────────┘        └───────────────────────────┘
```

### Database Schema (`schema.sql`):
```sql
CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,         -- 'square' or 'crypto'
  tier TEXT NOT NULL,             -- 'track', 'pack10', 'month', 'year'
  amount_cents INTEGER NOT NULL,
  currency TEXT DEFAULT 'USD',
  status TEXT NOT NULL,           -- 'pending', 'paid', 'expired'
  device_id TEXT,
  license_key TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  paid_at DATETIME
);

CREATE TABLE IF NOT EXISTS licenses (
  license_key TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  tier TEXT NOT NULL,
  valid_until DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ratings (
  episode_id TEXT NOT NULL,
  device_id TEXT NOT NULL,
  stars INTEGER CHECK(stars BETWEEN 1 AND 5),
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (episode_id, device_id)
);
```

### Worker Entrypoint Example (`worker.js`):
```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // CORS headers for GitHub Pages
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // 1. Status / Pricing Catalog
    if (url.pathname === '/api/catalog') {
      return Response.json({
        ok: true,
        plans: [
          { id: 'single', title: 'Single Release', cents: 25 },
          { id: 'monthly', title: 'Monthly Pass', cents: 199 },
          { id: 'annual', title: 'Annual Supporter', cents: 1499 }
        ]
      }, { headers: corsHeaders });
    }

    // 2. Square Webhook Listener
    if (url.pathname === '/api/webhooks/square' && request.method === 'POST') {
      const event = await request.json();
      if (event.type === 'payment.updated' && event.data.object.payment.status === 'COMPLETED') {
        const orderId = event.data.object.payment.order_id;
        // Mark order paid in D1 SQLite
        await env.DB.prepare('UPDATE orders SET status = ? WHERE id = ?')
          .bind('paid', orderId)
          .run();
      }
      return new Response('OK', { status: 200 });
    }

    // 3. Issue 6-hour temporary streaming ticket for audio
    if (url.pathname === '/api/ticket' && request.method === 'GET') {
      const episodeId = url.searchParams.get('id');
      const licenseKey = request.headers.get('Authorization')?.replace('Bearer ', '');

      const lic = await env.DB.prepare('SELECT * FROM licenses WHERE license_key = ?')
        .bind(licenseKey)
        .first();

      if (!lic) {
        return Response.json({ ok: false, error: 'License required' }, { status: 403, headers: corsHeaders });
      }

      // Generate signed R2 streaming URL valid for 6 hours
      const ticketUrl = `https://media.yourdomain.com/full/${episodeId}.mp3?token=signed_token`;
      return Response.json({ ok: true, streamUrl: ticketUrl }, { headers: corsHeaders });
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
  }
};
```

---

## 4. Setup in 3 Commands (When Ready to Deploy Edge Worker)
1. Install Wrangler CLI: `npm install -g wrangler`
2. Create D1 SQLite database: `wrangler d1 create zerofilter-db`
3. Deploy Worker: `wrangler deploy`

This gives your projects bulletproof survivability: even if your home server, VPS, or primary host goes offline, the GitHub Pages portal + Cloudflare SQLite Worker continue operating 24/7/365 without missing a single beat or transaction.
