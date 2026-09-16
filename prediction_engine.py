"""
Sports Match Prediction Engine
Predicts match outcomes based on team stats and performance metrics
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
    
    def predict_winner(self):
        """
        Predict match winner based on team strength
        Returns: 'Home Win', 'Away Win', or 'Draw'
        """
        home_strength = self.home_team.get_strength_score()
        away_strength = self.away_team.get_strength_score()
        
        # Add home advantage (5% boost)
        home_advantage = 1.05
        home_strength *= home_advantage
        
        # Calculate win probability
        total_strength = home_strength + away_strength
        home_win_prob = home_strength / total_strength
        away_win_prob = away_strength / total_strength
        
        # Determine outcome
        if home_win_prob > away_win_prob + 0.1:
            return "Home Win", home_win_prob
        elif away_win_prob > home_win_prob + 0.1:
            return "Away Win", away_win_prob
        else:
            return "Draw", 0.5
    
    def predict_score(self):
        """Predict expected match score"""
        home_goals = round(self.home_team.goals_for * (self.home_team.get_strength_score() / 100))
        away_goals = round(self.away_team.goals_for * (self.away_team.get_strength_score() / 100))
        
        return f"{home_goals}-{away_goals}"
    
    def generate_prediction_report(self):
        """Generate full prediction report"""
        winner, confidence = self.predict_winner()
        score = self.predict_score()
        
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


# Example: São Paulo vs Boca Juniors
if __name__ == "__main__":
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
    match = MatchPrediction(sao_paulo, boca_juniors)
    print(match.generate_prediction_report())
