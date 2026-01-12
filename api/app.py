from __future__ import annotations

import math
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="mai-tools-api",
    description="Programmatic access to maimai rating math used by mai-tools.",
    version="0.1.0",
)

# Enable CORS for browser-based clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


class RankDef(BaseModel):
    title: str
    min_achv: float = Field(..., description="Minimum achievement percentage that qualifies for this rank")
    factor: float = Field(..., description="Rating multiplier for this rank")
    max_achv: Optional[float] = Field(None, description="Upper bound of achievement for this rank, if any")
    max_factor: Optional[float] = Field(None, description="Multiplier to use when achievement hits the upper bound")


class RatingRequest(BaseModel):
    level: float = Field(..., description="Chart constant, e.g. 13.7")
    achievement: float = Field(..., description="Achievement percentage, e.g. 100.3")


class RatingResponse(BaseModel):
    rating: float
    rank_title: str
    capped_achievement: float


class RatingRangeRequest(BaseModel):
    level: float
    rank_title: str


class RatingRangeResponse(BaseModel):
    min_rating: int
    max_rating: int
    rank_title: str


class RecommendedLevelsRequest(BaseModel):
    rating: float = Field(..., description="Target total rating")


class RecommendedLevel(BaseModel):
    lv: float
    min_achv: float
    rating: int


MAX_LEVEL = 15

RANK_S = RankDef(min_achv=97.0, factor=0.2, title="S")
RANK_SSS_PLUS = RankDef(min_achv=100.5, factor=0.224, title="SSS+")

RANK_DEFINITIONS: List[RankDef] = [
    RANK_SSS_PLUS,
    RankDef(min_achv=100.0, factor=0.216, title="SSS", max_achv=100.4999, max_factor=0.222),
    RankDef(min_achv=99.5, factor=0.211, title="SS+", max_achv=99.9999, max_factor=0.214),
    RankDef(min_achv=99.0, factor=0.208, title="SS"),
    RankDef(min_achv=98.0, factor=0.203, title="S+", max_achv=98.9999, max_factor=0.206),
    RANK_S,
    RankDef(min_achv=94.0, factor=0.168, title="AAA", max_achv=96.9999, max_factor=0.176),
    RankDef(min_achv=90.0, factor=0.152, title="AA"),
    RankDef(min_achv=80.0, factor=0.136, title="A"),
    RankDef(min_achv=75.0, factor=0.12, title="BBB", max_achv=79.9999, max_factor=0.128),
    RankDef(min_achv=70.0, factor=0.112, title="BB"),
    RankDef(min_achv=60.0, factor=0.096, title="B"),
    RankDef(min_achv=50.0, factor=0.08, title="C"),
    RankDef(min_achv=0.0, factor=0.016, title="D"),
]


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/ranks", response_model=List[RankDef])
def list_ranks() -> List[RankDef]:
    return RANK_DEFINITIONS


def _get_rank_by_title(rank_title: str) -> Optional[RankDef]:
    for rank in RANK_DEFINITIONS:
        if rank.title.lower() == rank_title.lower():
            return rank
    return None


def _get_rank_by_achievement(achievement: float) -> Optional[RankDef]:
    for rank in RANK_DEFINITIONS:
        if achievement >= rank.min_achv:
            return rank
    return None


def _round_float(num: float, method: str, unit: float) -> float:
    if method == "floor":
        return math.floor(num / unit) * unit
    if method == "ceil":
        return math.ceil(num / unit) * unit
    if method == "round":
        return round(num / unit) * unit
    raise ValueError("Unsupported rounding method")


def calculate_rating(level: float, achievement: float) -> RatingResponse:
    capped_achievement = min(achievement, RANK_SSS_PLUS.min_achv)
    rank = _get_rank_by_achievement(capped_achievement)
    if not rank:
        raise HTTPException(status_code=400, detail="Could not find rank for achievement")
    positive_lv = abs(level)
    if rank.max_achv and rank.max_factor and math.isclose(rank.max_achv, capped_achievement):
        rating_val = positive_lv * rank.max_achv * rank.max_factor
    else:
        rating_val = positive_lv * capped_achievement * rank.factor
    return RatingResponse(rating=rating_val, rank_title=rank.title, capped_achievement=capped_achievement)


def calculate_rating_range(level: float, rank_title: str) -> RatingRangeResponse:
    rank = _get_rank_by_title(rank_title)
    if not rank:
        raise HTTPException(status_code=404, detail="Rank not found")
    idx = RANK_DEFINITIONS.index(rank)
    min_rating = math.floor(level * rank.min_achv * rank.factor)
    if rank.max_achv and rank.max_factor:
        max_rating = math.floor(level * rank.max_achv * rank.max_factor)
    else:
        max_achv = rank.min_achv
        if idx + 1 < len(RANK_DEFINITIONS):
            max_achv = RANK_DEFINITIONS[idx + 1].min_achv - 0.0001
        max_rating = math.floor(level * max_achv * rank.factor)
    return RatingRangeResponse(min_rating=min_rating, max_rating=max_rating, rank_title=rank.title)


def calculate_recommended_levels(target_rating: float) -> Dict[str, List[RecommendedLevel]]:
    target_rating = math.floor(target_rating)
    ranks_low_to_high = sorted(RANK_DEFINITIONS, key=lambda r: r.min_achv)
    levels_by_rank: Dict[str, List[RecommendedLevel]] = {}
    for idx, rank in enumerate(ranks_low_to_high):
        # Skip ranks with 0 min_achv to avoid division by zero
        if rank.min_achv == 0:
            continue
        max_lv = _round_float(target_rating / rank.factor / rank.min_achv, "ceil", 0.1)
        if max_lv > MAX_LEVEL:
            continue
        max_achv = rank.min_achv
        if idx + 1 < len(ranks_low_to_high):
            max_achv = ranks_low_to_high[idx + 1].min_achv - 0.0001
        levels: List[RecommendedLevel] = []
        while math.floor(max_lv * rank.factor * max_achv) >= target_rating:
            min_achv = max(_round_float(target_rating / rank.factor / max_lv, "ceil", 0.0001), rank.min_achv)
            levels.append(
                RecommendedLevel(
                    lv=round(max_lv, 1),
                    min_achv=min_achv,
                    rating=math.floor(max_lv * rank.factor * min_achv),
                )
            )
            max_lv = round(max_lv - 0.1, 10)
        levels.reverse()
        levels_by_rank[rank.title] = levels
    return levels_by_rank


@app.post("/rating", response_model=RatingResponse)
def api_rating(payload: RatingRequest) -> RatingResponse:
    return calculate_rating(payload.level, payload.achievement)


@app.post("/rating-range", response_model=RatingRangeResponse)
def api_rating_range(payload: RatingRangeRequest) -> RatingRangeResponse:
    return calculate_rating_range(payload.level, payload.rank_title)


@app.post("/recommended-levels", response_model=Dict[str, List[RecommendedLevel]])
def api_recommended_levels(payload: RecommendedLevelsRequest) -> Dict[str, List[RecommendedLevel]]:
    return calculate_recommended_levels(payload.rating)


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "mai-tools API is running",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
