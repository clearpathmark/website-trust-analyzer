import asyncio
from trust_analyzer import TrustAnalyzer

async def main():
    analyzer = TrustAnalyzer()
    url = "github.com"
    print(f"Analyzing trust factors for: {url}")
    print("=" * 50)
    
    # Run analysis
    results = await analyzer.analyze(url)
    trust_score = results['trust_score']
    
    # Print overall scores
    print(f"\nOverall Trust Score: {trust_score['total_score']:.2f}")
    print(f"Trust Level: {trust_score['trust_level']}")
    
    # Print component scores
    print("\nComponent Scores:")
    print("-" * 50)
    for name, component in trust_score['components'].items():
        print(f"\n{name.replace('_', ' ').title()}:")
        print(f"Score: {component.score}/{component.max_score}")
        print("Details:")
        for key, value in component.details.items():
            print(f"  - {key}: {value}")
            
        # Show detailed review metrics for review ratings
        if name == 'reviews_ratings' and 'review_metrics' in component.details:
            metrics = component.details['review_metrics']
            print("\nDetailed Review Metrics:")
            print(f"  - Diversity Score: {metrics.get('diversity_score', 0):.1f}/10")
            print(f"  - Primary Review Sources: {metrics.get('primary_sources', 0)}")
            print(f"  - Total Review Sources: {metrics.get('total_sources', 0)}")
            print(f"  - Has Review Widgets: {'Yes' if metrics.get('has_widgets', False) else 'No'}")
    
    # Print review diversity details if available
    if 'review_diversity_details' in trust_score:
        diversity = trust_score['review_diversity_details']
        print("\nReview Sources Analysis:")
        print("-" * 50)
        print(f"Total Review Platforms: {diversity.get('total_sources', 0)}")
        
        if diversity.get('primary_sources'):
            print("\nPrimary Review Sources:")
            for source in diversity.get('primary_sources', []):
                print(f"  - {source}")
                
        if diversity.get('secondary_sources'):
            print("\nSecondary Review Sources:")
            for source in diversity.get('secondary_sources', []):
                print(f"  - {source}")
                
        if diversity.get('embedded_widgets'):
            print("\nEmbedded Review Widgets:")
            for widget in diversity.get('embedded_widgets', []):
                print(f"  - {widget}")
    
    # Print recommendations
    if trust_score['recommendations']:
        print("\nRecommendations:")
        print("-" * 50)
        for i, rec in enumerate(trust_score['recommendations'], 1):
            print(f"{i}. {rec}")

if __name__ == "__main__":
    asyncio.run(main())