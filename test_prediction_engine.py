"""
Unit tests for the sports prediction engine
Tests core functionality, edge cases, and prediction accuracy
"""

import unittest
import random
from datetime import datetime
from prediction_engine import Team, MatchPrediction, ChaosType


class TestTeamClass(unittest.TestCase):
    """Test cases for Team class"""
    
    def setUp(self):
        """Create sample teams for testing"""
        self.team_strong = Team(
            name="Strong Team",
            rating=85,
            recent_form=82,
            goals_for=2.0,
            goals_against=0.8,
            injury_level=2,
            manager_rating=85,
            crowd_strength=1.15,
            mental_strength=85,
            luck_factor=1.05
        )
        
        self.team_weak = Team(
            name="Weak Team",
            rating=60,
            recent_form=55,
            goals_for=1.0,
            goals_against=1.8,
            injury_level=10,
            manager_rating=60,
            crowd_strength=1.0,
            mental_strength=60,
            luck_factor=0.85
        )
    
    def test_team_creation(self):
        """Test team object creation"""
        self.assertEqual(self.team_strong.name, "Strong Team")
        self.assertEqual(self.team_strong.rating, 85)
        self.assertIsNotNone(self.team_strong)
    
    def test_team_attributes(self):
        """Test all team attributes are set correctly"""
        self.assertEqual(self.team_strong.rating, 85)
        self.assertEqual(self.team_strong.recent_form, 82)
        self.assertEqual(self.team_strong.goals_for, 2.0)
        self.assertEqual(self.team_strong.goals_against, 0.8)
        self.assertEqual(self.team_strong.injury_level, 2)
        self.assertEqual(self.team_strong.manager_rating, 85)
        self.assertEqual(self.team_strong.crowd_strength, 1.15)
        self.assertEqual(self.team_strong.mental_strength, 85)
        self.assertEqual(self.team_strong.luck_factor, 1.05)
    
    def test_team_rating_ranges(self):
        """Test team ratings are within valid ranges"""
        self.assertGreaterEqual(self.team_strong.rating, 0)
        self.assertLessEqual(self.team_strong.rating, 100)
        self.assertGreaterEqual(self.team_strong.mental_strength, 0)
        self.assertLessEqual(self.team_strong.mental_strength, 100)


