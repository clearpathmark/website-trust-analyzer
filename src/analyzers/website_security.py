import ssl
import socket
import aiohttp
from urllib.parse import urlparse
from typing import Dict, List, Optional

class WebsiteSecurityAnalyzer:
    """Analyzes website security aspects including SSL, privacy policy, and contact information"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    async def analyze(self, url: str) -> Dict:
        """
        Analyze website security aspects
        
        Args:
            url (str): Website URL to analyze
            
        Returns:
            Dict: Analysis results including SSL status, privacy policy, and security indicators
        """
        try:
            # Normalize URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            async with aiohttp.ClientSession() as session:
                results = {
                    'url': url,
                    'ssl_certificate': await self._check_ssl(url),
                    'privacy_policy': await self._check_privacy_policy(session, url),
                    'contact_info': await self._check_contact_info(session, url),
                    'security_headers': await self._check_security_headers(session, url)
                }
                
                return results
                
        except Exception as e:
            return {
                'url': url,
                'error': f"Analysis failed: {str(e)}",
                'status': 'failed'
            }
    
    async def _check_ssl(self, url: str) -> Dict:
        """Check SSL certificate status and details"""
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
            return {
                'status': 'valid',
                'issuer': dict(x[0] for x in cert['issuer']),
                'expiry': cert['notAfter'],
                'version': cert['version']
            }
        except Exception as e:
            return {
                'status': 'invalid',
                'error': str(e)
            }
    
    async def _check_privacy_policy(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Check for presence of privacy policy"""
        common_paths = [
            '/privacy',
            '/privacy-policy',
            '/privacy-notice',
            '/legal/privacy'
        ]
        
        results = {
            'has_privacy_policy': False,
            'policy_urls': [],
            'status': 'checked'
        }
        
        for path in common_paths:
            try:
                full_url = url.rstrip('/') + path
                async with session.head(full_url, allow_redirects=True) as response:
                    if response.status == 200:
                        results['has_privacy_policy'] = True
                        results['policy_urls'].append(full_url)
            except Exception as e:
                continue
                
        return results
    
    async def _check_contact_info(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Check for presence of contact information"""
        common_paths = [
            '/contact',
            '/contact-us',
            '/about',
            '/about-us'
        ]
        
        results = {
            'has_contact_page': False,
            'contact_urls': [],
            'status': 'checked'
        }
        
        for path in common_paths:
            try:
                full_url = url.rstrip('/') + path
                async with session.head(full_url, allow_redirects=True) as response:
                    if response.status == 200:
                        results['has_contact_page'] = True
                        results['contact_urls'].append(full_url)
            except Exception as e:
                continue
                
        return results
        
    async def _check_security_headers(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Check security-related HTTP headers"""
        try:
            async with session.head(url) as response:
                headers = response.headers
                return {
                    'has_hsts': 'Strict-Transport-Security' in headers,
                    'has_xframe': 'X-Frame-Options' in headers,
                    'has_content_security': 'Content-Security-Policy' in headers,
                    'has_xss_protection': 'X-XSS-Protection' in headers,
                    'status': 'checked'
                }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }