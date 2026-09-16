"""
Advanced Sports Match Prediction Engine
Predicts match outcomes based on comprehensive team stats and real-world factors
Includes: ratings, form, injuries, head-to-head, manager performance, crowd advantage
"""

class Team:
    """Represents a sports team with comprehensive performance metrics"""
    def __init__(self, name, rating, recent_form, goals_for, goals_against, 
                 injury_level=0, manager_rating=75, crowd_strength=1.0):
        self.name = name
        self.rating = rating  # Overall team strength (0-100)
        self.recent_form = recent_form  # Recent performance score (0-100)
        self.goals_for = goals_for  # Average goals scored
        self.goals_against = goals_against  # Average goals conceded
        self.injury_level = injury_level  # Injury impact (0-30, higher = more injuries)
        self.manager_rating = manager_rating  # Manager tactical ability (0-100)
        self.crowd_strength = crowd_strength  # Home crowd advantage multiplier (1.0-1.3)
    
    def get_strength_score(self):
        """Calculate overall team strength with real-world factors"""
        base_strength = (self.rating * 0.4) + (self.recent_form * 0.4) + (self.manager_rating * 0.2)
        
        # Apply injury penalty
        injury_penalty = (self.injury_level / 100) * 20  # Up to 20 point deduction
        
        final_strength = base_strength - injury_penalty
        return max(20, final_strength)  # Minimum 20 to avoid negative values


class MatchPrediction:
    """Advanced match prediction with real-world factors"""
    
    def __init__(self, home_team, away_team, head_to_head_record=None):
        """
        head_to_head_record: dict with keys 'home_wins', 'away_wins', 'draws'
        Example: {'home_wins': 2, 'away_wins': 1, 'draws': 1}
        """
        self.home_team = home_team
        self.away_team = away_team
        self.head_to_head_record = head_to_head_record or {'home_wins': 0, 'away_wins': 0, 'draws': 0}
    
    def calculate_h2h_advantage(self):
        """Calculate head-to-head historical advantage"""
        total_matches = sum(self.head_to_head_record.values())
        if total_matches == 0:
            return 0  # No historical data
        
        home_win_rate = self.head_to_head_record['home_wins'] / total_matches
        away_win_rate = self.head_to_head_record['away_wins'] / total_matches
        
        # Advantage: difference in historical win rates (scaled to -10 to +10)
        h2h_advantage = (home_win_rate - away_win_rate) * 10
        return h2h_advantage
    
    def predict_winner_and_score(self):
        """
        Predict match winner AND score with real-world factors
        Returns: (winner, confidence, predicted_score, analysis)
        """
        home_strength = self.home_team.get_strength_score()
        away_strength = self.away_team.get_strength_score()
        
        # 1. Home advantage (5-30% depending on crowd strength)
        home_advantage = 1.0 + (0.05 * self.home_team.crowd_strength)
        home_strength_with_advantage = home_strength * home_advantage
        
        # 2. Head-to-head advantage/disadvantage
        h2h_advantage = self.calculate_h2h_advantage()
        home_strength_with_h2h = home_strength_with_advantage + h2h_advantage
        
        # 3. Calculate final win probability
        total_strength = home_strength_with_h2h + away_strength
        home_win_prob = home_strength_with_h2h / total_strength
        away_win_prob = away_strength / total_strength
        
        # Analysis details
        analysis = {
            'home_base_strength': round(home_strength, 2),
            'away_base_strength': round(away_strength, 2),
            'home_injuries': self.home_team.injury_level,
            'away_injuries': self.away_team.injury_level,
            'h2h_advantage': round(h2h_advantage, 2)
        }
        
        # Determine outcome with confidence threshold
        confidence_threshold = 0.10
        
        if home_win_prob > away_win_prob + confidence_threshold:
            winner = "Home Win"
            confidence = home_win_prob
            # Home team wins - score reflects this
            home_goals = max(1, round(self.home_team.goals_for * (home_strength / 100)))
            away_goals = max(0, round(self.away_team.goals_for * (away_strength / 100) * 0.75))
            # Ensure home has more goals
            if home_goals <= away_goals:
                home_goals = away_goals + 1
        elif away_win_prob > home_win_prob + confidence_threshold:
            winner = "Away Win"
            confidence = away_win_prob
            # Away team wins - score reflects this
            away_goals = max(1, round(self.away_team.goals_for * (away_strength / 100)))
            home_goals = max(0, round(self.home_team.goals_for * (home_strength / 100) * 0.75))
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
        return winner, confidence, predicted_score, analysis
    
    def generate_prediction_report(self):
        """Generate comprehensive prediction report with analysis"""
        winner, confidence, score, analysis = self.predict_winner_and_score()
        
        h2h_text = "No H2H Data"
        if sum(self.head_to_head_record.values()) > 0:
            h2h_text = f"H: {self.head_to_head_record['home_wins']} - D: {self.head_to_head_record['draws']} - A: {self.head_to_head_record['away_wins']}"
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
║          ADVANCED MATCH PREDICTION REPORT                  ║
╚════════════════════════════════════════════════════════════╝

