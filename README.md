# sports-prediction-system
A sports match prediction system for analyzing team performance and predicting match outcomes

## Overview
This project provides a sophisticated prediction engine that analyzes team performance metrics and generates realistic match predictions. It factors in team ratings, recent form, head-to-head records, injuries, crowd effects, and even unpredictable "chaos events" to create nuanced predictions for international and club football matches.

## Features
- **Comprehensive Team Analysis**: Evaluates multiple performance factors including ratings, recent form, goals scored/conceded, injury levels, and manager ratings
- **Head-to-Head Integration**: Considers historical matchup data to adjust win probabilities
- **Home Advantage Modeling**: Incorporates crowd strength and mental factors affecting home teams
- **Chaos Factor**: Introduces realistic unpredictability through psychological events, referee bias, lucky goals, and momentum shifts
- **Detailed Predictions**: Generates match outcome predictions with:
  - Win probability percentages
  - Predicted final scores
  - Confidence levels
  - Comprehensive analysis of influencing factors

## Project Structure

```
├── prediction_engine.py          # Core prediction logic and classes
├── live_predictions.py           # Multi-match real-time predictions demo
├── live_predictions_single.py    # Single match prediction template
│
# Individual match prediction files:
├── kodagu_vs_agniputhra.py       # Kodagu FC vs FC Agniputhra
├── borneo_vs_dewa_united.py      # Indonesian Premier League
├── met_kharkiv_vs_polissya.py    # Ukrainian Premier League
├── fk_teplice_vs_slavia_prague.py # Czech First League
├── zbrojovka_brno_vs_hradec_kralove.py # Czech First League
├── thailand_vs_kyrgyzstan.py     # International match
└── README.md                     # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Marybshannon/sports-prediction-system.git
   cd sports-prediction-system
   ```

2. **Requirements**:
   - Python 3.7+
   - No external dependencies (uses only Python standard library)

## Usage

### Run a Single Match Prediction
```bash
python kodagu_vs_agniputhra.py
```

### Run Multiple Live Predictions
```bash
python live_predictions.py
```

### Create Your Own Prediction
```python
from prediction_engine import Team, MatchPrediction

# Define home team
home_team = Team(
    name="Team A",
    rating=78,
    recent_form=75,
    goals_for=1.8,
    goals_against=1.2,
    injury_level=5,
    manager_rating=78,
    crowd_strength=1.15,
    mental_strength=76,
    luck_factor=0.9
)

# Define away team
away_team = Team(
    name="Team B",
    rating=82,
    recent_form=80,
    goals_for=2.1,
    goals_against=1.0,
    injury_level=8,
    manager_rating=82,
    crowd_strength=1.0,
    mental_strength=80,
    luck_factor=1.1
)

# Head-to-head record
h2h = {'home_wins': 3, 'away_wins': 4, 'draws': 2}

# Create prediction
match = MatchPrediction(home_team, away_team, h2h, chaos_probability=0.40)

# Generate report
print(match.generate_prediction_report())
```

## Core Components

### Team Class
Represents a football team with performance metrics:
- **rating**: Overall team strength (0-100)
- **recent_form**: Current performance level (0-100)
- **goals_for**: Average goals scored per match
- **goals_against**: Average goals conceded per match
- **injury_level**: Number of key injuries (0-15+)
- **manager_rating**: Tactical quality (0-100)
- **crowd_strength**: Home advantage multiplier (1.0-1.3)
- **mental_strength**: Team resilience (0-100)
- **luck_factor**: Match outcome variance (0.8-1.2)

### MatchPrediction Class
Analyzes two teams and generates predictions:
- Calculates base team strength from multiple factors
- Applies head-to-head historical advantages
- Incorporates luck and crowd effects
- Simulates chaos events for realistic unpredictability
- Determines outcome (Home Win/Away Win/Draw) with confidence level
- Predicts final match score

### Prediction Algorithm
1. **Base Strength Calculation**: Combines team rating, recent form, and injuries
2. **Home Advantage**: Multiplies home team strength by crowd effect
3. **H2H Adjustment**: Adds historical matchup advantage to win probability
4. **Luck Application**: Applies team luck factors to final calculations
5. **Chaos Events**: Randomly introduces match-changing moments (35-40% probability)
6. **Outcome Determination**: Calculates win probabilities and predicts match result

## Chaos Events
Realistic unpredictable events that affect match outcomes:
- **Lucky Goal**: Unexpected goal changes momentum
- **Referee Bias**: Controversial decisions favor one team
- **Psychological Breakthrough**: Team overcomes mental barriers
- **Injury Crisis**: Key player injury affects performance
- **Momentum Shift**: Team gains or loses psychological edge

## Example Output
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 LIVE REAL-TIME MATCH PREDICTIONS 🔴
  Execution Time: 2026-09-16 11:39:50
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LIVE MATCH 1: SÃO PAULO vs BOCA JUNIORS
════════════════════════════════════════════════════════════
🏟️  Home Team: São Paulo FC | Rating: 78
🏟️  Away Team: Boca Juniors | Rating: 82

PREDICTION ANALYSIS:
├─ Home Base Strength: 72.45
├─ Away Base Strength: 75.82
├─ Home Win Probability: 42.5%
├─ Away Win Probability: 52.8%
├─ Draw Probability: 4.7%
└─ Predicted Score: 1-2 (Away Win)

CONFIDENCE: 52.8% | Match Rating: LIKELY AWAY WIN
```

## Contributing
Contributions are welcome! Feel free to:
- Add new team matchups
- Improve prediction algorithms
- Add new chaos event types
- Enhance performance metrics

## License
This project is open source and available for educational and analytical purposes.

## Author
Created by @Marybshannon

---

*Last updated: September 2026*
