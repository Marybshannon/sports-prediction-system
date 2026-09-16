"""Validated adapters for the sports prediction engine.

These classes keep the original prediction_engine API while validating inputs
before the engine performs calculations. Existing scripts can continue using
prediction_engine.Team and prediction_engine.MatchPrediction unchanged, or
adopt these safer adapters for user-supplied data.
"""

from prediction_engine import MatchPrediction as BaseMatchPrediction
from prediction_engine import Team as BaseTeam
from validation import validate_match_data, validate_prediction, validate_team_data


class ValidatedTeam(BaseTeam):
    """Team that validates and sanitizes all constructor values."""

    def __init__(self, name, rating, recent_form, goals_for, goals_against,
                 injury_level=0, manager_rating=75, crowd_strength=1.0,
                 mental_strength=75, luck_factor=0.5):
        data = validate_team_data({
            "name": name,
            "rating": rating,
            "recent_form": recent_form,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "injury_level": injury_level,
            "manager_rating": manager_rating,
            "crowd_strength": crowd_strength,
            "mental_strength": mental_strength,
            "luck_factor": luck_factor,
        })
        super().__init__(
            data["name"], data["rating"], data["recent_form"],
            data["goals_for"], data["goals_against"], data["injury_level"],
            data["manager_rating"], data["crowd_strength"],
            data["mental_strength"], data["luck_factor"],
        )


class ValidatedMatchPrediction(BaseMatchPrediction):
    """Match prediction that validates teams, H2H data, and probability."""

    def __init__(self, home_team, away_team, head_to_head_record=None,
                 chaos_probability=0.35):
        home_data = {
            key: getattr(home_team, key)
            for key in (
                "name", "rating", "recent_form", "goals_for", "goals_against",
                "injury_level", "manager_rating", "crowd_strength",
                "mental_strength", "luck_factor",
            )
        }
        away_data = {
            key: getattr(away_team, key)
            for key in (
                "name", "rating", "recent_form", "goals_for", "goals_against",
                "injury_level", "manager_rating", "crowd_strength",
                "mental_strength", "luck_factor",
            )
        }
        validated = validate_match_data(
            home_data, away_data, head_to_head_record, chaos_probability
        )
        super().__init__(
            home_team,
            away_team,
            validated["head_to_head_record"],
            validated["chaos_probability"],
        )

    def predict_winner_and_score(self):
        """Generate a prediction and validate its core result fields."""
        winner, confidence, score, analysis, chaos_event = super().predict_winner_and_score()
        try:
            home_goals, away_goals = (int(value) for value in score.split("-", 1))
        except (AttributeError, ValueError) as exc:
            raise ValueError(f"Engine returned an invalid score: {score!r}") from exc
        validated = validate_prediction({
            "winner": winner,
            "confidence": confidence,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "analysis": analysis,
        })
        return (
            validated["winner"], validated["confidence"],
            f"{validated['home_goals']}-{validated['away_goals']}",
            analysis, chaos_event,
        )


__all__ = ["ValidatedTeam", "ValidatedMatchPrediction"]


if __name__ == "__main__":
    # Small smoke test for the validated API.
    home = ValidatedTeam("Home FC", 80, 78, 1.8, 1.2)
    away = ValidatedTeam("Away FC", 75, 73, 1.5, 1.4)
    match = ValidatedMatchPrediction(home, away)
    print(match.generate_prediction_report())
