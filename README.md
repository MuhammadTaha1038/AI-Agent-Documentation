# AI-Powered Natural Language ERP Agent

**A Multi-Provider Conversational Intelligence System for Enterprise Resource Planning**

> An intelligent conversational agent that understands natural language queries about enterprise data, automatically selects the optimal AI provider, and returns contextually-aware responses with real-time cost and performance tracking.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Usage Guidelines](#usage-guidelines)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Monitoring & Analytics](#monitoring--analytics)
- [Deployment](#deployment)
- [Research & Development](#research--development)

---

## Project Overview

### Problem Statement

Enterprise Resource Planning (ERP) systems are powerful but complex. Users must navigate intricate UI hierarchies, remember specific field names, and understand workflow sequences. Meanwhile, multiple Large Language Model (LLM) providers exist with varying capabilities, costs, and quota limitations.

### Solution

**AI-Powered Natural Language ERP Agent** is an intelligent middleware that:

1. **Understands intent** — Classifies user queries into actionable categories (data retrieval, explanation, guidance)
2. **Routes efficiently** — Dynamically selects the optimal AI provider (OpenAI, Google Gemini, Anthropic, Grok) based on:
   - Tenant policies and preferences
   - Provider health and available quota
   - Cost optimization and response time
3. **Retrieves data securely** — Queries internal ERP APIs with user's own authentication token (no direct DB access)
4. **Tracks economics** — Logs every API call with provider, tokens, cost, latency, and success status
5. **Monitors health** — Real-time dashboard showing provider status, usage forecasts, and budget alerts

### Real-World Use Case

**School Administrator:**
> "How many students failed in Mathematics this term?"

The agent:
- Classifies intent as `DATA_QUERY`
- Routes to lowest-cost available provider (Grok or Anthropic)
- Fetches exam performance data via `/analytics/exam-performance`
- Formats response naturally: "12 students failed Math (8.5% of 141 total)"
- Logs cost ($0.0012), latency (280ms), tokens used (45 input, 28 output)

**School Admin Dashboard:**
- Views real-time cost ($12.34 of $50 budget used this month)
- Sees provider health (Gemini: 15/20 quota remaining, OpenAI: healthy, Anthropic: healthy)
- Gets forecast: "Budget will be exhausted in 18 days at current usage rate"

---

## Key Features

### 1. **Multi-Provider Intelligence**
- **Supported Providers:** OpenAI (GPT-4), Google Gemini, Anthropic (Claude), Grok
- **Dynamic Selection:** Picks optimal provider per query based on health, cost, and performance
- **Automatic Fallback:** If primary provider quota exceeded, seamlessly switches to secondary
- **Intelligent Degradation:** Falls back to heuristic intent detection + knowledge base if all providers unavailable

### 2. **Intent Classification Pipeline**
- **4 Intent Categories:**
  - `DATA_QUERY` — Requests actual school data (students, fees, attendance, exam results)
  - `EXPLANATION` — "How does the fee module work?"
  - `HOW_TO` — Step-by-step procedural guidance (adding students, marking attendance)
  - `UNKNOWN` — Out-of-domain queries
- **Multi-Provider Classification:** Primary provider classifies intent; falls back to heuristic if unavailable

### 3. **Secure Data Access**
- **Zero Direct DB Access:** Agent forwards user's JWT token to internal REST APIs
- **Tenant Isolation:** Each user sees only their organization's data (enforced by existing auth layer)
- **Audit Trail:** Every data request logged for compliance and debugging

### 4. **Comprehensive Cost Tracking**
- **Per-Query Analytics:** Each response includes:
  - Provider used, model, tokens (input/output), cost in USD
  - Latency (ms), timestamp, success/failure status
  - Applied parameters (temperature, maxTokens, topP)
- **Aggregated Reporting:**
  - Monthly budget consumption by provider
  - Cost trends and forecasting
  - Per-tenant spending analysis

### 5. **Real-Time Monitoring Dashboard**
- **Provider Health Panel:** Status, quota remaining, error rates for each provider
- **Usage Forecasting:** Predicts monthly costs based on current trends
- **Budget Alerts:** Color-coded warnings (critical/warning/normal) when approaching limits
- **Performance Metrics:** Average latency, performance grading, optimization recommendations

### 6. **Embedded UI Components**
- **Floating Chat Widget:** Always-accessible AI assistant in any page
- **Full-Screen Chat Interface:** Dedicated `/ai-assistant` route
- **Model Selector:** Users can choose preferred AI model if multiple available
- **Usage Panel:** Real-time visualization of cost, tokens, and provider health
- **Parameter Inspector:** View exact settings (temperature, topP, etc.) used per response

---

## Architecture

### High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER APPLICATION                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Floating Chat Widget / Full-Screen Interface               │   │
│  │ Sends: { message, history }                                │   │
│  └────────────────────────────┬────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                    POST /api/v1/ai-assistant/chat
                    Authorization: Bearer <JWT>
                                 │
┌─────────────────────────────────────────────────────────────────────┐
│                       AI ASSISTANT BACKEND                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ AiAssistantController                                        │  │
│  │ • Extracts JWT token and tenant context from request        │  │
│  │ • Validates auth guards                                     │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│  ┌────────────────────────▼─────────────────────────────────────┐  │
│  │ AiAssistantService.chat(message, history)                   │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│       ┌───────────────────┼───────────────────┐                    │
│       │                   │                   │                    │
│  ┌────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐             │
│  │ Provider  │   │ Intent          │  │ Context     │             │
│  │ Router    │   │ Classifier      │  │ Retriever   │             │
│  │           │   │                 │  │             │             │
│  │ Checks:   │   │ Calls selected  │  │ If DATA_QY: │             │
│  │ • Tenant  │   │ provider to     │  │ Queries:    │             │
│  │   policy  │   │ classify intent │  │ /students   │             │
│  │ • Health  │   │                 │  │ /fees       │             │
│  │ • Quota   │   │ Falls back to   │  │ /attendance │             │
│  │ • Cost    │   │ heuristic if    │  │ /analytics  │             │
│  │           │   │ provider fails  │  │             │             │
│  └────┬──────┘   └────────┬────────┘  └──────┬──────┘             │
│       │                   │                   │                    │
│       └───────────────────┼───────────────────┘                    │
│                           │                                         │
│  ┌────────────────────────▼─────────────────────────────────────┐  │
│  │ Response Generator ([*]Adapter)                              │  │
│  │ • Calls selected provider (OpenAI/Gemini/Anthropic/Grok)    │  │
│  │ • Sends: intent + context + message + history               │  │
│  │ • On quota error (429): tries next provider in fallback    │  │
│  │   chain                                                     │  │
│  │ • Returns: response + metadata (tokens, cost, latency)     │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│  ┌────────────────────────▼─────────────────────────────────────┐  │
│  │ Usage Logger (AiUsageLedger)                                 │  │
│  │ • Records: provider, model, tokens, cost, latency,          │  │
│  │   status, timestamp, tenant_id, user_id                     │  │
│  │ • Updates: provider quota, tenant monthly spend             │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
└───────────────────────────┼─────────────────────────────────────────┘
                            │
                Return JSON Response:
                {
                  response: "...",
                  metadata: {
                    provider: "openai",
                    tokens: 198,
                    cost: $0.0023,
                    latency: 1240ms,
                    ...
                  }
                }
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                       USER APPLICATION                              │
│ • Renders response in chat UI                                       │
│ • Updates usage panel with cost/tokens/provider info               │
│ • Shows provider health status                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Module Interactions

```
┌──────────────────────────────────────────────────────────────────────┐
│                  AI ASSISTANT MODULE (ai-assistant)                  │
│                                                                      │
│  Controllers:                                                       │
│  └─ AiAssistantController (/api/v1/ai-assistant/chat)              │
│                                                                      │
│  Services:                                                          │
│  ├─ AiAssistantService (orchestration)                             │
│  │  ├─ Dependencies: [*]Adapter, ERP REST APIs, KnowledgeBase     │
│  │  └─ Methods: chat(), retrieveErpData(), formatResponse()       │
│  │                                                                 │
│  ├─ KnowledgeBaseService (offline explanations/guides)             │
│  │  ├─ 27 JSON files (modules, how-to guides)                     │
│  │  └─ Methods: searchExplanation(), searchHowTo()                │
│  │                                                                 │
│  └─ HeuristicIntentDetection (fallback classification)             │
│     └─ Methods: classifyByKeywords()                              │
└──────────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
┌───────────────▼──────────────────────┐  ┌────▼──────────────────────┐
│  AI PROVIDER MANAGEMENT MODULE       │  │  MONITORING MODULE         │
│  (ai-provider-management)            │  │  (ai-provider-management)  │
│                                      │  │                            │
│  Controllers:                        │  │  Controllers:              │
│  └─ AiProviderAdminController        │  │  └─ AiMonitoringController │
│     (/api/v1/super-admin/ai-...) │  │     (/api/v1/super-admin/   │
│                                      │  │     ai-monitoring)         │
│  Services:                           │  │                            │
│  ├─ AiProviderRouter                │  │  Services:                 │
│  │  ├─ selectProvider()              │  │  ├─ AiMonitoringService   │
│  │  └─ getProviderHealth()           │  │  │  ├─ getMetrics()       │
│  │                                   │  │  │  ├─ getForecasts()     │
│  ├─ [*]Adapter (provider abstraction)│  │  │  ├─ getBudgetAlerts()  │
│  │  ├─ GeminiAdapter                 │  │  │  └─ getPerformance()   │
│  │  ├─ OpenAiAdapter                 │  │  │                        │
│  │  ├─ AnthropicAdapter              │  │  └─ Provider health cache │
│  │  └─ GrokAdapter                   │  │                            │
│  │     Each has:                     │  │  Entities:                 │
│  │     • classifyIntent()            │  │  └─ Real-time monitoring   │
│  │     • generateResponse()          │  │     dashboard              │
│  │     • streamResponse()            │  │                            │
│  │                                   │  │                            │
│  ├─ AiUsageLedgerService            │  │                            │
│  │  └─ recordUsage(provider, tokens, │  │                            │
│  │     cost, latency, status)       │  │                            │
│  │                                   │  │                            │
│  └─ AiProviderAccountService        │  │                            │
│     └─ manage API keys & quotas     │  │                            │
└───────────────────────────────────────┘  └────────────────────────────┘
                │                                       │
                └───────────────┬───────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │  DATABASE              │
                    │                        │
                    │  Tables:               │
                    │  ├─ ai_usage_ledger   │
                    │  ├─ ai_providers      │
                    │  ├─ ai_provider_accts │
                    │  ├─ ai_tenant_policies│
                    │  └─ ai_provider_health│
                    │                        │
                    └────────────────────────┘
```

---

## Technology Stack

### Frontend
- **Framework:** Next.js 15.5.18 with React 19 (TypeScript)
- **State Management:** TanStack React Query v5 + Zustand
- **UI Components:** Radix UI primitives + Tailwind CSS
- **Chat Storage:** Browser localStorage (message history, user preferences)
- **Real-Time Updates:** React Query polling for cost/health metrics

### Backend
- **Runtime:** Node.js with NestJS 11.x (TypeScript)
- **HTTP Server:** Fastify adapter (high performance)
- **Database:** PostgreSQL 16 with Prisma v6.19.3 ORM
- **Authentication:** JWT RS256 (RS algorithms for better security)
- **Session Management:** httpOnly refresh token cookies

### External LLM Providers
| Provider | Model | API Endpoint | Auth | Cost |
|----------|-------|--------------|------|------|
| Google | Gemini 2.5 Flash Lite | `api.generativeai.google.com` | API Key | Free tier: ~20 req/day; paid: $0.075/M input, $0.30/M output |
| OpenAI | GPT-4 Turbo | `api.openai.com` | Bearer Token | $0.01/$0.03 per 1K tokens (input/output) |
| Anthropic | Claude 3 Sonnet | `api.anthropic.com` | Bearer Token | $0.003/$0.015 per 1K tokens (input/output) |
| Grok | Grok 2 Latest | `api.x.ai` | Bearer Token | $0.002/$0.01 per 1K tokens (provisional) |

### Deployment & Monitoring
- **Containerization:** Docker + docker-compose
- **CI/CD:** GitHub Actions (automated builds & tests)
- **Monitoring:** Winston logs, structured JSON logging
- **Error Tracking:** Sentry (future enhancement)
- **Hosting:** AWS/GCP/DigitalOcean (docker-compatible)

---

## System Requirements

### Development Environment
- **Node.js:** v18.18.0 or higher
- **npm:** v9.0.0 or higher (or yarn/pnpm)
- **PostgreSQL:** 16.x
- **Docker:** 20.10+ (optional, for containerized deployment)

### Hardware Minimum
- **CPU:** 2 cores (4+ cores recommended for production)
- **RAM:** 2GB (4GB+ recommended)
- **Storage:** 5GB free disk space

### API Keys Required
- Google Gemini API key (or skip for Gemini)
- OpenAI API key (or skip for OpenAI)
- Anthropic API key (or skip for Claude)
- Grok API key (or skip for Grok)

*Note: You can start with just one provider; multi-provider routing is optional.*

---

## Installation Guide

### 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-erp-agent.git
cd ai-erp-agent
```

### 2. Install Dependencies

```bash
# Install root dependencies
npm install

# Install workspace dependencies
npm install -w apps/api
npm install -w apps/web
```

### 3. Environment Configuration

Create `.env.local` in project root:

```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/erp_db"

# JWT
JWT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...-----END RSA PRIVATE KEY-----"
JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...-----END PUBLIC KEY-----"
JWT_EXPIRY_MINUTES=15
JWT_REFRESH_EXPIRY_DAYS=7

# LLM Providers
GEMINI_API_KEY="AIzaSy..."
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GROK_API_KEY="xai-..."

# AI Config
AI_DEFAULT_PROVIDER="openai"  # Fallback if no tenant policy
AI_TEMPERATURE=0.2
AI_MAX_TOKENS=1000
AI_REQUEST_TIMEOUT_MS=30000

# Backend
API_PORT=3001
API_HOST="0.0.0.0"

# Frontend
NEXT_PUBLIC_API_URL="http://localhost:3001"
NEXT_PUBLIC_CHAT_HISTORY_LIMIT=50
```

### 4. Database Setup

```bash
# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate deploy

# Seed initial data (optional)
npx prisma db seed
```

### 5. Start Development Servers

```bash
# Terminal 1: Backend
cd apps/api
npm run start:dev

# Terminal 2: Frontend
cd apps/web
npm run dev
```

### 6. Verify Installation

- **Backend:** http://localhost:3001/api/v1/health
- **Frontend:** http://localhost:3000
- **Chat Widget:** Visible on any page after login

---

## Usage Guidelines

### For End Users

#### 1. Access the Chat Interface

**Option A: Floating Widget**
- Available on every page (bottom-right corner)
- Click to expand/collapse
- Remembers last 5 messages

**Option B: Full Screen**
- Navigate to `/ai-assistant`
- Larger UI, full conversation history
- Side panel shows real-time metrics

#### 2. Example Queries

```
Data Queries:
├─ "How many students passed the final exam?"
├─ "Show me fee defaulters from Class 10"
├─ "What's the attendance rate for this month?"
└─ "Which teachers are absent frequently?"

Explanations:
├─ "What is the attendance module?"
├─ "How does the fee system work?"
├─ "Explain the exam results page"
└─ "What are student admission statuses?"

How-To Guides:
├─ "How do I add a new student?"
├─ "How to mark attendance in bulk?"
├─ "How do I generate a fee slip?"
└─ "How to add exam marks?"

Out-of-Domain:
└─ "What's the weather?" → Politely declines & suggests related ERP queries
```

#### 3. Monitor Cost & Performance

**In Chat Widget:**
- View provider name and model used
- See token count (input/output) and cost
- Check monthly budget remaining
- View provider health status

**In Usage Panel:**
- Monthly budget vs. actual spend
- Cost per query
- Rate limits and quota
- Provider fallback chain status

### For Administrators

#### 1. Configure Provider Policies

Navigate to `/super-admin/ai-providers/policies`:

```
Tenant: "Lincoln School"
├─ Primary Provider: OpenAI (GPT-4 Turbo)
│  └─ Temperature: 0.2, Max Tokens: 1000
├─ Secondary Provider: Anthropic (Claude 3 Sonnet)
│  └─ Temperature: 0.2, Max Tokens: 1000
├─ Tertiary Provider: Gemini (2.5 Flash Lite)
│  └─ Temperature: 0.2, Max Tokens: 512
└─ Monthly Budget: $50.00
   └─ Alert Thresholds: Warning at 75%, Critical at 90%
```

#### 2. Monitor AI Usage

Navigate to `/super-admin/ai-monitoring`:

**Overall Metrics:**
- Total requests (24h, 7d, 30d)
- Total tokens used
- Total cost
- Success rate %

**Per-Provider Health:**
- Real-time status (healthy/degraded)
- Quota remaining
- Error rate
- Average response time

**Budget Forecasting:**
- Current period usage
- Projected monthly cost
- Days until budget exhausted
- Usage trend (increasing/stable/decreasing)

**Budget Alerts:**
- Critical: Budget will be exhausted within 3 days
- Warning: Budget at 75%+
- Normal: Budget healthy

---

## API Endpoints

### Chat API

#### `POST /api/v1/ai-assistant/chat`

**Authentication:** Required (JWT Bearer token)

**Request:**
```json
{
  "message": "How many students are in Class 10?",
  "history": [
    {
      "role": "user",
      "text": "Show me student statistics"
    },
    {
      "role": "assistant",
      "text": "Here are the student statistics..."
    }
  ]
}
```

**Response (200 OK):**
```json
{
  "response": "There are 42 students enrolled in Class 10 currently.",
  "metadata": {
    "provider": "openai",
    "model": "gpt-4-turbo",
    "modelDisplayName": "GPT-4 Turbo",
    "inputTokens": 128,
    "outputTokens": 15,
    "totalTokens": 143,
    "costUsd": 0.001287,
    "latencyMs": 1240,
    "status": "success",
    "failureReason": null,
    "appliedConfig": {
      "temperature": 0.2,
      "maxTokens": 1000,
      "topP": 0.95,
      "frequencyPenalty": 0,
      "presencePenalty": 0
    },
    "usagePanel": {
      "monthlyBudgetUsd": 50.00,
      "monthlyUsedUsd": 12.34,
      "remainingUsd": 37.66,
      "percentUsed": 24.68,
      "requestsThisMonth": 432,
      "rateLimit": "100 requests/minute"
    },
    "providerHealth": {
      "status": "healthy",
      "quotaRemaining": 95000,
      "quotaTotal": 100000,
      "lastHealthCheck": "2026-06-07T16:30:00Z"
    }
  }
}
```

**Error Responses:**

```json
// 401 Unauthorized
{
  "statusCode": 401,
  "message": "Invalid or expired token",
  "error": "Unauthorized"
}

// 429 All Providers Quota Exceeded
{
  "statusCode": 429,
  "message": "All AI providers currently at quota. Please try again later.",
  "error": "ServiceUnavailable",
  "retryAfter": 3600
}

// 500 Internal Error
{
  "statusCode": 500,
  "message": "Failed to generate response. Using fallback response.",
  "response": "I was unable to process your request with AI providers, but here's what I found: [static knowledge base response]",
  "metadata": {
    "status": "fallback",
    "reason": "All providers unavailable"
  }
}
```

### Monitoring API

#### `GET /api/v1/super-admin/ai-monitoring`

**Query Parameters:**
- `tenant` (optional): "all" | tenantId (default: "all")
- `range` (optional): "24h" | "7d" | "30d" (default: "30d")

**Response:**
```json
{
  "overallMetrics": {
    "totalRequests": 1243,
    "totalTokensUsed": 156789,
    "totalCostUsd": 23.45,
    "avgResponseTimeMs": 847,
    "successRate": 98.5
  },
  "providerMetrics": [
    {
      "provider": "openai",
      "healthy": true,
      "requests": 623,
      "errors": 8,
      "quotaRemaining": 95000,
      "quotaTotal": 100000,
      "avgResponseTime": 920
    },
    {
      "provider": "gemini",
      "healthy": true,
      "requests": 380,
      "errors": 2,
      "quotaRemaining": 15,
      "quotaTotal": 20,
      "avgResponseTime": 640
    },
    {
      "provider": "anthropic",
      "healthy": true,
      "requests": 240,
      "errors": 3,
      "quotaRemaining": 87500,
      "quotaTotal": 100000,
      "avgResponseTime": 780
    }
  ],
  "budgetAlerts": [
    {
      "tenantId": "tenant-1",
      "tenantName": "Lincoln School",
      "monthlyBudget": 50.00,
      "monthlyUsed": 38.50,
      "percentUsed": 77.0,
      "daysRemaining": 9,
      "severity": "warning"
    }
  ]
}
```

#### `GET /api/v1/super-admin/ai-usage-forecast`

**Query Parameters:**
- `tenant` (optional): "all" | tenantId
- `range` (optional): "24h" | "7d" | "30d"

**Response:**
```json
{
  "currentUsage": 12.34,
  "projectedMonthlyUsage": 26.78,
  "projectedCost": 26.78,
  "trend": "increasing",
  "daysUntilBudgetExhausted": 18,
  "trendPercentageChange": 12.5
}
```

---

## Configuration

### Provider Selection Strategy

The agent selects providers based on this priority matrix:

```
┌─────────────────────────────────────────────────────────┐
│ PROVIDER SELECTION ALGORITHM                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. Tenant Policy Check                                  │
│    ├─ Does tenant have explicit provider preference?   │
│    └─ YES → Use preferred provider (if healthy)        │
│       NO  → Continue to step 2                         │
│                                                         │
│ 2. Cost Optimization (for low-risk queries)            │
│    └─ Select cheapest available provider               │
│       (if confidence score > 90%)                      │
│                                                         │
│ 3. Latency Optimization (for urgent queries)           │
│    └─ Select fastest available provider                │
│       (if confidence score > 80%)                      │
│                                                         │
│ 4. Health & Quota Check                                │
│    ├─ Is primary provider healthy?                     │
│    ├─ Does it have quota remaining?                    │
│    ├─ Is it within rate limits?                        │
│    └─ YES → Use it; NO → Try next in fallback chain   │
│                                                         │
│ 5. Fallback Chain                                       │
│    └─ Try secondary → tertiary → quaternary providers  │
│       (if configured)                                  │
│                                                         │
│ 6. Graceful Degradation                                │
│    └─ If ALL providers unavailable:                    │
│       • Heuristic intent detection (no LLM)           │
│       • Return knowledge base response                 │
│       • OR cached fallback response                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Model Configuration

Each provider supports parameter tuning via tenant policies:

```typescript
interface ProviderConfig {
  temperature: 0.0–2.0;      // 0.2 (deterministic) recommended for factual data
  maxTokens: 1–2000;         // 1000 typical max for ERP queries
  topP: 0.0–1.0;             // 0.95 (default, allows diverse outputs)
  frequencyPenalty: 0.0–2.0; // 0 (neutral, no frequency bias)
  presencePenalty: 0.0–2.0;  // 0 (neutral, no presence bias)
}
```

**Recommended for ERP (Data Queries):**
```json
{
  "temperature": 0.2,
  "maxTokens": 1000,
  "topP": 0.95,
  "frequencyPenalty": 0,
  "presencePenalty": 0
}
```

---

## Monitoring & Analytics

### Real-Time Dashboards

#### 1. User Dashboard (Floating Widget & Chat)
- Current provider + model
- Cost of this response
- Tokens used
- Response latency
- Provider health status
- Monthly budget remaining

#### 2. Admin Dashboard (`/super-admin/ai-monitoring`)
- 4-card metrics grid:
  - Total Requests (24h/7d/30d)
  - Total Tokens Used
  - Total Cost (USD)
  - Success Rate (%)
- Provider Health Panel with quota bars
- Usage Forecasting graph
- Budget Alert list (by severity)
- Performance Metrics gauge

### Metrics Collected

**Per Request:**
- `provider` — Which LLM was used
- `model` — Specific model version
- `intent` — Classified intent type
- `inputTokens`, `outputTokens` — Token counts
- `costUsd` — Computed cost
- `latencyMs` — End-to-end time
- `status` — success | error | fallback
- `failureReason` — If status != success
- `timestamp` — ISO 8601 UTC
- `tenantId`, `userId` — For segmentation

**Aggregated Daily/Monthly:**
- Cost per provider
- Cost per tenant
- Success rate trend
- Latency p50/p95/p99
- Token burn rate
- Provider error rates

### Alerts & Notifications

**Real-Time Alerts:**
- Provider quota exhausted (429) → Try fallback
- Response latency >2s → Log warning
- Cost anomaly detected → Notify admin
- Budget forecast exceeded → Email alert
- Provider health check failed → Mark degraded

**Admin Notifications (Weekly):**
- Usage summary & cost report
- Provider performance comparison
- Forecast accuracy check
- Quota utilization per provider

---

## Deployment

### Docker Deployment

```dockerfile
# Build image
docker build -t ai-erp-agent:latest .

# Run with docker-compose
docker-compose up -d
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: erp_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: .
      dockerfile: apps/api/Dockerfile
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/erp_db
      JWT_PRIVATE_KEY: ${JWT_PRIVATE_KEY}
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "3001:3001"
    depends_on:
      - postgres

  frontend:
    build:
      context: .
      dockerfile: apps/web/Dockerfile
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:3001
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Cloud Deployment (AWS ECS)

1. Push image to ECR
2. Create ECS Task Definition
3. Launch ECS Service with ALB
4. Configure RDS PostgreSQL
5. Set environment variables in ECS Task
6. Configure CloudWatch monitoring

---

## Research & Development

### Academic Use Cases

This project demonstrates:

1. **Multi-Agent Architecture** — Dynamic provider selection based on real-time constraints
2. **Intent Classification Pipeline** — NLP-based intent detection with fallback heuristics
3. **Cost Optimization Algorithms** — Selecting providers based on cost-quality-latency tradeoff
4. **Distributed Systems** — Coordinating multiple external LLM APIs with fallback chains
5. **Real-Time Analytics** — Monitoring and forecasting cost trends
6. **Security & Auth** — JWT-based isolation, no direct DB access

### Key Research Questions

- How to optimally route requests across multiple LLM providers?
- How accurate is heuristic fallback vs. LLM-based intent classification?
- What cost savings can dynamic provider selection achieve vs. single-provider?
- How does temperature/maxTokens affect accuracy for ERP data queries?
- Can latency forecasting improve user experience?

### Extension Ideas

- [ ] Fine-tune provider selection using reinforcement learning
- [ ] Add semantic caching to reduce tokens and cost
- [ ] Implement streaming responses for long-form queries
- [ ] Build custom ORCA-style distilled model for fallback
- [ ] Add multi-language support with automatic translation
- [ ] Implement document-level RAG for knowledge base
- [ ] Add voice input/output (speech-to-text & text-to-speech)

---

## License

MIT License — See LICENSE file for details

## Support

For questions, issues, or contributions:
- **GitHub Issues:** https://github.com/your-username/ai-erp-agent/issues
- **Email:** your-email@example.com
- **Documentation:** Full technical docs in `TECHNICAL.md`

---

**Last Updated:** June 7, 2026  
**Version:** 1.0.0 (Phase 5 — Monitoring Dashboard Complete)
