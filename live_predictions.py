"""
REAL-TIME MATCH PREDICTIONS - LIVE EXECUTION
Running predictions with chaos factor for matches happening today!
"""

import random
from datetime import datetime

# Set random seed for reproducibility but with real variability
random.seed(datetime.now().timestamp())

from enum import Enum

class ChaosType(Enum):
    """Types of chaos that can affect a match"""
    REFEREE_BIAS = "Controversial Referee Decision"
    LUCKY_GOAL = "Unexplained Lucky Goal"
    INJURY_CRISIS = "Key Player Sudden Injury"
    RED_CARD = "Red Card Drama"
    VAR_CONTROVERSY = "VAR Malfunction/Controversy"
    WEATHER = "Extreme Weather Impact"
    PSYCHOLOGICAL = "Mental Breakdown/Pressure"
    MOMENTUM_SHIFT = "Unexpected Momentum Shift"
    NOTHING = "Match Goes as Expected"

class Team:
    """Represents a sports team with comprehensive performance metrics"""
    def __init__(self, name, rating, recent_form, goals_for, goals_against, 
                 injury_level=0, manager_rating=75, crowd_strength=1.0, 
                 mental_strength=75, luck_factor=0.5):
        self.name = name
        self.rating = rating
        self.recent_form = recent_form
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.injury_level = injury_level
        self.manager_rating = manager_rating
        self.crowd_strength = crowd_strength
        self.mental_strength = mental_strength
        self.luck_factor = luck_factor
    
    def get_strength_score(self):
        """Calculate overall team strength with real-world factors"""
        base_strength = (self.rating * 0.4) + (self.recent_form * 0.4) + (self.manager_rating * 0.2)
        injury_penalty = (self.injury_level / 100) * 20
        final_strength = base_strength - injury_penalty
        return max(20, final_strength)