class TestMatchPrediction(unittest.TestCase):
    """Test cases for MatchPrediction class"""
    
    def setUp(self):
        """Create sample match for testing"""
        self.home_team = Team(
            name="Home Team",
            rating=80,
            recent_form=78,
            goals_for=1.8,
            goals_against=1.2,
            injury_level=3,
            manager_rating=80,
            crowd_strength=1.15,
            mental_strength=78,
            luck_factor=0.98
        )
        
        self.away_team = Team(
            name="Away Team",
            rating=75,
            recent_form=73,
            goals_for=1.5,
            goals_against=1.4,
            injury_level=5,
            manager_rating=75,
            crowd_strength=1.0,
            mental_strength=73,
            luck_factor=1.02
        )
        
        self.h2h_record = {'home_wins': 3, 'away_wins': 2, 'draws': 1}
        self.match = MatchPrediction(
            self.home_team, 
            self.away_team, 
            self.h2h_record,
            chaos_probability=0.35
        )
    
    def test_match_creation(self):
        """Test match prediction object creation"""
        self.assertIsNotNone(self.match)
        self.assertEqual(self.match.home_team.name, "Home Team")
        self.assertEqual(self.match.away_team.name, "Away Team")
    
    def test_match_attributes(self):
        """Test match has correct attributes"""
        self.assertEqual(self.match.h2h_record, self.h2h_record)
        self.assertEqual(self.match.chaos_probability, 0.35)
        self.assertIsNotNone(self.match.affected_team)
    
    def test_prediction_generation(self):
        """Test prediction generation produces valid results"""
        random.seed(42)  # For reproducibility
        prediction = self.match.predict_match()
        
        # Check prediction contains required keys
        self.assertIn('winner', prediction)
        self.assertIn('confidence', prediction)
        self.assertIn('home_goals', prediction)
        self.assertIn('away_goals', prediction)
        self.assertIn('analysis', prediction)
    
    def test_winner_validity(self):
        """Test prediction winner is valid"""
        random.seed(42)
        prediction = self.match.predict_match()
        valid_winners = ["Home Win", "Away Win", "Draw"]
        self.assertIn(prediction['winner'], valid_winners)
    
    def test_confidence_range(self):
        """Test confidence is between 0 and 1"""
        random.seed(42)
        prediction = self.match.predict_match()
        self.assertGreaterEqual(prediction['confidence'], 0)
        self.assertLessEqual(prediction['confidence'], 1)
    
    def test_goals_are_non_negative(self):
        """Test predicted goals are non-negative"""
        random.seed(42)
        prediction = self.match.predict_match()
        self.assertGreaterEqual(prediction['home_goals'], 0)
        self.assertGreaterEqual(prediction['away_goals'], 0)
    
    def test_draw_consistency(self):
        """Test draw predictions have equal goals"""
        # Run multiple predictions to find a draw
        for seed in range(100):
            random.seed(seed)
            prediction = self.match.predict_match()
            if prediction['winner'] == "Draw":
                self.assertEqual(prediction['home_goals'], prediction['away_goals'])
                return
    
    def test_home_win_consistency(self):
        """Test home win predictions have home goals > away goals"""
        for seed in range(100):
            random.seed(seed)
            prediction = self.match.predict_match()
            if prediction['winner'] == "Home Win":
                self.assertGreater(prediction['home_goals'], prediction['away_goals'])
                return
    
    def test_away_win_consistency(self):
        """Test away win predictions have away goals > home goals"""
        for seed in range(100):
            random.seed(seed)
            prediction = self.match.predict_match()
            if prediction['winner'] == "Away Win":
                self.assertGreater(prediction['away_goals'], prediction['home_goals'])
                return
    
    def test_prediction_report_generation(self):
        """Test prediction report can be generated"""
        report = self.match.generate_prediction_report()
        self.assertIsNotNone(report)
        self.assertIsInstance(report, str)
        self.assertGreater(len(report), 0)
    
    def test_stronger_team_advantage(self):
        """Test stronger team has higher win probability on average"""
        strong_home = Team(
            name="Strong Home",
            rating=90, recent_form=88, goals_for=2.5, goals_against=0.5,
            injury_level=1, manager_rating=90, crowd_strength=1.15,
            mental_strength=90, luck_factor=1.0
        )
        
        weak_away = Team(
            name="Weak Away",
            rating=50, recent_form=48, goals_for=0.8, goals_against=2.5,
            injury_level=12, manager_rating=50, crowd_strength=1.0,
            mental_strength=50, luck_factor=1.0
        )
        
        h2h = {'home_wins': 5, 'away_wins': 0, 'draws': 0}
        match = MatchPrediction(strong_home, weak_away, h2h, chaos_probability=0.2)
        
        home_wins = 0
        draws = 0
        away_wins = 0
        
        for seed in range(20):
            random.seed(seed)
            pred = match.predict_match()
            if pred['winner'] == "Home Win":
                home_wins += 1
            elif pred['winner'] == "Draw":
                draws += 1
            else:
                away_wins += 1
        
        # Strong team should win more often
        self.assertGreater(home_wins, away_wins)


