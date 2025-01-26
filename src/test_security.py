import asyncio
from analyzers.website_security import WebsiteSecurityAnalyzer

async def test_security_analyzer():
    analyzer = WebsiteSecurityAnalyzer()
    
    # Test with a known secure website
    test_url = "github.com"  # Replace with your test URL
    
    print(f"Analyzing security for: {test_url}")
    results = await analyzer.analyze(test_url)
    
    # Print results
    print("\nAnalysis Results:")
    print("----------------")
    for key, value in results.items():
        print(f"\n{key}:")
        if isinstance(value, dict):
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {value}")

if __name__ == "__main__":
    asyncio.run(test_security_analyzer())