"""
Borneo Samarinda vs Dewa United Match Prediction
Real-time prediction using the sports prediction engine
Indonesian Premier League Match
"""

import random
from datetime import datetime
from prediction_engine import Team, MatchPrediction

# Set random seed for reproducibility
random.seed(datetime.now().timestamp())

# Borneo Samarinda Team Setup
borneo_samarinda = Team(
    name="Borneo Samarinda",
    rating=77,
    recent_form=75,
    goals_for=1.5,
    goals_against=1.3,
    injury_level=6,
    manager_rating=74,
    crowd_strength=1.17,  # Strong home support
    mental_strength=75,
    luck_factor=0.96
)

# Dewa United Team Setup
dewa_united = Team(
    name="Dewa United",
    rating=80,
    recent_form=78,
    goals_for=1.8,
    goals_against=1.1,
    injury_level=4,
    manager_rating=77,
    crowd_strength=1.0,
    mental_strength=76,
    luck_factor=1.02
)

# Head-to-head history (estimated)
h2h_record = {'home_wins': 2, 'away_wins': 2, 'draws': 1}

# Create match prediction with chaos factor
match = MatchPrediction(borneo_samarinda, dewa_united, h2h_record, chaos_probability=0.37)

# Generate and display prediction report
if __name__ == "__main__":
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  🏆 BORNEO SAMARINDA vs DEWA UNITED PREDICTION 🏆".center(73) + "█")
    print("█" + f"  Indonesian Premier League Match".center(73) + "█")
    print("█" + f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
    
    print(match.generate_prediction_report())
    
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  ⚽ PREDICTION ANALYSIS COMPLETE - BORNEO vs DEWA ⚽".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
