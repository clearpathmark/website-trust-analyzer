import asyncio
from trust_analyzer import TrustAnalyzer

async def main():
    analyzer = TrustAnalyzer()
    url = "github.com"  # Example URL
    
    print(f"Analyzing trust factors for: {url}")
    print("=" * 50)
    
    # Run analysis
    results = await analyzer.analyze(url)
    
    # Print trust score results
    trust_score = results['trust_score']
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
    
    # Print recommendations if any
    if trust_score['recommendations']:
        print("\nRecommendations:")
        print("-" * 50)
        for i, rec in enumerate(trust_score['recommendations'], 1):
            print(f"{i}. {rec}")

if __name__ == "__main__":
    asyncio.run(main())