🏠 HOME: {self.home_team.name}
   ├─ Overall Rating: {self.home_team.rating}/100
   ├─ Recent Form: {self.home_team.recent_form}/100
   ├─ Manager Rating: {self.home_team.manager_rating}/100
   ├─ Injuries: {self.home_team.injury_level}/30
   ├─ Crowd Advantage: {self.home_team.crowd_strength:.1f}x
   └─ Base Strength: {analysis['home_base_strength']}

✈️  AWAY: {self.away_team.name}
   ├─ Overall Rating: {self.away_team.rating}/100
   ├─ Recent Form: {self.away_team.recent_form}/100
   ├─ Manager Rating: {self.away_team.manager_rating}/100
   ├─ Injuries: {self.away_team.injury_level}/30
   └─ Base Strength: {analysis['away_base_strength']}

📊 HEAD-TO-HEAD HISTORY:
   {h2h_text}
   H2H Advantage: {analysis['h2h_advantage']:+.2f}

🎯 FINAL PREDICTION:
   🏆 Winner: {winner}
   📈 Confidence: {confidence*100:.1f}%
   ⚽ Expected Score: {score}

════════════════════════════════════════════════════════════
       ✅ PREDICTION READY - FACTORS CONSIDERED ✅
════════════════════════════════════════════════════════════
"""
        return report


# Example: São Paulo vs Boca Juniors & Puebla vs Toluca
if __name__ == "__main__":
    print("=" * 60)
    print("PREDICTION SET 1: SÃO PAULO vs BOCA JUNIORS")
    print("=" * 60)
    
    # Team data with real-world factors
    sao_paulo = Team(
        name="São Paulo FC",
        rating=78,
        recent_form=75,
        goals_for=1.8,
        goals_against=1.2,
        injury_level=5,  # Minor injuries
        manager_rating=78,
        crowd_strength=1.15  # Strong home support
    )
    
    boca_juniors = Team(
        name="Boca Juniors",
        rating=82,
        recent_form=80,
        goals_for=2.1,
        goals_against=1.0,
        injury_level=8,  # Moderate injuries
        manager_rating=82,
        crowd_strength=1.0  # Away team
    )
    
    # Head-to-head record: Boca has slight advantage
    h2h_sp_boca = {'home_wins': 3, 'away_wins': 4, 'draws': 2}
    
    match1 = MatchPrediction(sao_paulo, boca_juniors, h2h_sp_boca)
    print(match1.generate_prediction_report())
    
    print("\n" + "=" * 60)
    print("PREDICTION SET 2: PUEBLA vs TOLUCA")
    print("=" * 60)
    
    puebla = Team(
        name="FC Puebla",
        rating=72,
        recent_form=68,
        goals_for=1.5,
        goals_against=1.4,
        injury_level=12,  # Several key players out
        manager_rating=70,
        crowd_strength=1.20  # Passionate fans
    )
    
    toluca = Team(
        name="Toluca FC",
        rating=80,
        recent_form=82,
        goals_for=2.0,
        goals_against=0.9,
        injury_level=3,  # Few injuries
        manager_rating=85,  # Excellent manager
        crowd_strength=1.0  # Away team
    )
    
    # Head-to-head: Toluca has won more recently
    h2h_puebla_toluca = {'home_wins': 2, 'away_wins': 5, 'draws': 1}
    
    match2 = MatchPrediction(puebla, toluca, h2h_puebla_toluca)
    print(match2.generate_prediction_report())
