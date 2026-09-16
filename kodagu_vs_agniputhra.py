"""
Kodagu FC vs FC Agniputhra Match Prediction
Real-time prediction using the sports prediction engine
Match scheduled: 9:00 AM Nigeria Time (WAT - UTC+1)
"""

import random
from datetime import datetime
from prediction_engine import Team, MatchPrediction

# Set random seed for reproducibility
random.seed(datetime.now().timestamp())

# Kodagu FC Team Setup
kodagu_fc = Team(
    name="Kodagu FC",
    rating=76,
    recent_form=74,
    goals_for=1.5,
    goals_against=1.4,
    injury_level=4,
    manager_rating=73,
    crowd_strength=1.18,  # Strong home support
    mental_strength=75,
    luck_factor=0.92
)

# FC Agniputhra Team Setup
fc_agniputhra = Team(
    name="FC Agniputhra",
    rating=79,
    recent_form=77,
    goals_for=1.7,
    goals_against=1.2,
    injury_level=5,
    manager_rating=76,
    crowd_strength=1.0,
    mental_strength=74,
    luck_factor=1.05
)

# Head-to-head history (estimated)
h2h_record = {'home_wins': 2, 'away_wins': 1, 'draws': 1}

# Create match prediction with chaos factor
match = MatchPrediction(kodagu_fc, fc_agniputhra, h2h_record, chaos_probability=0.38)

# Generate and display prediction report
if __name__ == "__main__":
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  🏆 KODAGU FC vs FC AGNIPUTHRA PREDICTION 🏆".center(73) + "█")
    print("█" + f"  Match Time: 09:00 AM Nigeria Time (WAT)".center(73) + "█")
    print("█" + f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
    
    print(match.generate_prediction_report())
    
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  ⚽ PREDICTION ANALYSIS COMPLETE - MATCH AT 9:00 AM WAT ⚽".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
