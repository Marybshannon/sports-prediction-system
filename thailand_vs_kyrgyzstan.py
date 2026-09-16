"""
Thailand vs Kyrgyzstan Match Prediction
Real-time prediction using the sports prediction engine
"""

import random
from datetime import datetime
from prediction_engine import Team, MatchPrediction

# Set random seed for reproducibility
random.seed(datetime.now().timestamp())

# Thailand Team Setup
thailand = Team(
    name="Thailand",
    rating=92,
    recent_form=78,
    goals_for=1.6,
    goals_against=1.3,
    injury_level=3,
    manager_rating=75,
    crowd_strength=1.15,  # Home advantage
    mental_strength=76,
    luck_factor=0.95
)

# Kyrgyzstan Team Setup
kyrgyzstan = Team(
    name="Kyrgyzstan",
    rating=112,
    recent_form=72,
    goals_for=1.2,
    goals_against=1.5,
    injury_level=6,
    manager_rating=70,
    crowd_strength=1.0,
    mental_strength=72,
    luck_factor=0.9
)

# Head-to-head history
h2h_record = {'home_wins': 1, 'away_wins': 1, 'draws': 0}

# Create match prediction with chaos factor
match = MatchPrediction(thailand, kyrgyzstan, h2h_record, chaos_probability=0.35)

# Generate and display prediction report
if __name__ == "__main__":
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🏆 THAILAND vs KYRGYZSTAN PREDICTION 🏆".center(68) + "█")
    print("█" + f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print("\n")
    
    print(match.generate_prediction_report())
    
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  ⚽ PREDICTION ANALYSIS COMPLETE ⚽".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print("\n")