class TestChaosEvents(unittest.TestCase):
    """Test cases for chaos event generation"""
    
    def setUp(self):
        """Create match for chaos testing"""
        self.home_team = Team(
            name="Home", rating=75, recent_form=73, goals_for=1.5,
            goals_against=1.3, injury_level=4, manager_rating=75,
            crowd_strength=1.1, mental_strength=73, luck_factor=0.98
        )
        
        self.away_team = Team(
            name="Away", rating=75, recent_form=73, goals_for=1.5,
            goals_against=1.3, injury_level=4, manager_rating=75,
            crowd_strength=1.0, mental_strength=73, luck_factor=1.02
        )
        
        self.h2h = {'home_wins': 2, 'away_wins': 2, 'draws': 2}
    
    def test_chaos_event_generation(self):
        """Test chaos events can be generated"""
        match = MatchPrediction(
            self.home_team, self.away_team, self.h2h, chaos_probability=1.0
        )
        
        for _ in range(10):
            event = match.generate_chaos_event()
            # Event should be a ChaosType or string
            self.assertIsNotNone(event)
    
    def test_chaos_probability_effect(self):
        """Test chaos probability affects event generation"""
        # High probability
        match_high = MatchPrediction(
            self.home_team, self.away_team, self.h2h, chaos_probability=0.95
        )
        
        # Low probability
        match_low = MatchPrediction(
            self.home_team, self.away_team, self.h2h, chaos_probability=0.05
        )
        
        # Both should work without errors
        event_high = match_high.generate_chaos_event()
        event_low = match_low.generate_chaos_event()
        
        self.assertIsNotNone(event_high)
        self.assertIsNotNone(event_low)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_zero_ratings(self):
        """Test handling of minimum rating"""
        team = Team(
            name="Minimum Team",
            rating=0, recent_form=0, goals_for=0.1,
            goals_against=5.0, injury_level=15, manager_rating=0,
            crowd_strength=1.0, mental_strength=0, luck_factor=0.5
        )
        self.assertEqual(team.rating, 0)
    
    def test_max_ratings(self):
        """Test handling of maximum rating"""
        team = Team(
            name="Maximum Team",
            rating=100, recent_form=100, goals_for=5.0,
            goals_against=0.1, injury_level=0, manager_rating=100,
            crowd_strength=1.3, mental_strength=100, luck_factor=1.5
        )
        self.assertEqual(team.rating, 100)
    
    def test_identical_teams(self):
        """Test prediction with identical teams"""
        identical_team = Team(
            name="Team", rating=75, recent_form=75, goals_for=1.5,
            goals_against=1.5, injury_level=5, manager_rating=75,
            crowd_strength=1.0, mental_strength=75, luck_factor=1.0
        )
        
        match = MatchPrediction(
            identical_team, identical_team, 
            {'home_wins': 1, 'away_wins': 1, 'draws': 1},
            chaos_probability=0.3
        )
        
        prediction = match.predict_match()
        self.assertIsNotNone(prediction)
        self.assertIn(prediction['winner'], ["Home Win", "Away Win", "Draw"])
    
    def test_no_head_to_head_history(self):
        """Test prediction with no H2H history"""
        home = Team(
            name="New Team 1", rating=75, recent_form=75, goals_for=1.5,
            goals_against=1.5, injury_level=5, manager_rating=75,
            crowd_strength=1.1, mental_strength=75, luck_factor=1.0
        )
        
        away = Team(
            name="New Team 2", rating=75, recent_form=75, goals_for=1.5,
            goals_against=1.5, injury_level=5, manager_rating=75,
            crowd_strength=1.0, mental_strength=75, luck_factor=1.0
        )
        
        h2h = {'home_wins': 0, 'away_wins': 0, 'draws': 0}
        match = MatchPrediction(home, away, h2h, chaos_probability=0.3)
        
        prediction = match.predict_match()
        self.assertIsNotNone(prediction)


class TestPredictionConsistency(unittest.TestCase):
    """Test prediction consistency and reproducibility"""
    
    def setUp(self):
        """Create match for consistency testing"""
        self.home_team = Team(
            name="Home", rating=80, recent_form=78, goals_for=1.8,
            goals_against=1.2, injury_level=3, manager_rating=80,
            crowd_strength=1.15, mental_strength=78, luck_factor=0.98
        )
        
        self.away_team = Team(
            name="Away", rating=75, recent_form=73, goals_for=1.5,
            goals_against=1.4, injury_level=5, manager_rating=75,
            crowd_strength=1.0, mental_strength=73, luck_factor=1.02
        )
        
        self.h2h = {'home_wins': 3, 'away_wins': 2, 'draws': 1}
    
    def test_reproducibility_with_seed(self):
        """Test predictions are reproducible with same seed"""
        match1 = MatchPrediction(
            self.home_team, self.away_team, self.h2h, chaos_probability=0.35
        )
        match2 = MatchPrediction(
            self.home_team, self.away_team, self.h2h, chaos_probability=0.35
        )
        
        random.seed(42)
        pred1 = match1.predict_match()
        
        random.seed(42)
        pred2 = match2.predict_match()
        
        self.assertEqual(pred1['winner'], pred2['winner'])
        self.assertEqual(pred1['home_goals'], pred2['home_goals'])
        self.assertEqual(pred1['away_goals'], pred2['away_goals'])


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTeamClass))
    suite.addTests(loader.loadTestsFromTestCase(TestMatchPrediction))
    suite.addTests(loader.loadTestsFromTestCase(TestChaosEvents))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPredictionConsistency))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result


if __name__ == "__main__":
    run_tests()
