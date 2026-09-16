"""
Sports Match Prediction Engine
Predicts match outcomes based on team stats and performance metrics
FIXED: Score predictions now match winner predictions
"""

class Team:
    """Represents a sports team with performance metrics"""
    def __init__(self, name, rating, recent_form, goals_for, goals_against):
        self.name = name
        self.rating = rating  # Overall team strength (0-100)
        self.recent_form = recent_form  # Recent performance score (0-100)
        self.goals_for = goals_for  # Average goals scored
        self.goals_against = goals_against  # Average goals conceded
    
    def get_strength_score(self):
        """Calculate overall team strength"""
        return (self.rating * 0.5) + (self.recent_form * 0.5)


class MatchPrediction:
    """Predicts match outcomes between two teams"""
    
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
    
    def predict_winner_and_score(self):
        """
        Predict match winner AND score - CONSISTENT with each other
        Returns: (winner, confidence, predicted_score)
        """
        home_strength = self.home_team.get_strength_score()
        away_strength = self.away_team.get_strength_score()
        
        # Add home advantage (5% boost)
        home_advantage = 1.05
        home_strength_with_advantage = home_strength * home_advantage
        
        # Calculate win probability
        total_strength = home_strength_with_advantage + away_strength
        home_win_prob = home_strength_with_advantage / total_strength
        away_win_prob = away_strength / total_strength
        
        # Determine outcome with confidence threshold
        if home_win_prob > away_win_prob + 0.10:
            winner = "Home Win"
            confidence = home_win_prob
            # Home team wins - score reflects this
            home_goals = max(1, round(self.home_team.goals_for * (home_strength / 100)))
            away_goals = max(0, round(self.away_team.goals_for * (away_strength / 100) * 0.8))
            # Ensure home has more goals
            if home_goals <= away_goals:
                home_goals = away_goals + 1
        elif away_win_prob > home_win_prob + 0.10:
            winner = "Away Win"
            confidence = away_win_prob
            # Away team wins - score reflects this
            away_goals = max(1, round(self.away_team.goals_for * (away_strength / 100)))
            home_goals = max(0, round(self.home_team.goals_for * (home_strength / 100) * 0.8))
            # Ensure away has more goals
            if away_goals <= home_goals:
                away_goals = home_goals + 1
        else:
            winner = "Draw"
            confidence = 0.5
            # Draw - similar goals for both teams
            home_goals = round(self.home_team.goals_for * (home_strength / 100))
            away_goals = round(self.away_team.goals_for * (away_strength / 100))
            # Make it closer for a draw
            if home_goals != away_goals:
                if home_goals > away_goals:
                    away_goals = home_goals
                else:
                    home_goals = away_goals
        
        predicted_score = f"{home_goals}-{away_goals}"
        return winner, confidence, predicted_score
    
    def generate_prediction_report(self):
        """Generate full prediction report"""
        winner, confidence, score = self.predict_winner_and_score()
        
        report = f"""
╔════════════════════════════════════════╗
║       MATCH PREDICTION REPORT           ║
╚════════════════════════════════════════╝

🏠 HOME: {self.home_team.name}
   Rating: {self.home_team.rating}/100
   Recent Form: {self.home_team.recent_form}/100
   Strength Score: {self.home_team.get_strength_score():.2f}

✈️  AWAY: {self.away_team.name}
   Rating: {self.away_team.rating}/100
   Recent Form: {self.away_team.recent_form}/100
   Strength Score: {self.away_team.get_strength_score():.2f}

🎯 PREDICTION:
   Winner: {winner}
   Confidence: {confidence*100:.1f}%
   Expected Score: {score}

════════════════════════════════════════
        ✅ PREDICTION READY ✅
════════════════════════════════════════
"""
        return report


# Example: São Paulo vs Boca Juniors & Puebla vs Toluca
if __name__ == "__main__":
    print("=" * 50)
    print("PREDICTION SET 1: SÃO PAULO vs BOCA JUNIORS")
    print("=" * 50)
    
    # Team data (example values)
    sao_paulo = Team(
        name="São Paulo FC",
        rating=78,
        recent_form=75,
        goals_for=1.8,
        goals_against=1.2
    )
    
    boca_juniors = Team(
        name="Boca Juniors",
        rating=82,
        recent_form=80,
        goals_for=2.1,
        goals_against=1.0
    )
    
    # Generate prediction
    match1 = MatchPrediction(sao_paulo, boca_juniors)
    print(match1.generate_prediction_report())
    
    print("\n" + "=" * 50)
    print("PREDICTION SET 2: PUEBLA vs TOLUCA")
    print("=" * 50)
    
    # Puebla vs Toluca prediction
    puebla = Team(
        name="FC Puebla",
        rating=72,
        recent_form=68,
        goals_for=1.5,
        goals_against=1.4
    )
    
    toluca = Team(
        name="Toluca FC",
        rating=80,
        recent_form=82,
        goals_for=2.0,
        goals_against=0.9
    )
    
    # Generate prediction
    match2 = MatchPrediction(puebla, toluca)
    print(match2.generate_prediction_report())
