from analyzers.scoring import TrustScore

def main():
    # Create sample data
    security_data = {
        'ssl_certificate': {'status': 'valid'},
        'security_headers': {
            'has_hsts': True,
            'has_xframe': True,
            'has_content_security': True,
            'has_xss_protection': True
        }
    }
    
    review_data = {
        'has_reviews': True,
        'recent_reviews': True,
        'diverse_reviews': True
    }
    
    business_data = {
        'has_credentials': True,
        'contact_verified': True
    }
    
    content_data = {
        'has_resources': True,
        'recent_content': True,
        'expert_content': True
    }
    
    transparency_data = {
        'has_privacy_policy': True,
        'has_terms': True,
        'clear_pricing': True
    }
    
    # Calculate score
    scorer = TrustScore()
    results = scorer.calculate_total_score(
        security_data,
        review_data,
        business_data,
        content_data,
        transparency_data
    )
    
    # Print results
    print("\nTrust Score Analysis")
    print("=" * 50)
    print(f"Total Score: {results['total_score']:.2f}")
    print(f"Trust Level: {results['trust_level']}")
    
    print("\nComponent Scores:")
    print("-" * 50)
    for name, component in results['components'].items():
        print(f"\n{name.replace('_', ' ').title()}:")
        print(f"Score: {component.score}/{component.max_score}")
        print("Details:")
        for key, value in component.details.items():
            print(f"  - {key}: {value}")
            
    if results['recommendations']:
        print("\nRecommendations:")
        print("-" * 50)
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"{i}. {rec}")

if __name__ == "__main__":
    main()