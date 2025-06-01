import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import pandas as pd

class ProfileRecommender:
    def __init__(self):
        self.feature_weights = {
            'age': 0.1,
            'location': 0.15,
            'religion': 0.1,
            'education_level': 0.1,
            'profession': 0.1,
            'smoking': 0.05,
            'drinking': 0.05,
            'diet': 0.05,
            'hobbies': 0.2,
            'languages': 0.1
        }
        
        self.categorical_features = ['gender', 'religion', 'location', 'education_level', 
                                   'profession', 'diet']
        self.numerical_features = ['age']
        self.binary_features = ['smoking', 'drinking']
        self.list_features = ['hobbies', 'languages']
        
        # Initialize transformers
        self.preprocessor = self._create_preprocessor()
        
    def _create_preprocessor(self):
        """Create a preprocessing pipeline for features"""
        transformers = [
            ('num', StandardScaler(), self.numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), self.categorical_features)
        ]
        return ColumnTransformer(transformers, remainder='drop')
    
    def _preprocess_list_features(self, profiles: List[Dict[str, Any]]) -> np.ndarray:
        """Convert list features (hobbies, languages) into binary vectors"""
        # Get all unique values for list features
        all_hobbies = set()
        all_languages = set()
        
        for profile in profiles:
            all_hobbies.update(profile['hobbies'])
            all_languages.update(profile['languages'])
            
        # Convert to sorted lists for consistent ordering
        all_hobbies = sorted(list(all_hobbies))
        all_languages = sorted(list(all_languages))
        
        # Create binary vectors
        hobby_vectors = []
        language_vectors = []
        
        for profile in profiles:
            hobby_vector = [1 if hobby in profile['hobbies'] else 0 for hobby in all_hobbies]
            language_vector = [1 if lang in profile['languages'] else 0 for lang in all_languages]
            hobby_vectors.append(hobby_vector)
            language_vectors.append(language_vector)
            
        return np.hstack([
            np.array(hobby_vectors) * self.feature_weights['hobbies'],
            np.array(language_vectors) * self.feature_weights['languages']
        ])
    
    def get_recommendations(self, 
                          liked_profiles: List[Dict[str, Any]], 
                          candidate_profiles: List[Dict[str, Any]], 
                          top_n: int = 10) -> List[Dict[str, Any]]:
        """Get recommendations based on liked profiles"""
        if not liked_profiles or not candidate_profiles:
            return []
        
        liked_df = pd.DataFrame(liked_profiles)
        candidate_df = pd.DataFrame(candidate_profiles)
        
        all_profiles_df = pd.concat([liked_df, candidate_df], axis=0)
        
        self.preprocessor.fit(all_profiles_df[self.numerical_features + self.categorical_features])
        
        # Transform liked and candidate profiles
        liked_features = self.preprocessor.transform(liked_df[self.numerical_features + self.categorical_features])
        candidate_features = self.preprocessor.transform(candidate_df[self.numerical_features + self.categorical_features])
        
        liked_binary = np.array(liked_df[self.binary_features].astype(float))
        candidate_binary = np.array(candidate_df[self.binary_features].astype(float))
        
        all_profiles = liked_profiles + candidate_profiles
        all_hobbies = set()
        all_languages = set()
        
        for profile in all_profiles:
            all_hobbies.update(profile.get('hobbies', []))
            all_languages.update(profile.get('languages', []))
            
        # Convert to sorted lists for consistent ordering
        all_hobbies = sorted(list(all_hobbies))
        all_languages = sorted(list(all_languages))
        
        # Create binary vectors for liked profiles
        liked_hobby_vectors = []
        liked_language_vectors = []
        
        for profile in liked_profiles:
            hobby_vector = [1 if hobby in profile.get('hobbies', []) else 0 for hobby in all_hobbies]
            language_vector = [1 if lang in profile.get('languages', []) else 0 for lang in all_languages]
            liked_hobby_vectors.append(hobby_vector)
            liked_language_vectors.append(language_vector)
            
        # Create binary vectors for candidate profiles
        candidate_hobby_vectors = []
        candidate_language_vectors = []
        
        for profile in candidate_profiles:
            hobby_vector = [1 if hobby in profile.get('hobbies', []) else 0 for hobby in all_hobbies]
            language_vector = [1 if lang in profile.get('languages', []) else 0 for lang in all_languages]
            candidate_hobby_vectors.append(hobby_vector)
            candidate_language_vectors.append(language_vector)
            
        # Convert to numpy arrays and apply weights
        liked_lists = np.hstack([
            np.array(liked_hobby_vectors) * self.feature_weights['hobbies'],
            np.array(liked_language_vectors) * self.feature_weights['languages']
        ])
        
        candidate_lists = np.hstack([
            np.array(candidate_hobby_vectors) * self.feature_weights['hobbies'],
            np.array(candidate_language_vectors) * self.feature_weights['languages']
        ])
        
        liked_features_array = liked_features.toarray() if hasattr(liked_features, 'toarray') else liked_features
        candidate_features_array = candidate_features.toarray() if hasattr(candidate_features, 'toarray') else candidate_features
        
        # Combine all features
        liked_combined = np.hstack([
            liked_features_array,
            liked_binary,
            liked_lists
        ])
        
        candidate_combined = np.hstack([
            candidate_features_array,
            candidate_binary,
            candidate_lists
        ])
        
        print(f"Liked combined shape: {liked_combined.shape}")
        print(f"Candidate combined shape: {candidate_combined.shape}")
        
        avg_liked_profile = np.mean(liked_combined, axis=0).reshape(1, -1)
        
        # Calculate similarity scores
        similarities = cosine_similarity(candidate_combined, avg_liked_profile)
        
        # Get top N recommendations
        top_indices = np.argsort(similarities.flatten())[-top_n:][::-1]
        
        return [candidate_profiles[i] for i in top_indices] 