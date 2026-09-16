"""Command-line interface for the sports prediction system.

Examples:
    python cli.py --home "São Paulo FC" --away "Boca Juniors" \
        --home-rating 78 --away-rating 82

    python cli.py --interactive

    python cli.py --home "Home FC" --away "Away FC" --json
"""

import argparse
import json
import logging
import sys
from typing import Any, Dict

from validated_engine import ValidatedMatchPrediction, ValidatedTeam
from validation import ValidationError, configure_logging


LOGGER = logging.getLogger("sports_prediction.cli")


def _team_from_args(args, prefix: str) -> ValidatedTeam:
    """Build a validated team from CLI arguments."""
    return ValidatedTeam(
        name=getattr(args, f"{prefix}_name"),
        rating=getattr(args, f"{prefix}_rating"),
        recent_form=getattr(args, f"{prefix}_form"),
        goals_for=getattr(args, f"{prefix}_goals_for"),
        goals_against=getattr(args, f"{prefix}_goals_against"),
        injury_level=getattr(args, f"{prefix}_injuries"),
        manager_rating=getattr(args, f"{prefix}_manager"),
        crowd_strength=getattr(args, f"{prefix}_crowd"),
        mental_strength=getattr(args, f"{prefix}_mental"),
        luck_factor=getattr(args, f"{prefix}_luck"),
    )


def _prompt_team(label: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    """Collect one team's values interactively."""
    print(f"\n{label} team")
    values = {}
    prompts = {
        "name": ("Name", str), "rating": ("Rating", float),
        "recent_form": ("Recent form", float), "goals_for": ("Goals for", float),
        "goals_against": ("Goals against", float), "injury_level": ("Injury level", float),
        "manager_rating": ("Manager rating", float), "crowd_strength": ("Crowd strength", float),
        "mental_strength": ("Mental strength", float), "luck_factor": ("Luck factor", float),
    }
    for key, (label_text, converter) in prompts.items():
        default = defaults[key]
        raw = input(f"{label_text} [{default}]: ").strip()
        values[key] = default if not raw else converter(raw)
    return values


def interactive_prediction() -> Any:
    """Run an interactive prediction session."""
    defaults = {
        "rating": 70, "recent_form": 70, "goals_for": 1.5,
        "goals_against": 1.5, "injury_level": 0, "manager_rating": 75,
        "crowd_strength": 1.0, "mental_strength": 75, "luck_factor": 0.5,
    }
    home_data = _prompt_team("Home", {**defaults, "name": "Home FC"})
    away_data = _prompt_team("Away", {**defaults, "name": "Away FC"})
    chaos = float(input("Chaos probability [0.35]: ").strip() or "0.35")
    h2h = {
        "home_wins": int(input("Previous home wins [0]: ").strip() or "0"),
        "away_wins": int(input("Previous away wins [0]: ").strip() or "0"),
        "draws": int(input("Previous draws [0]: ").strip() or "0"),
    }
    return create_prediction(home_data, away_data, h2h, chaos)


def create_prediction(home_data: Dict[str, Any], away_data: Dict[str, Any],
                      h2h: Dict[str, int], chaos_probability: float) -> Any:
    """Create a validated prediction from dictionaries."""
    home = ValidatedTeam(**home_data)
    away = ValidatedTeam(**away_data)
    return ValidatedMatchPrediction(home, away, h2h, chaos_probability)


def prediction_as_dict(prediction: Any) -> Dict[str, Any]:
    """Return prediction data suitable for JSON output."""
    winner, confidence, score, analysis, chaos_event = prediction.predict_winner_and_score()
    result = {
        "home_team": prediction.home_team.name,
        "away_team": prediction.away_team.name,
        "winner": winner,
        "confidence": round(confidence, 4),
        "score": score,
        "analysis": analysis,
        "chaos_event": chaos_event.value if chaos_event else None,
        "affected_team": prediction.affected_team,
    }
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate football match predictions.")
    parser.add_argument("--interactive", action="store_true", help="Prompt for match data")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output JSON")
    parser.add_argument("--log-file", help="Optional log file")
    parser.add_argument("--home", dest="home_name", help="Home team name")
    parser.add_argument("--away", dest="away_name", help="Away team name")
    for prefix in ("home", "away"):
        parser.add_argument(f"--{prefix}-rating", dest=f"{prefix}_rating", type=float, default=70)
        parser.add_argument(f"--{prefix}-form", dest=f"{prefix}_form", type=float, default=70)
        parser.add_argument(f"--{prefix}-goals-for", dest=f"{prefix}_goals_for", type=float, default=1.5)
        parser.add_argument(f"--{prefix}-goals-against", dest=f"{prefix}_goals_against", type=float, default=1.5)
        parser.add_argument(f"--{prefix}-injuries", dest=f"{prefix}_injuries", type=float, default=0)
        parser.add_argument(f"--{prefix}-manager", dest=f"{prefix}_manager", type=float, default=75)
        parser.add_argument(f"--{prefix}-crowd", dest=f"{prefix}_crowd", type=float, default=1.0)
        parser.add_argument(f"--{prefix}-mental", dest=f"{prefix}_mental", type=float, default=75)
        parser.add_argument(f"--{prefix}-luck", dest=f"{prefix}_luck", type=float, default=0.5)
    parser.add_argument("--home-wins", type=int, default=0)
    parser.add_argument("--away-wins", type=int, default=0)
    parser.add_argument("--draws", type=int, default=0)
    parser.add_argument("--chaos", type=float, default=0.35, dest="chaos_probability")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(logging.INFO, args.log_file)
    try:
        if args.interactive:
            prediction = interactive_prediction()
        elif not args.home_name or not args.away_name:
            parser.error("--home and --away are required unless --interactive is used")
        else:
            prediction = create_prediction(
                vars_to_team_data(args, "home"), vars_to_team_data(args, "away"),
                {"home_wins": args.home_wins, "away_wins": args.away_wins, "draws": args.draws},
                args.chaos_probability,
            )
        print(json.dumps(prediction_as_dict(prediction), indent=2, ensure_ascii=False)
              if args.as_json else prediction.generate_prediction_report())
        return 0
    except (ValidationError, ValueError, TypeError) as exc:
        LOGGER.error("Could not generate prediction: %s", exc)
        return 2
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def vars_to_team_data(args, prefix: str) -> Dict[str, Any]:
    """Convert parsed arguments into ValidatedTeam keyword arguments."""
    return {
        "name": getattr(args, f"{prefix}_name"),
        "rating": getattr(args, f"{prefix}_rating"),
        "recent_form": getattr(args, f"{prefix}_form"),
        "goals_for": getattr(args, f"{prefix}_goals_for"),
        "goals_against": getattr(args, f"{prefix}_goals_against"),
        "injury_level": getattr(args, f"{prefix}_injuries"),
        "manager_rating": getattr(args, f"{prefix}_manager"),
        "crowd_strength": getattr(args, f"{prefix}_crowd"),
        "mental_strength": getattr(args, f"{prefix}_mental"),
        "luck_factor": getattr(args, f"{prefix}_luck"),
    }


if __name__ == "__main__":
    raise SystemExit(main())
