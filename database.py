"""
Database module for sports prediction system
Handles team data, match history, and prediction storage
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path


class PredictionDatabase:
    """Manages SQLite database for prediction system"""
    
    def __init__(self, db_path="sports_predictions.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database connection and tables"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.create_tables()
            print(f"✓ Database initialized at {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    def create_tables(self):
        """Create all required tables"""
        # Teams table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                rating INTEGER DEFAULT 70,
                recent_form INTEGER DEFAULT 70,
                goals_for REAL DEFAULT 1.5,
                goals_against REAL DEFAULT 1.5,
                injury_level INTEGER DEFAULT 0,
                manager_rating INTEGER DEFAULT 70,
                crowd_strength REAL DEFAULT 1.0,
                mental_strength INTEGER DEFAULT 70,
                luck_factor REAL DEFAULT 1.0,
                league TEXT,
                country TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Matches table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                home_goals INTEGER,
                away_goals INTEGER,
                match_date TIMESTAMP,
                league TEXT,
                status TEXT DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
            )
        ''')
        
        # Head-to-head history table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS head_to_head (
                h2h_id INTEGER PRIMARY KEY AUTOINCREMENT,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                home_wins INTEGER DEFAULT 0,
                away_wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
                UNIQUE(home_team_id, away_team_id)
            )
        ''')
        
        # Predictions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                predicted_winner TEXT,
                predicted_confidence REAL,
                predicted_home_goals INTEGER,
                predicted_away_goals INTEGER,
                prediction_analysis TEXT,
                chaos_event TEXT,
                prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actual_result TEXT,
                accuracy_score REAL,
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
            )
        ''')
        
        # Prediction accuracy stats table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accuracy_stats (
                stats_id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_predictions INTEGER DEFAULT 0,
                correct_predictions INTEGER DEFAULT 0,
                accuracy_percentage REAL DEFAULT 0.0,
                win_accuracy REAL DEFAULT 0.0,
                draw_accuracy REAL DEFAULT 0.0,
                loss_accuracy REAL DEFAULT 0.0,
                avg_confidence REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    # ==================== TEAM OPERATIONS ====================
    
    def add_team(self, team_data):
        """Add a new team to database"""
        try:
            self.cursor.execute('''
                INSERT INTO teams (
                    name, rating, recent_form, goals_for, goals_against,
                    injury_level, manager_rating, crowd_strength, 
                    mental_strength, luck_factor, league, country
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                team_data['name'],
                team_data.get('rating', 70),
                team_data.get('recent_form', 70),
                team_data.get('goals_for', 1.5),
                team_data.get('goals_against', 1.5),
                team_data.get('injury_level', 0),
                team_data.get('manager_rating', 70),
                team_data.get('crowd_strength', 1.0),
                team_data.get('mental_strength', 70),
                team_data.get('luck_factor', 1.0),
                team_data.get('league'),
                team_data.get('country')
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"✗ Team '{team_data['name']}' already exists")
            return None
        except sqlite3.Error as e:
            print(f"✗ Error adding team: {e}")
            return None
    
    def get_team_by_name(self, team_name):
        """Get team by name"""
        try:
            self.cursor.execute('SELECT * FROM teams WHERE name = ?', (team_name,))
            result = self.cursor.fetchone()
            if result:
                return self._convert_team_row(result)
            return None
        except sqlite3.Error as e:
            print(f"✗ Error getting team: {e}")
            return None
    
    def get_team_by_id(self, team_id):
        """Get team by ID"""
        try:
            self.cursor.execute('SELECT * FROM teams WHERE team_id = ?', (team_id,))
            result = self.cursor.fetchone()
            if result:
                return self._convert_team_row(result)
            return None
        except sqlite3.Error as e:
            print(f"✗ Error getting team: {e}")
            return None
    
    def get_all_teams(self):
        """Get all teams"""
        try:
            self.cursor.execute('SELECT * FROM teams ORDER BY name')
            results = self.cursor.fetchall()
            return [self._convert_team_row(row) for row in results]
        except sqlite3.Error as e:
            print(f"✗ Error getting teams: {e}")
            return []
    
    def update_team(self, team_id, team_data):
        """Update team information"""
        try:
            update_fields = []
            values = []
            
            for key, value in team_data.items():
                if key != 'team_id':
                    update_fields.append(f"{key} = ?")
                    values.append(value)
            
            if not update_fields:
                return False
            
            values.append(team_id)
            query = f"UPDATE teams SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE team_id = ?"
            
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"✗ Error updating team: {e}")
            return False
    
    def delete_team(self, team_id):
        """Delete team from database"""
        try:
            self.cursor.execute('DELETE FROM teams WHERE team_id = ?', (team_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"✗ Error deleting team: {e}")
            return False
    
    def _convert_team_row(self, row):
        """Convert database row to team dictionary"""
        columns = ['team_id', 'name', 'rating', 'recent_form', 'goals_for', 
                  'goals_against', 'injury_level', 'manager_rating', 'crowd_strength',
                  'mental_strength', 'luck_factor', 'league', 'country', 'created_at', 'updated_at']
        return dict(zip(columns, row))
    
    # ==================== MATCH OPERATIONS ====================
    
    def add_match(self, home_team_id, away_team_id, match_date=None, league=None):
        """Add a new match"""
        try:
            self.cursor.execute('''
                INSERT INTO matches (home_team_id, away_team_id, match_date, league, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (home_team_id, away_team_id, match_date, league, 'scheduled'))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"✗ Error adding match: {e}")
            return None
    
    def get_match_by_id(self, match_id):
        """Get match by ID"""
        try:
            self.cursor.execute('SELECT * FROM matches WHERE match_id = ?', (match_id,))
            result = self.cursor.fetchone()
            if result:
                return self._convert_match_row(result)
            return None
        except sqlite3.Error as e:
            print(f"✗ Error getting match: {e}")
            return None
    
    def get_team_matches(self, team_id, limit=10):
        """Get recent matches for a team"""
        try:
            query = '''
                SELECT * FROM matches 
                WHERE home_team_id = ? OR away_team_id = ?
                ORDER BY match_date DESC
                LIMIT ?
            '''
            self.cursor.execute(query, (team_id, team_id, limit))
            results = self.cursor.fetchall()
            return [self._convert_match_row(row) for row in results]
        except sqlite3.Error as e:
            print(f"✗ Error getting matches: {e}")
            return []
    
    def update_match_result(self, match_id, home_goals, away_goals, status='completed'):
        """Update match with actual result"""
        try:
            self.cursor.execute('''
                UPDATE matches 
                SET home_goals = ?, away_goals = ?, status = ?
                WHERE match_id = ?
            ''', (home_goals, away_goals, status, match_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"✗ Error updating match: {e}")
            return False
    
    def _convert_match_row(self, row):
        """Convert database row to match dictionary"""
        columns = ['match_id', 'home_team_id', 'away_team_id', 'home_goals', 
                  'away_goals', 'match_date', 'league', 'status', 'created_at']
        return dict(zip(columns, row))
    
    # ==================== HEAD-TO-HEAD OPERATIONS ====================
    
    def get_h2h_record(self, home_team_id, away_team_id):
        """Get head-to-head record"""
        try:
            self.cursor.execute('''
                SELECT home_wins, away_wins, draws FROM head_to_head
                WHERE home_team_id = ? AND away_team_id = ?
            ''', (home_team_id, away_team_id))
            result = self.cursor.fetchone()
            if result:
                return {'home_wins': result[0], 'away_wins': result[1], 'draws': result[2]}
            return {'home_wins': 0, 'away_wins': 0, 'draws': 0}
        except sqlite3.Error as e:
            print(f"✗ Error getting H2H record: {e}")
            return {'home_wins': 0, 'away_wins': 0, 'draws': 0}
    
    def update_h2h_record(self, home_team_id, away_team_id, home_goals, away_goals):
        """Update H2H record after match completion"""
        try:
            record = self.get_h2h_record(home_team_id, away_team_id)
            
            if home_goals > away_goals:
                record['home_wins'] += 1
            elif away_goals > home_goals:
                record['away_wins'] += 1
            else:
                record['draws'] += 1
            
            # Check if record exists
            self.cursor.execute('''
                SELECT h2h_id FROM head_to_head
                WHERE home_team_id = ? AND away_team_id = ?
            ''', (home_team_id, away_team_id))
            
            if self.cursor.fetchone():
                # Update existing
                self.cursor.execute('''
                    UPDATE head_to_head
                    SET home_wins = ?, away_wins = ?, draws = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE home_team_id = ? AND away_team_id = ?
                ''', (record['home_wins'], record['away_wins'], record['draws'], 
                      home_team_id, away_team_id))
            else:
                # Insert new
                self.cursor.execute('''
                    INSERT INTO head_to_head (home_team_id, away_team_id, home_wins, away_wins, draws)
                    VALUES (?, ?, ?, ?, ?)
                ''', (home_team_id, away_team_id, record['home_wins'], 
                      record['away_wins'], record['draws']))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ Error updating H2H record: {e}")
            return False
    
    # ==================== PREDICTION OPERATIONS ====================
    
    def store_prediction(self, prediction_data):
        """Store prediction in database"""
        try:
            analysis_json = json.dumps(prediction_data.get('analysis', {}))
            
            self.cursor.execute('''
                INSERT INTO predictions (
                    match_id, home_team_id, away_team_id, predicted_winner,
                    predicted_confidence, predicted_home_goals, predicted_away_goals,
                    prediction_analysis, chaos_event
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prediction_data.get('match_id'),
                prediction_data['home_team_id'],
                prediction_data['away_team_id'],
                prediction_data.get('winner'),
                prediction_data.get('confidence'),
                prediction_data.get('home_goals'),
                prediction_data.get('away_goals'),
                analysis_json,
                prediction_data.get('chaos_event')
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"✗ Error storing prediction: {e}")
            return None
    
    def get_prediction_by_id(self, prediction_id):
        """Get prediction by ID"""
        try:
            self.cursor.execute('SELECT * FROM predictions WHERE prediction_id = ?', 
                              (prediction_id,))
            result = self.cursor.fetchone()
            if result:
                return self._convert_prediction_row(result)
            return None
        except sqlite3.Error as e:
            print(f"✗ Error getting prediction: {e}")
            return None
    
    def get_match_predictions(self, match_id):
        """Get all predictions for a match"""
        try:
            self.cursor.execute(
                'SELECT * FROM predictions WHERE match_id = ? ORDER BY prediction_date DESC',
                (match_id,)
            )
            results = self.cursor.fetchall()
            return [self._convert_prediction_row(row) for row in results]
        except sqlite3.Error as e:
            print(f"✗ Error getting predictions: {e}")
            return []
    
    def update_prediction_result(self, prediction_id, actual_result, accuracy_score=None):
        """Update prediction with actual match result"""
        try:
            self.cursor.execute('''
                UPDATE predictions
                SET actual_result = ?, accuracy_score = ?
                WHERE prediction_id = ?
            ''', (actual_result, accuracy_score, prediction_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"✗ Error updating prediction: {e}")
            return False
    
    def _convert_prediction_row(self, row):
        """Convert database row to prediction dictionary"""
        columns = ['prediction_id', 'match_id', 'home_team_id', 'away_team_id',
                  'predicted_winner', 'predicted_confidence', 'predicted_home_goals',
                  'predicted_away_goals', 'prediction_analysis', 'chaos_event',
                  'prediction_date', 'actual_result', 'accuracy_score']
        data = dict(zip(columns, row))
        try:
            data['prediction_analysis'] = json.loads(data['prediction_analysis'])
        except:
            data['prediction_analysis'] = {}
        return data
    
    # ==================== ACCURACY STATISTICS ====================
    
    def calculate_accuracy_stats(self):
        """Calculate and update accuracy statistics"""
        try:
            # Get total predictions
            self.cursor.execute(
                'SELECT COUNT(*) FROM predictions WHERE actual_result IS NOT NULL'
            )
            total = self.cursor.fetchone()[0]
            
            if total == 0:
                return None
            
            # Get correct predictions
            self.cursor.execute('''
                SELECT COUNT(*) FROM predictions 
                WHERE actual_result = predicted_winner AND actual_result IS NOT NULL
            ''')
            correct = self.cursor.fetchone()[0]
            
            accuracy = (correct / total * 100) if total > 0 else 0
            
            # Update stats
            self.cursor.execute('''
                DELETE FROM accuracy_stats
            ''')
            
            self.cursor.execute('''
                INSERT INTO accuracy_stats (total_predictions, correct_predictions, accuracy_percentage)
                VALUES (?, ?, ?)
            ''', (total, correct, accuracy))
            
            self.conn.commit()
            return {'total': total, 'correct': correct, 'accuracy': accuracy}
        except sqlite3.Error as e:
            print(f"✗ Error calculating stats: {e}")
            return None
    
    def get_accuracy_stats(self):
        """Get current accuracy statistics"""
        try:
            self.cursor.execute('SELECT * FROM accuracy_stats ORDER BY last_updated DESC LIMIT 1')
            result = self.cursor.fetchone()
            if result:
                columns = ['stats_id', 'total_predictions', 'correct_predictions', 
                          'accuracy_percentage', 'win_accuracy', 'draw_accuracy',
                          'loss_accuracy', 'avg_confidence', 'last_updated']
                return dict(zip(columns, result))
            return None
        except sqlite3.Error as e:
            print(f"✗ Error getting stats: {e}")
            return None
    
    # ==================== UTILITY OPERATIONS ====================
    
    def get_database_summary(self):
        """Get summary statistics of database"""
        try:
            summary = {}
            
            # Count teams
            self.cursor.execute('SELECT COUNT(*) FROM teams')
            summary['total_teams'] = self.cursor.fetchone()[0]
            
            # Count matches
            self.cursor.execute('SELECT COUNT(*) FROM matches')
            summary['total_matches'] = self.cursor.fetchone()[0]
            
            # Count predictions
            self.cursor.execute('SELECT COUNT(*) FROM predictions')
            summary['total_predictions'] = self.cursor.fetchone()[0]
            
            # Get accuracy
            accuracy = self.get_accuracy_stats()
            summary['accuracy_stats'] = accuracy
            
            return summary
        except sqlite3.Error as e:
            print(f"✗ Error getting summary: {e}")
            return {}
    
    def export_data(self, export_format='json'):
        """Export database to file"""
        try:
            summary = self.get_database_summary()
            
            # Get all data
            self.cursor.execute('SELECT * FROM teams')
            teams = [dict(zip([col[0] for col in self.cursor.description], row)) 
                    for row in self.cursor.fetchall()]
            
            self.cursor.execute('SELECT * FROM matches')
            matches = [dict(zip([col[0] for col in self.cursor.description], row)) 
                      for row in self.cursor.fetchall()]
            
            if export_format == 'json':
                export_data = {
                    'timestamp': datetime.now().isoformat(),
                    'summary': summary,
                    'teams': teams,
                    'matches': matches
                }
                return json.dumps(export_data, indent=2, default=str)
            
            return None
        except sqlite3.Error as e:
            print(f"✗ Error exporting data: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    db = PredictionDatabase()
    
    print("\n" + "="*70)
    print("DATABASE INITIALIZATION EXAMPLE")
    print("="*70)
    
    # Add sample teams
    sample_teams = [
        {
            'name': 'Manchester United',
            'rating': 85,
            'recent_form': 82,
            'goals_for': 2.1,
            'goals_against': 0.9,
            'injury_level': 2,
            'manager_rating': 85,
            'crowd_strength': 1.15,
            'mental_strength': 85,
            'luck_factor': 1.05,
            'league': 'Premier League',
            'country': 'England'
        },
        {
            'name': 'Liverpool',
            'rating': 86,
            'recent_form': 84,
            'goals_for': 2.2,
            'goals_against': 0.8,
            'injury_level': 3,
            'manager_rating': 87,
            'crowd_strength': 1.16,
            'mental_strength': 86,
            'luck_factor': 1.06,
            'league': 'Premier League',
            'country': 'England'
        }
    ]
    
    print("\n✓ Adding sample teams...")
    for team in sample_teams:
        team_id = db.add_team(team)
        if team_id:
            print(f"  Added: {team['name']} (ID: {team_id})")
    
    # Get teams
    print("\n✓ Retrieved teams:")
    all_teams = db.get_all_teams()
    for team in all_teams:
        print(f"  - {team['name']}: Rating {team['rating']}")
    
    # Get database summary
    print("\n✓ Database Summary:")
    summary = db.get_database_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*70)
    db.close()
