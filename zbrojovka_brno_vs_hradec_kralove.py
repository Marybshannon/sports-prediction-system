"""
FC Zbrojovka Brno vs FC Hradec Kralove Match Prediction
Real-time prediction using the sports prediction engine
Czech First League Match
"""

import random
from datetime import datetime
from prediction_engine import Team, MatchPrediction

# Set random seed for reproducibility
random.seed(datetime.now().timestamp())

# FC Zbrojovka Brno Team Setup
zbrojovka_brno = Team(
    name="FC Zbrojovka Brno",
    rating=75,
    recent_form=73,
    goals_for=1.4,
    goals_against=1.4,
    injury_level=7,
    manager_rating=72,
    crowd_strength=1.14,  # Home support
    mental_strength=73,
    luck_factor=0.93
)

# FC Hradec Kralove Team Setup
hradec_kralove = Team(
    name="FC Hradec Králové",
    rating=78,
    recent_form=76,
    goals_for=1.6,
    goals_against=1.2,
    injury_level=5,
    manager_rating=75,
    crowd_strength=1.0,
    mental_strength=75,
    luck_factor=1.01
)

# Head-to-head history (estimated - Czech First League rivals)
h2h_record = {'home_wins': 2, 'away_wins': 2, 'draws': 2}

# Create match prediction with chaos factor
match = MatchPrediction(zbrojovka_brno, hradec_kralove, h2h_record, chaos_probability=0.36)

# Generate and display prediction report
if __name__ == "__main__":
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  🏆 FC ZBROJOVKA BRNO vs FC HRADEC KRÁLOVÉ PREDICTION 🏆".center(73) + "█")
    print("█" + f"  Czech First League Match".center(73) + "█")
    print("█" + f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
    
    print(match.generate_prediction_report())
    
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  ⚽ PREDICTION ANALYSIS COMPLETE - ZBROJOVKA vs HRADEC ⚽".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
