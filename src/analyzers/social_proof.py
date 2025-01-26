import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import re

class SocialProofAnalyzer:
    """Analyzes website social proof elements including reviews, testimonials, and team presence"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Enhanced review platforms detection
        self.review_platforms = {
            'trustpilot': {
                'domain': 'trustpilot.com',
                'weight': 5,
                'patterns': [r'trustpilot\.com/review', r'trustpilot\.com/evaluate']
            },
            'google': {
                'domain': 'google.com',
                'weight': 4,
                'patterns': [r'google\.com/business', r'google\.com/maps/place', r'reviews\?hl=']
            },
            'yelp': {
                'domain': 'yelp.com',
                'weight': 3,
                'patterns': [r'yelp\.com/biz', r'yelp\.com/business']
            },
            'bbb': {
                'domain': 'bbb.org',
                'weight': 4,
                'patterns': [r'bbb\.org/business-reviews', r'bbb\.org/us/']
            },
            'sitejabber': {
                'domain': 'sitejabber.com',
                'weight': 3,
                'patterns': [r'sitejabber\.com/reviews']
            },
            'capterra': {
                'domain': 'capterra.com',
                'weight': 3,
                'patterns': [r'capterra\.com/reviews', r'capterra\.com/software']
            },
            'g2': {
                'domain': 'g2.com',
                'weight': 4,
                'patterns': [r'g2\.com/products']
            },
            'facebook': {
                'domain': 'facebook.com',
                'weight': 2,
                'patterns': [r'facebook\.com/.*/reviews', r'facebook\.com/pg/.*/reviews']
            }
        }
        
    async def analyze(self, url: str) -> Dict:
        """Analyze social proof elements on the website"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            async with aiohttp.ClientSession(headers=self.headers) as session:
                results = {
                    'url': url,
                    'team_presence': await self._check_team_presence(session, url),
                    'social_profiles': await self._check_social_profiles(session, url),
                    'testimonials': await self._check_testimonials(session, url),
                    'review_presence': await self._check_review_presence(session, url),
                    'review_diversity': await self._analyze_review_diversity(session, url)
                }
                
                return results
                
        except Exception as e:
            return {
                'url': url,
                'error': f"Analysis failed: {str(e)}",
                'status': 'failed'
            }

    async def _analyze_review_diversity(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Analyze the diversity and quality of review sources"""
        results = {
            'review_sources': [],
            'diversity_score': 0,
            'total_sources': 0,
            'primary_sources': [],
            'secondary_sources': [],
            'embedded_widgets': [],
            'status': 'checked'
        }
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Check for review platform links
                    for link in soup.find_all('a', href=True):
                        href = link['href'].lower()
                        for platform, info in self.review_platforms.items():
                            for pattern in info['patterns']:
                                if re.search(pattern, href):
                                    source_info = {
                                        'platform': platform,
                                        'url': href,
                                        'weight': info['weight']
                                    }
                                    results['review_sources'].append(source_info)
                                    if info['weight'] >= 4:
                                        results['primary_sources'].append(platform)
                                    else:
                                        results['secondary_sources'].append(platform)
                    
                    # Check for embedded review widgets
                    for script in soup.find_all('script', src=True):
                        src = script['src'].lower()
                        for platform, info in self.review_platforms.items():
                            if info['domain'] in src:
                                results['embedded_widgets'].append(platform)
                    
                    # Calculate diversity metrics
                    results['total_sources'] = len(results['review_sources'])
                    total_weight = sum(source['weight'] for source in results['review_sources'])
                    
                    # Calculate diversity score (0-10)
                    if results['total_sources'] > 0:
                        weighted_score = min(total_weight / 10, 1.0) * 10
                        platform_variety = min(results['total_sources'] / 5, 1.0) * 10
                        results['diversity_score'] = (weighted_score + platform_variety) / 2
                    
        except Exception as e:
            results['error'] = str(e)
            
        return results

    async def _check_team_presence(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Check for team/about pages and team member information"""
        team_paths = [
            '/team',
            '/about/team',
            '/about-us/team',
            '/our-team',
            '/about',
            '/about-us'
        ]
        
        results = {
            'has_team_page': False,
            'team_urls': [],
            'status': 'checked'
        }
        
        for path in team_paths:
            try:
                full_url = urljoin(url, path)
                async with session.head(full_url, allow_redirects=True) as response:
                    if response.status == 200:
                        results['has_team_page'] = True
                        results['team_urls'].append(full_url)
            except Exception:
                continue
                
        return results
    
    async def _check_social_profiles(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Check for social media profile links"""
        social_platforms = {
            'facebook': 'facebook.com',
            'twitter': 'twitter.com',
            'linkedin': 'linkedin.com',
            'instagram': 'instagram.com',
            'youtube': 'youtube.com'
        }
        
        results = {
            'has_social_profiles': False,
            'platforms_found': [],
            'status': 'checked'
        }
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    for link in soup.find_all('a', href=True):
                        href = link['href'].lower()
                        for platform, domain in social_platforms.items():
                            if domain in href and platform not in results['platforms_found']:
                                results['platforms_found'].append(platform)
                                results['has_social_profiles'] = True
        except Exception as e:
            results['error'] = str(e)
            
        return results
    
    async def _check_testimonials(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Check for testimonials and case studies"""
        testimonial_paths = [
            '/testimonials',
            '/reviews',
            '/case-studies',
            '/success-stories',
            '/what-our-customers-say'
        ]
        
        results = {
            'has_testimonials': False,
            'testimonial_urls': [],
            'status': 'checked'
        }
        
        for path in testimonial_paths:
            try:
                full_url = urljoin(url, path)
                async with session.head(full_url, allow_redirects=True) as response:
                    if response.status == 200:
                        results['has_testimonials'] = True
                        results['testimonial_urls'].append(full_url)
            except Exception:
                continue
                
        return results