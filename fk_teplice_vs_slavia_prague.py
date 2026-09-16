"""
FK Teplice vs Slavia Prague Match Prediction
Real-time prediction using the sports prediction engine
Czech First League Match - Prague Derby Rivalry
"""

import random
from datetime import datetime
from prediction_engine import Team, MatchPrediction

# Set random seed for reproducibility
random.seed(datetime.now().timestamp())

# FK Teplice Team Setup
fk_teplice = Team(
    name="FK Teplice",
    rating=71,
    recent_form=69,
    goals_for=1.3,
    goals_against=1.6,
    injury_level=8,
    manager_rating=70,
    crowd_strength=1.12,  # Home support
    mental_strength=71,
    luck_factor=0.91
)

# Slavia Prague Team Setup
slavia_prague = Team(
    name="Slavia Prague",
    rating=86,
    recent_form=84,
    goals_for=2.2,
    goals_against=0.9,
    injury_level=3,
    manager_rating=82,
    crowd_strength=1.0,
    mental_strength=82,
    luck_factor=1.08
)

# Head-to-head history (Czech First League rivals - Slavia typically dominant)
h2h_record = {'home_wins': 1, 'away_wins': 4, 'draws': 1}

# Create match prediction with chaos factor
match = MatchPrediction(fk_teplice, slavia_prague, h2h_record, chaos_probability=0.35)

# Generate and display prediction report
if __name__ == "__main__":
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  🏆 FK TEPLICE vs SLAVIA PRAGUE PREDICTION 🏆".center(73) + "█")
    print("█" + f"  Czech First League - Prague Derby".center(73) + "█")
    print("█" + f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
    
    print(match.generate_prediction_report())
    
    print("\n")
    print("█" * 75)
    print("█" + " " * 73 + "█")
    print("█" + "  ⚽ PREDICTION ANALYSIS COMPLETE - TEPLICE vs SLAVIA ⚽".center(73) + "█")
    print("█" + " " * 73 + "█")
    print("█" * 75)
    print("\n")
