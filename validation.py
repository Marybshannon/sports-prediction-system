"""
Validation and error-handling utilities for the sports prediction system.

Use these helpers before constructing Team and MatchPrediction instances so
invalid input is reported clearly instead of producing unreliable predictions.
"""

import logging
import math
import re
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


LOGGER = logging.getLogger("sports_prediction")


class ValidationError(ValueError):
    """Raised when user-provided prediction data is invalid."""


class TeamValidationError(ValidationError):
    """Raised when team data fails validation."""


class MatchValidationError(ValidationError):
    """Raised when match data fails validation."""


class PredictionValidationError(ValidationError):
    """Raised when a generated prediction is invalid."""


@dataclass(frozen=True)
class ValidationConfig:
    """Allowed ranges for prediction inputs."""

    rating_min: float = 0
    rating_max: float = 100
    injury_min: float = 0
    injury_max: float = 30
    crowd_min: float = 0.5
    crowd_max: float = 2.0
    luck_min: float = 0.3
    luck_max: float = 1.5
    goals_min: float = 0


DEFAULT_CONFIG = ValidationConfig()


def configure_logging(level=logging.INFO, log_file: Optional[str] = None):
    """Configure console logging and optionally a file handler.

    Applications can call this once at startup. Library imports do not alter
    the application's global logging configuration.
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=level,
        handlers=handlers,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{field} must be a number")
    if not math.isfinite(float(value)):
        raise ValidationError(f"{field} must be finite")
    return float(value)


def _range(value: Any, field: str, minimum: float, maximum: float):
    value = _number(value, field)
    if not minimum <= value <= maximum:
        raise ValidationError(f"{field} must be between {minimum} and {maximum}")
    return value


def validate_team_data(team: Mapping[str, Any], config: ValidationConfig = DEFAULT_CONFIG) -> Dict[str, Any]:
    """Validate and return a sanitized copy of a team mapping."""
    if not isinstance(team, Mapping):
        raise TeamValidationError("Team data must be a mapping")

    name = str(team.get("name", "")).strip()
    if not name or len(name) > 120:
        raise TeamValidationError("Team name must contain 1-120 characters")
    if not re.search(r"[\wÀ-ÿ]", name, re.UNICODE):
        raise TeamValidationError("Team name must contain a letter or number")

    try:
        clean = dict(team)
        clean["name"] = name
        clean["rating"] = _range(team.get("rating", 70), "rating", config.rating_min, config.rating_max)
        clean["recent_form"] = _range(team.get("recent_form", 70), "recent_form", config.rating_min, config.rating_max)
        clean["manager_rating"] = _range(team.get("manager_rating", 75), "manager_rating", config.rating_min, config.rating_max)
        clean["mental_strength"] = _range(team.get("mental_strength", 75), "mental_strength", config.rating_min, config.rating_max)
        clean["injury_level"] = _range(team.get("injury_level", 0), "injury_level", config.injury_min, config.injury_max)
        clean["goals_for"] = _range(team.get("goals_for", 1.5), "goals_for", config.goals_min, 100)
        clean["goals_against"] = _range(team.get("goals_against", 1.5), "goals_against", config.goals_min, 100)
        clean["crowd_strength"] = _range(team.get("crowd_strength", 1.0), "crowd_strength", config.crowd_min, config.crowd_max)
        clean["luck_factor"] = _range(team.get("luck_factor", 0.5), "luck_factor", config.luck_min, config.luck_max)
    except ValidationError as exc:
        raise TeamValidationError(str(exc)) from exc

    return clean


def validate_h2h_record(record: Optional[Mapping[str, Any]]) -> Dict[str, int]:
    """Validate a head-to-head record and return integer counts."""
    record = record or {"home_wins": 0, "away_wins": 0, "draws": 0}
    if not isinstance(record, Mapping):
        raise MatchValidationError("Head-to-head record must be a mapping")
    clean = {}
    for key in ("home_wins", "away_wins", "draws"):
        value = record.get(key, 0)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise MatchValidationError(f"{key} must be a non-negative integer")
        clean[key] = value
    return clean


def validate_match_data(home_team: Mapping[str, Any], away_team: Mapping[str, Any],
                        h2h_record=None, chaos_probability=0.35) -> Dict[str, Any]:
    """Validate match inputs, including teams, H2H data, and chaos probability."""
    home = validate_team_data(home_team)
    away = validate_team_data(away_team)
    if home["name"].casefold() == away["name"].casefold():
        raise MatchValidationError("Home and away teams must be different")
    probability = _range(chaos_probability, "chaos_probability", 0, 1)
    return {"home_team": home, "away_team": away,
            "head_to_head_record": validate_h2h_record(h2h_record),
            "chaos_probability": probability}


def validate_prediction(prediction: Mapping[str, Any]) -> Dict[str, Any]:
    """Validate a prediction result before storing or displaying it."""
    if not isinstance(prediction, Mapping):
        raise PredictionValidationError("Prediction must be a mapping")
    winner = prediction.get("winner")
    if winner not in {"Home Win", "Away Win", "Draw"}:
        raise PredictionValidationError("winner must be Home Win, Away Win, or Draw")
    try:
        confidence = _range(prediction.get("confidence"), "confidence", 0, 1)
        home_goals = _range(prediction.get("home_goals", 0), "home_goals", 0, 1000)
        away_goals = _range(prediction.get("away_goals", 0), "away_goals", 0, 1000)
    except ValidationError as exc:
        raise PredictionValidationError(str(exc)) from exc
    result = dict(prediction)
    result.update(confidence=confidence, home_goals=int(home_goals), away_goals=int(away_goals))
    return result


def safe_validate(function, *args, **kwargs):
    """Run a validator and log failures before re-raising them."""
    try:
        return function(*args, **kwargs)
    except ValidationError:
        LOGGER.exception("Validation failed in %s", getattr(function, "__name__", function))
        raise


__all__ = [
    "ValidationError", "TeamValidationError", "MatchValidationError",
    "PredictionValidationError", "ValidationConfig", "configure_logging",
    "validate_team_data", "validate_h2h_record", "validate_match_data",
    "validate_prediction", "safe_validate",
]
