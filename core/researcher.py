from ddgs import DDGS
import trafilatura
import concurrent.futures

class DeepResearcher:
    def __init__(self, brain):
        self.brain = brain
        self.ddgs = DDGS()

    def perform_deep_research(self, topic):
        """Searches multiple sources, scrapes them, and returns raw data."""
        print(f"[Researcher] Deep research started for: {topic}")
        
        # 1. Get Top 5 Links
        results = self.ddgs.text(topic, max_results=5)
        if not results: return "No sources found."
        
        links = [r['href'] for r in results]
        titles = [r['title'] for r in results]
        
        # 2. Scrape all links in parallel
        sources_content = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self._scrape, url): url for url in links}
            for future in concurrent.futures.as_completed(future_to_url):
                content = future.result()
                if content:
                    sources_content.append(content[:1500]) # Cap per source

        if not sources_content: return "Could not extract data from sources."

        # 3. Formulate Synthesis Prompt
        combined_data = "\n\n--- SOURCE ---\n".join(sources_content)
        research_prompt = f"""
        Research Topic: {topic}
        
        I found multiple sources. Here is the raw data:
        {combined_data}
        
        TASK:
        1. Summarize the answer based on ALL sources.
        2. If sources conflict, mention the disagreement (Misinformation check).
        3. Provide internal citations like [Source 1].
        """
        
        # 4. Ask Brain to synthesize
        return self.brain.query_lm_studio(research_prompt)

    def _scrape(self, url):
        try:
            downloaded = trafilatura.fetch_url(url)
            return trafilatura.extract(downloaded)
        except: return None