class MatchPrediction:
    """Ultimate match prediction with real-world factors AND chaos"""
    
    def __init__(self, home_team, away_team, head_to_head_record=None, chaos_probability=0.35):
        self.home_team = home_team
        self.away_team = away_team
        self.head_to_head_record = head_to_head_record or {'home_wins': 0, 'away_wins': 0, 'draws': 0}
        self.chaos_probability = chaos_probability
        self.chaos_event = None
        self.affected_team = None
    
    def calculate_h2h_advantage(self):
        """Calculate head-to-head historical advantage"""
        total_matches = sum(self.head_to_head_record.values())
        if total_matches == 0:
            return 0
        
        home_win_rate = self.head_to_head_record['home_wins'] / total_matches
        away_win_rate = self.head_to_head_record['away_wins'] / total_matches
        
        h2h_advantage = (home_win_rate - away_win_rate) * 10
        return h2h_advantage
    
    def generate_chaos_event(self):
        """Generate random chaos event that affects match outcome"""
        chaos_roll = random.random()
        
        if chaos_roll > self.chaos_probability:
            self.chaos_event = ChaosType.NOTHING
            return None
        
        # Chaos events that favor home team
        home_favorable = [
            ChaosType.REFEREE_BIAS,
            ChaosType.PSYCHOLOGICAL,
        ]
        
        # Chaos events that favor away team
        away_favorable = [
            ChaosType.LUCKY_GOAL,
            ChaosType.MOMENTUM_SHIFT,
        ]
        
        # Neutral chaos events
        neutral = [
            ChaosType.INJURY_CRISIS,
            ChaosType.RED_CARD,
            ChaosType.VAR_CONTROVERSY,
            ChaosType.WEATHER,
        ]
        
        chaos_type = random.choice(home_favorable + away_favorable + neutral)
        self.chaos_event = chaos_type
        
        if chaos_type in home_favorable:
            self.affected_team = self.home_team.name
        elif chaos_type in away_favorable:
            self.affected_team = self.away_team.name
        else:
            self.affected_team = random.choice([self.home_team.name, self.away_team.name])
        
        return chaos_type
    
    def predict_winner_and_score(self):
        """Predict match winner with all factors including chaos"""
        home_strength = self.home_team.get_strength_score()
        away_strength = self.away_team.get_strength_score()
        
        home_advantage = 1.0 + (0.05 * self.home_team.crowd_strength)
        home_strength_with_advantage = home_strength * home_advantage
        
        h2h_advantage = self.calculate_h2h_advantage()
        home_strength_with_h2h = home_strength_with_advantage + h2h_advantage
        
        home_strength_final = home_strength_with_h2h * self.home_team.luck_factor
        away_strength_final = away_strength * self.away_team.luck_factor
        
        chaos_event = self.generate_chaos_event()
        
        chaos_impact = 0
        if chaos_event and chaos_event != ChaosType.NOTHING:
            chaos_impact = random.uniform(-15, 15)
            
            if self.affected_team == self.home_team.name:
                if chaos_event in [ChaosType.REFEREE_BIAS, ChaosType.PSYCHOLOGICAL]:
                    home_strength_final += abs(chaos_impact)
                else:
                    home_strength_final -= abs(chaos_impact)
            else:
                if chaos_event in [ChaosType.LUCKY_GOAL, ChaosType.MOMENTUM_SHIFT]:
                    away_strength_final += abs(chaos_impact)
                else:
                    away_strength_final -= abs(chaos_impact)
        
        total_strength = max(1, home_strength_final + away_strength_final)
        home_win_prob = home_strength_final / total_strength
        away_win_prob = away_strength_final / total_strength
        
        analysis = {
            'home_base_strength': round(home_strength, 2),
            'away_base_strength': round(away_strength, 2),
            'home_with_factors': round(home_strength_final, 2),
            'away_with_factors': round(away_strength_final, 2),
            'chaos_impact': round(chaos_impact, 2) if chaos_event else 0
        }
        
        confidence_threshold = 0.10
        
        if home_win_prob > away_win_prob + confidence_threshold:
            winner = "Home Win"
            confidence = home_win_prob
            home_goals = max(1, round(self.home_team.goals_for * (home_strength_final / 100)))
            away_goals = max(0, round(self.away_team.goals_for * (away_strength_final / 100) * 0.75))
            if home_goals <= away_goals:
                home_goals = away_goals + 1
        elif away_win_prob > home_win_prob + confidence_threshold:
            winner = "Away Win"
            confidence = away_win_prob
            away_goals = max(1, round(self.away_team.goals_for * (away_strength_final / 100)))
            home_goals = max(0, round(self.home_team.goals_for * (home_strength_final / 100) * 0.75))
            if away_goals <= home_goals:
                away_goals = home_goals + 1
        else:
            winner = "Draw"
            confidence = 0.5
            home_goals = round(self.home_team.goals_for * (home_strength_final / 100))
            away_goals = round(self.away_team.goals_for * (away_strength_final / 100))
            if home_goals != away_goals:
                if home_goals > away_goals:
                    away_goals = home_goals
                else:
                    home_goals = away_goals
        
        predicted_score = f"{home_goals}-{away_goals}"
        return winner, confidence, predicted_score, analysis, chaos_event
    
    def generate_prediction_report(self):
        """Generate ultimate prediction report"""
        winner, confidence, score, analysis, chaos_event = self.predict_winner_and_score()
        
        h2h_text = "No H2H Data"
        if sum(self.head_to_head_record.values()) > 0:
            h2h_text = f"H: {self.head_to_head_record['home_wins']} - D: {self.head_to_head_record['draws']} - A: {self.head_to_head_record['away_wins']}"
        
        chaos_text = ""
        if chaos_event and chaos_event != ChaosType.NOTHING:
            chaos_text = f"""
⚡ CHAOS EVENT DETECTED:
   └─ {chaos_event.value} (Affects: {self.affected_team})
   └─ Impact: {analysis['chaos_impact']:+.1f} points
"""
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           🔴 LIVE REAL-TIME PREDICTION 🔴                   ║
║        (Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})        ║
╚═══════��══════════════════════════════════════════════════════╝

🏠 HOME: {self.home_team.name}
   Rating: {self.home_team.rating}/100 | Form: {self.home_team.recent_form}/100
   Manager: {self.home_team.manager_rating}/100 | Luck: {self.home_team.luck_factor:.2f}x
   Injuries: {self.home_team.injury_level}/30 | Mental: {self.home_team.mental_strength}/100

