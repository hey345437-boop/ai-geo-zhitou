# 智投 API Documentation

**Version**: 5.0.0  
**Base URL**: `http://localhost:8000/api/v1`  
**Authentication**: JWT Bearer Token

---

## Table of Contents

1. [Authentication](#authentication)
2. [LLM Visibility Research](#llm-visibility-research)
3. [Probes](#probes)
4. [Citations](#citations)
5. [Cost Control](#cost-control)
6. [Question Sets](#question-sets)
7. [Causal Experiments](#causal-experiments)
8. [Multi-Armed Bandit](#multi-armed-bandit)
9. [Business Impact](#business-impact)
10. [Integrations](#integrations)
11. [Stores & NAP](#stores--nap)
12. [Evaluation Protocol](#evaluation-protocol)
13. [Recommendations](#recommendations)

---

## Authentication

All API requests require authentication using JWT tokens.

### Get Access Token

```http
POST /auth/token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Using the Token

Include the token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## LLM Visibility Research

### Analyze Visibility

Analyze brand visibility across LLM engines.

```http
POST /research/analyze
Content-Type: application/json

{
  "category": "restaurants",
  "brand_name": "Example Restaurant",
  "competitors": ["Competitor A", "Competitor B"],
  "engines": ["gpt4", "claude3", "gemini"],
  "question_count": 10
}
```

**Response**:
```json
{
  "analysis_id": "analysis_123",
  "status": "completed",
  "share_of_model": {
    "Example Restaurant": 45.5,
    "Competitor A": 30.2,
    "Competitor B": 24.3
  },
  "cognitive_gaps": [
    {
      "gap_type": "underserved_segment",
      "description": "Vegan options queries",
      "opportunity_score": 85
    }
  ],
  "strategies": [
    {
      "strategy": "Content Enhancement",
      "positioning": "Emphasize vegan menu",
      "expected_outcome": "+15% visibility"
    }
  ]
}
```

---

## Probes

### Create Probe

Create a new monitoring probe.

```http
POST /probes/create
Content-Type: application/json

{
  "name": "Restaurant Visibility Probe",
  "brand_id": "brand_123",
  "engines": ["gpt4", "claude3"],
  "questions": ["Best Italian restaurants in NYC"],
  "schedule": "0 */6 * * *"
}
```

### Get Probe Results

```http
GET /probes/{probe_id}/results?timeframe=7d
```

**Response**:
```json
{
  "probe_id": "probe_123",
  "results": [
    {
      "timestamp": "2026-02-12T10:00:00Z",
      "engine": "gpt4",
      "visibility_score": 75.5,
      "mention_rate": 80.0,
      "position_score": 85.0
    }
  ],
  "summary": {
    "avg_visibility_score": 75.5,
    "trend": "improving"
  }
}
```

---

## Citations

### Extract Citations

Extract citations from LLM responses.

```http
POST /citations/extract
Content-Type: application/json

{
  "text": "According to research from MIT...",
  "brand_id": "brand_123"
}
```

**Response**:
```json
{
  "citations": [
    {
      "type": "attribution",
      "text": "According to research from MIT",
      "credibility": "very_high",
      "position": "opening",
      "domain": "mit.edu"
    }
  ],
  "metrics": {
    "total_citations": 1,
    "avg_credibility": 0.95,
    "citation_rate": 0.8
  }
}
```

---

## Cost Control

### Check Budget

Check current budget status.

```http
GET /cost/check-budget?user_id=user_123
```

**Response**:
```json
{
  "user_id": "user_123",
  "tier": "pro",
  "monthly_limit": 500.00,
  "current_usage": 245.50,
  "remaining": 254.50,
  "warning_level": "normal"
}
```

### Get Cost Breakdown

```http
GET /cost/breakdown?user_id=user_123&month=2026-02
```

**Response**:
```json
{
  "total_cost": 245.50,
  "by_engine": {
    "gpt4": 150.00,
    "claude3": 75.50,
    "gemini": 20.00
  },
  "by_category": {
    "probes": 180.00,
    "research": 65.50
  }
}
```

---

## Evaluation Protocol

### Create Evaluation Run

```http
POST /evaluation/run
Content-Type: application/json

{
  "question_set_name": "restaurant_benchmark",
  "question_set_version": "v1.0",
  "engines": ["gpt4", "claude3"],
  "random_seed": 42
}
```

**Response**:
```json
{
  "run_id": "eval_run_123",
  "status": "completed",
  "metrics": {
    "avg_visibility_score": 75.5,
    "avg_citation_count": 3.2,
    "mention_rate": 80.0
  }
}
```

### Check Drift

```http
POST /evaluation/drift/check
Content-Type: application/json

{
  "baseline_run_id": "eval_run_100",
  "current_run_id": "eval_run_123"
}
```

**Response**:
```json
{
  "has_significant_drift": false,
  "overall_drift_score": 5.2,
  "drift_metrics": [
    {
      "metric_name": "avg_visibility_score",
      "baseline_value": 75.0,
      "current_value": 75.5,
      "drift_percentage": 0.67,
      "severity": "none"
    }
  ]
}
```

---

## Recommendations

### Generate Recommendations

```http
POST /recommendations/generate
Content-Type: application/json

{
  "project_id": "proj_123",
  "content_analysis": {
    "relevance_score": 65,
    "authority_score": 55,
    "structure_score": 70
  },
  "visibility_score": 60
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "type": "content_quality",
      "priority": "high",
      "title": "Improve Content Relevance",
      "description": "Content relevance score is 65%. Enhance content...",
      "expected_impact": 15.0,
      "effort_level": "medium"
    }
  ]
}
```

### Check Compliance

```http
POST /compliance/check
Content-Type: application/json

{
  "content_id": "content_123",
  "content": "Your content here...",
  "html": "<html>...</html>"
}
```

**Response**:
```json
{
  "compliance_score": 85.0,
  "is_compliant": true,
  "issues": [
    {
      "issue_type": "thin_content",
      "severity": "medium",
      "description": "Content is too short (250 words)",
      "fix_suggestion": "Expand content to at least 300 words"
    }
  ]
}
```

---

## Rate Limits

| Tier | Requests/Hour | Requests/Day |
|------|---------------|--------------|
| Free | 100 | 1,000 |
| Basic | 1,000 | 10,000 |
| Pro | 10,000 | 100,000 |
| Enterprise | Unlimited | Unlimited |

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

---

## Webhooks

Subscribe to events via webhooks.

### Configure Webhook

```http
POST /integrations/webhook
Content-Type: application/json

{
  "url": "https://your-domain.com/webhook",
  "events": ["visibility_change", "drift_detected"]
}
```

### Webhook Payload

```json
{
  "event": "visibility_change",
  "timestamp": "2026-02-12T10:00:00Z",
  "data": {
    "brand_id": "brand_123",
    "old_score": 70.0,
    "new_score": 75.5,
    "change_percentage": 7.86
  }
}
```

---

## SDKs

### Python SDK

```python
from geo_optimizer import Client

client = Client(api_key="your_api_key")

# Analyze visibility
result = client.research.analyze(
    category="restaurants",
    brand_name="Example Restaurant"
)

print(result.share_of_model)
```

### JavaScript SDK

```javascript
import { GeoOptimizer } from '@geo-optimizer/sdk';

const client = new GeoOptimizer({ apiKey: 'your_api_key' });

// Create probe
const probe = await client.probes.create({
  name: 'My Probe',
  engines: ['gpt4', 'claude3']
});
```

---

## Support

- **Documentation**: https://docs.geo-optimizer.com
- **API Status**: https://status.geo-optimizer.com
- **Support Email**: support@geo-optimizer.com
- **GitHub**: https://github.com/geo-optimizer

---

**Last Updated**: February 12, 2026
