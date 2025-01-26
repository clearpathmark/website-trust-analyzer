from typing import Dict
from analyzers.website_security import WebsiteSecurityAnalyzer
from analyzers.social_proof import SocialProofAnalyzer
from analyzers.content_expertise import ContentExpertiseAnalyzer
from analyzers.scoring import TrustScore

class TrustAnalyzer:
    def __init__(self):
        self.security_analyzer = WebsiteSecurityAnalyzer()
        self.social_analyzer = SocialProofAnalyzer()
        self.content_analyzer = ContentExpertiseAnalyzer()
        self.scorer = TrustScore()
        
    async def analyze(self, url: str) -> Dict:
        """Perform comprehensive trust analysis of a website"""
        # Run all analyzers
        security_results = await self.security_analyzer.analyze(url)
        social_results = await self.social_analyzer.analyze(url)
        content_results = await self.content_analyzer.analyze(url)
        
        # Map analyzer results to scoring inputs
        security_data = self._map_security_data(security_results)
        review_data = self._map_review_data(social_results)
        business_data = self._map_business_data(security_results, social_results)
        content_data = self._map_content_data(content_results)
        transparency_data = self._map_transparency_data(security_results)
        
        # Calculate trust score
        trust_score = self.scorer.calculate_total_score(
            security_data,
            review_data,
            business_data,
            content_data,
            transparency_data
        )
        
        # Add detailed review diversity information to the results
        if 'review_diversity' in social_results:
            trust_score['review_diversity_details'] = social_results['review_diversity']
        
        return {
            'url': url,
            'trust_score': trust_score,
            'raw_results': {
                'security': security_results,
                'social': social_results,
                'content': content_results
            }
        }
    
    def _map_security_data(self, security_results: Dict) -> Dict:
        """Map security analyzer results to scoring format"""
        return {
            'ssl_certificate': security_results.get('ssl_certificate', {}),
            'security_headers': security_results.get('security_headers', {})
        }
    
    def _map_review_data(self, social_results: Dict) -> Dict:
        """Map social proof analyzer results to review scoring format with enhanced diversity metrics"""
        testimonials = social_results.get('testimonials', {})
        review_presence = social_results.get('review_presence', {})
        review_diversity = social_results.get('review_diversity', {})
        
        # Calculate review strength based on multiple factors
        has_reviews = testimonials.get('has_testimonials', False) or review_presence.get('has_reviews', False)
        recent_reviews = bool(testimonials.get('testimonial_urls', []))
        
        # New diversity metrics
        diversity_score = review_diversity.get('diversity_score', 0)
        primary_sources = len(review_diversity.get('primary_sources', []))
        total_sources = review_diversity.get('total_sources', 0)
        has_embedded_widgets = bool(review_diversity.get('embedded_widgets', []))
        
        # Determine review diversity based on enhanced metrics
        diverse_reviews = (
            total_sources >= 3 or  # Has multiple review sources
            (primary_sources >= 2 and has_embedded_widgets) or  # Has major platforms and widgets
            diversity_score >= 7.0  # High diversity score
        )
        
        return {
            'has_reviews': has_reviews,
            'recent_reviews': recent_reviews,
            'diverse_reviews': diverse_reviews,
            'review_metrics': {
                'diversity_score': diversity_score,
                'primary_sources': primary_sources,
                'total_sources': total_sources,
                'has_widgets': has_embedded_widgets
            }
        }
    
    def _map_business_data(self, security_results: Dict, social_results: Dict) -> Dict:
        """Map analyzer results to business verification scoring format"""
        contact_info = security_results.get('contact_info', {})
        team_presence = social_results.get('team_presence', {})
        
        return {
            'has_credentials': team_presence.get('has_team_page', False),
            'contact_verified': contact_info.get('has_contact_page', False)
        }
    
    def _map_content_data(self, content_results: Dict) -> Dict:
        """Map content analyzer results to scoring format"""
        return {
            'has_resources': content_results.get('documentation', {}).get('has_documentation', False),
            'recent_content': content_results.get('blog_presence', {}).get('content_freshness') == 'Recent content found',
            'expert_content': content_results.get('thought_leadership', {}).get('has_thought_leadership', False)
        }
    
    def _map_transparency_data(self, security_results: Dict) -> Dict:
        """Map analyzer results to transparency scoring format"""
        privacy = security_results.get('privacy_policy', {})
        
        return {
            'has_privacy_policy': privacy.get('has_privacy_policy', False),
            'has_terms': True if privacy.get('policy_urls', []) else False,
            'clear_pricing': False  # To be implemented with pricing detection
        }