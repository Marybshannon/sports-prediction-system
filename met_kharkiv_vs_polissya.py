"""
Met Kharkiv vs Polissya Zhytomyr Match Prediction
Real-time prediction using the sports prediction engine
Ukrainian Premier League Match
"""

import random
from datetime import datetime
from prediction_engine import Team, MatchPrediction

# Set random seed for reproducibility
random.seed(datetime.now().timestamp())

# Met Kharkiv Team Setup
met_kharkiv = Team(
    name="Met Kharkiv",
    rating=78,
    recent_form=76,
    goals_for=1.6,
    goals_against=1.3,
    injury_level=5,
    manager_rating=75,
    crowd_strength=1.16,  # Strong home support
    mental_strength=74,
    luck_factor=0.94
)

# Polissya Zhytomyr Team Setup
polissya_zhytomyr = Team(
    name="Polissya Zhytomyr",
    rating=73,
    recent_form=71,
    goals_for=1.4,
    goals_against=1.5,
    injury_level=7,
    manager_rating=71,
    crowd_strength=1.0,
    mental_strength=72,
    luck_factor=0.98
)

# Head-to-head history (estimated)
h2h_record = {'home_wins': 3, 'away_wins': 1, 'draws': 2}

# Create match prediction with chaos factor
match = MatchPrediction(met_kharkiv, polissya_zhytomyr, h2h_record, chaos_probability=0.36)

# Generate and display prediction report
if __name__ == "__main__":
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  🏆 MET KHARKIV vs POLISSYA ZHYTOMYR PREDICTION 🏆".center(73) + "█")
    print("█" + f"  Ukrainian Premier League Match".center(73) + "█")
    print("█" + f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
    
    print(match.generate_prediction_report())
    
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  ⚽ PREDICTION ANALYSIS COMPLETE - MET KHARKIV vs POLISSYA ⚽".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
