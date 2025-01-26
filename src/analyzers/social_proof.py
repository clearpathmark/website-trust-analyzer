import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urljoin

class SocialProofAnalyzer:
    """Analyzes website social proof elements including reviews, testimonials, and team presence"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    async def analyze(self, url: str) -> Dict:
        """
        Analyze social proof elements on the website
        
        Args:
            url (str): Website URL to analyze
            
        Returns:
            Dict: Analysis results including presence of reviews, testimonials, and team info
        """
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            async with aiohttp.ClientSession(headers=self.headers) as session:
                results = {
                    'url': url,
                    'team_presence': await self._check_team_presence(session, url),
                    'social_profiles': await self._check_social_profiles(session, url),
                    'testimonials': await self._check_testimonials(session, url),
                    'review_presence': await self._check_review_presence(session, url)
                }
                
                return results
                
        except Exception as e:
            return {
                'url': url,
                'error': f"Analysis failed: {str(e)}",
                'status': 'failed'
            }
    
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
    
    async def _check_review_presence(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Check for review integration and review site links"""
        review_platforms = {
            'trustpilot': 'trustpilot.com',
            'google_reviews': 'google.com/reviews',
            'yelp': 'yelp.com',
            'bbb': 'bbb.org'
        }
        
        results = {
            'has_reviews': False,
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
                        for platform, domain in review_platforms.items():
                            if domain in href and platform not in results['platforms_found']:
                                results['platforms_found'].append(platform)
                                results['has_reviews'] = True
        except Exception as e:
            results['error'] = str(e)
            
        return results