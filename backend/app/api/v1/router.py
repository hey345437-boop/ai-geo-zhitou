from fastapi import APIRouter
from app.api.v1.endpoints import (
    research,
    probes,
    experiments,
    content,
    optimization,
    citations,
    cost,
    question_sets,
    causal_experiments,
    bandit,
    stores,
    business_impact,
    integrations,
    evaluation,
    recommendations,
)

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    research.router,
    prefix="/research",
    tags=["LLM Visibility Research"]
)

api_router.include_router(
    probes.router,
    prefix="/probes",
    tags=["Probes"]
)

api_router.include_router(
    experiments.router,
    prefix="/experiments",
    tags=["Experiments"]
)

api_router.include_router(
    content.router,
    prefix="/content",
    tags=["Content Analysis"]
)

api_router.include_router(
    optimization.router,
    prefix="/optimization",
    tags=["Optimization"]
)

api_router.include_router(
    citations.router,
    prefix="/citations",
    tags=["Citations"]
)

api_router.include_router(
    cost.router,
    prefix="/cost",
    tags=["Cost Control"]
)

api_router.include_router(
    question_sets.router,
    prefix="/question-sets",
    tags=["Question Sets"]
)

api_router.include_router(
    causal_experiments.router,
    prefix="/causal-experiments",
    tags=["Causal Experiments"]
)

api_router.include_router(
    bandit.router,
    prefix="/bandit",
    tags=["Multi-Armed Bandit"]
)

api_router.include_router(
    stores.router,
    prefix="/stores",
    tags=["Store & NAP Management"]
)

api_router.include_router(
    business_impact.router,
    prefix="/business-impact",
    tags=["Business Impact Tracking"]
)

api_router.include_router(
    integrations.router,
    prefix="/integrations",
    tags=["Workflow & Integrations"]
)

api_router.include_router(
    evaluation.router,
    prefix="/evaluation",
    tags=["Evaluation Protocol"]
)

api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Optimization & Recommendations"]
)
