from typing import Dict, List, TypedDict, Optional
from dataclasses import dataclass

@dataclass
class ScoreComponent:
    score: float
    max_score: float
    details: Dict[str, any]
    recommendations: List[str]

class TrustScore:
    def __init__(self):
        self.score_weights = {
            'technical_security': 15,
            'reviews_ratings': 15,
            'business_verification': 10,
            'review_quality': 15,
            'social_proof': 15,
            'content_quality': 15,
            'transparency': 15
        }
        
    def calculate_technical_score(self, security_data: Dict) -> ScoreComponent:
        """Calculate technical security score"""
        score = 0
        details = {}
        recommendations = []
        
        # SSL/HTTPS (5 points)
        if security_data.get('ssl_certificate', {}).get('status') == 'valid':
            score += 5
            details['ssl'] = 'Valid SSL certificate'
        else:
            recommendations.append('Implement HTTPS with a valid SSL certificate')
            details['ssl'] = 'Missing or invalid SSL certificate'
            
        # Security Headers (5 points)
        headers = security_data.get('security_headers', {})
        header_score = 0
        if headers.get('has_hsts'): header_score += 1
        if headers.get('has_xframe'): header_score += 1
        if headers.get('has_content_security'): header_score += 1
        if headers.get('has_xss_protection'): header_score += 1
        
        score += header_score
        details['security_headers'] = f'Implemented {header_score}/4 security headers'
        
        if header_score < 4:
            recommendations.append('Implement missing security headers')
            
        # Domain factors (5 points) - placeholder for now
        score += 5
        
        return ScoreComponent(
            score=score,
            max_score=15,
            details=details,
            recommendations=recommendations
        )
        
    def calculate_review_score(self, review_data: Dict) -> ScoreComponent:
        """Calculate review and ratings score"""
        score = 0
        details = {}
        recommendations = []
        
        # Review presence (5 points)
        has_reviews = review_data.get('has_reviews', False)
        if has_reviews:
            score += 5
            details['review_presence'] = 'Has user reviews'
        else:
            recommendations.append('Implement a review system')
            details['review_presence'] = 'No user reviews found'
            
        # Review freshness (5 points)
        if review_data.get('recent_reviews', False):
            score += 5
            details['freshness'] = 'Has recent reviews'
        else:
            recommendations.append('Encourage recent reviews')
            details['freshness'] = 'No recent reviews'
            
        # Review diversity (5 points)
        if review_data.get('diverse_reviews', False):
            score += 5
            details['diversity'] = 'Has diverse reviews'
        else:
            recommendations.append('Encourage reviews from diverse sources')
            details['diversity'] = 'Limited review diversity'
            
        return ScoreComponent(
            score=score,
            max_score=15,
            details=details,
            recommendations=recommendations
        )
        
    def calculate_business_verification_score(self, business_data: Dict) -> ScoreComponent:
        """Calculate business verification score"""
        score = 0
        details = {}
        recommendations = []
        
        # Business credentials (5 points)
        if business_data.get('has_credentials', False):
            score += 5
            details['credentials'] = 'Business credentials verified'
        else:
            recommendations.append('Add business verification credentials')
            details['credentials'] = 'Missing business credentials'
            
        # Contact verification (5 points)
        if business_data.get('contact_verified', False):
            score += 5
            details['contact'] = 'Contact information verified'
        else:
            recommendations.append('Add verified contact information')
            details['contact'] = 'Contact information not verified'
            
        return ScoreComponent(
            score=score,
            max_score=10,
            details=details,
            recommendations=recommendations
        )
        
    def calculate_content_score(self, content_data: Dict) -> ScoreComponent:
        """Calculate content quality score"""
        score = 0
        details = {}
        recommendations = []
        
        # Resource quality (5 points)
        if content_data.get('has_resources', False):
            score += 5
            details['resources'] = 'Quality resources present'
        else:
            recommendations.append('Add high-quality resources and documentation')
            details['resources'] = 'Missing or low-quality resources'
            
        # Content freshness (5 points)
        if content_data.get('recent_content', False):
            score += 5
            details['freshness'] = 'Content is up to date'
        else:
            recommendations.append('Update content regularly')
            details['freshness'] = 'Content needs updating'
            
        # Expert content (5 points)
        if content_data.get('expert_content', False):
            score += 5
            details['expertise'] = 'Expert content present'
        else:
            recommendations.append('Add expert-level content')
            details['expertise'] = 'Missing expert content'
            
        return ScoreComponent(
            score=score,
            max_score=15,
            details=details,
            recommendations=recommendations
        )
        
    def calculate_transparency_score(self, transparency_data: Dict) -> ScoreComponent:
        """Calculate transparency score"""
        score = 0
        details = {}
        recommendations = []
        
        # Privacy policy (5 points)
        if transparency_data.get('has_privacy_policy', False):
            score += 5
            details['privacy'] = 'Clear privacy policy'
        else:
            recommendations.append('Add clear privacy policy')
            details['privacy'] = 'Missing privacy policy'
            
        # Terms & conditions (5 points)
        if transparency_data.get('has_terms', False):
            score += 5
            details['terms'] = 'Clear terms and conditions'
        else:
            recommendations.append('Add clear terms and conditions')
            details['terms'] = 'Missing terms and conditions'
            
        # Pricing transparency (5 points)
        if transparency_data.get('clear_pricing', False):
            score += 5
            details['pricing'] = 'Clear pricing information'
        else:
            recommendations.append('Add clear pricing information')
            details['pricing'] = 'Unclear pricing information'
            
        return ScoreComponent(
            score=score,
            max_score=15,
            details=details,
            recommendations=recommendations
        )
        
    def calculate_total_score(self, 
                            security_data: Dict,
                            review_data: Dict,
                            business_data: Dict,
                            content_data: Dict,
                            transparency_data: Dict) -> Dict:
        """Calculate overall trust score"""
        components = {
            'technical_security': self.calculate_technical_score(security_data),
            'reviews_ratings': self.calculate_review_score(review_data),
            'business_verification': self.calculate_business_verification_score(business_data),
            'content_quality': self.calculate_content_score(content_data),
            'transparency': self.calculate_transparency_score(transparency_data)
        }
        
        total_score = sum(comp.score for comp in components.values())
        max_possible = sum(comp.max_score for comp in components.values())
        
        # Normalize to 100-point scale
        normalized_score = (total_score / max_possible) * 100
        
        # Get all recommendations
        recommendations = []
        for comp in components.values():
            recommendations.extend(comp.recommendations)
            
        # Categorize trust level
        trust_level = self._categorize_trust_level(normalized_score)
        
        return {
            'total_score': normalized_score,
            'trust_level': trust_level,
            'components': components,
            'recommendations': recommendations
        }
        
    def _categorize_trust_level(self, score: float) -> str:
        """Categorize the trust level based on score"""
        if score >= 90:
            return 'Exceptional Trust'
        elif score >= 80:
            return 'High Trust'
        elif score >= 70:
            return 'Good Trust'
        elif score >= 60:
            return 'Moderate Trust'
        else:
            return 'Needs Improvement'