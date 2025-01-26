import asyncio
from analyzers.social_proof import SocialProofAnalyzer

async def main():
    analyzer = SocialProofAnalyzer()
    url = "github.com"
    print(f"Analyzing social proof for: {url}")
    
    # Run the analysis
    results = await analyzer.analyze(url)
    
    # Print results in a structured way
    print("\nAnalysis Results:")
    print("-" * 50)
    for key, value in results.items():
        print(f"\n{key.upper()}:")
        if isinstance(value, dict):
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {value}")

if __name__ == "__main__":
    asyncio.run(main())