✈️  AWAY: {self.away_team.name}
   Rating: {self.away_team.rating}/100 | Form: {self.away_team.recent_form}/100
   Manager: {self.away_team.manager_rating}/100 | Luck: {self.away_team.luck_factor:.2f}x
   Injuries: {self.away_team.injury_level}/30 | Mental: {self.away_team.mental_strength}/100

📊 HEAD-TO-HEAD: {h2h_text}

🎯 LIVE PREDICTION:
   🏆 Winner: {winner}
   📈 Confidence: {confidence*100:.1f}%
   ⚽ Expected Score: {score}{chaos_text}

════════════════════════════════════════════════════════════════
             LIVE CHAOS FACTOR: ACTIVE 🎭
════════════════════════════════════════════════════════════════
"""
        return report


# LIVE REAL-TIME PREDICTIONS
if __name__ == "__main__":
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🔴 LIVE REAL-TIME MATCH PREDICTIONS 🔴".center(68) + "█")
    print("█" + f"  Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print("\n")
    
    # MATCH 1: SÃO PAULO vs BOCA JUNIORS
    print("=" * 70)
    print("LIVE MATCH 1: SÃO PAULO vs BOCA JUNIORS")
    print("=" * 70)
    
    sao_paulo = Team(
        name="São Paulo FC",
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
    
    boca_juniors = Team(
        name="Boca Juniors",
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
    
    h2h_sp_boca = {'home_wins': 3, 'away_wins': 4, 'draws': 2}
    match1 = MatchPrediction(sao_paulo, boca_juniors, h2h_sp_boca, chaos_probability=0.40)
    print(match1.generate_prediction_report())
    
    # MATCH 2: PUEBLA vs TOLUCA
    print("\n")
    print("=" * 70)
    print("LIVE MATCH 2: PUEBLA vs TOLUCA")
    print("=" * 70)
    
    puebla = Team(
        name="FC Puebla",
        rating=72,
        recent_form=68,
        goals_for=1.5,
        goals_against=1.4,
        injury_level=12,
        manager_rating=70,
        crowd_strength=1.20,
        mental_strength=72,
        luck_factor=0.8
    )
    
    toluca = Team(
        name="Toluca FC",
        rating=80,
        recent_form=82,
        goals_for=2.0,
        goals_against=0.9,
        injury_level=3,
        manager_rating=85,
        crowd_strength=1.0,
        mental_strength=85,
        luck_factor=1.2
    )
    
    h2h_puebla_toluca = {'home_wins': 2, 'away_wins': 5, 'draws': 1}
    match2 = MatchPrediction(puebla, toluca, h2h_puebla_toluca, chaos_probability=0.35)
    print(match2.generate_prediction_report())
    
    # MATCH 3: İNKILAPSPOR vs TUZLASPOR (Turkish Cup)
    print("\n")
    print("=" * 70)
    print("LIVE MATCH 3: İNKILAPSPOR vs TUZLASPOR (Turkish Cup)")
    print("=" * 70)
    
    inkilapspor = Team(
        name="İnkılapspor",
        rating=65,
        recent_form=58,  # 2W-4L recent form = 33% win rate
        goals_for=1.4,
        goals_against=1.8,
        injury_level=6,
        manager_rating=72,
        crowd_strength=1.10,
        mental_strength=78,  # Better mental resilience than Tuzlaspor
        luck_factor=0.95
    )
    
    tuzlaspor = Team(
        name="Tuzlaspor",
        rating=64,
        recent_form=55,  # 2W-1D-3L recent form = 33% win rate
        goals_for=1.3,
        goals_against=1.9,
        injury_level=7,
        manager_rating=70,
        crowd_strength=1.0,  # Away team
        mental_strength=72,  # Lower mental strength
        luck_factor=1.05
    )
    
    h2h_inkilap_tuzla = {'home_wins': 1, 'away_wins': 1, 'draws': 2}
    match3 = MatchPrediction(inkilapspor, tuzlaspor, h2h_inkilap_tuzla, chaos_probability=0.38)
    print(match3.generate_prediction_report())
    
    # SUMMARY
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  ⚽ 3 PREDICTIONS COMPLETE - WATCH THE MATCHES! ⚽".center(68) + "█")
    print("█" + "  (Waiting for 4th match details...)".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print("\n")
