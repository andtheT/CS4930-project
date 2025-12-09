"""
Services for Policy Monster - Web Scraping and ChatGPT Analysis
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from openai import OpenAI


class PolicyScraper:
    """
    Web scraper for extracting privacy policy content from websites.
    """
    
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    
    # Common privacy policy URL patterns
    POLICY_PATTERNS = [
        '/privacy-policy',
        '/privacy',
        '/privacypolicy',
        '/legal/privacy',
        '/about/privacy',
        '/policies/privacy',
        '/terms/privacy',
    ]
    
    @classmethod
    def find_privacy_policy_link(cls, url: str) -> str | None:
        """
        Try to find a privacy policy link on the given page.
        """
        try:
            response = requests.get(url, headers=cls.HEADERS, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for links containing 'privacy' in href or text
            for link in soup.find_all('a', href=True):
                href = link.get('href', '').lower()
                text = link.get_text().lower()
                
                if 'privacy' in href or 'privacy' in text:
                    full_url = href
                    if href.startswith('/'):
                        # Relative URL - make it absolute
                        from urllib.parse import urljoin
                        full_url = urljoin(url, href)
                    elif not href.startswith('http'):
                        from urllib.parse import urljoin
                        full_url = urljoin(url, href)
                    return full_url
                    
            return None
        except Exception as e:
            print(f"Error finding privacy policy link: {e}")
            return None
    
    @classmethod
    def scrape_policy(cls, url: str) -> dict:
        """
        Scrape privacy policy content from a URL.
        Returns a dict with 'success', 'content', 'title', and 'error' keys.
        """
        result = {
            'success': False,
            'content': '',
            'title': '',
            'url': url,
            'error': None
        }
        
        try:
            response = requests.get(url, headers=cls.HEADERS, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get page title
            title_tag = soup.find('title')
            result['title'] = title_tag.get_text(strip=True) if title_tag else 'Privacy Policy'
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try multiple strategies to find main content
            content = None
            
            # Strategy 1: Look for article or main content areas
            main_selectors = [
                'article',
                'main',
                '[role="main"]',
                '.content',
                '.main-content',
                '#content',
                '#main-content',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.policy-content',
                '.privacy-policy',
                '.legal-content',
            ]
            
            for selector in main_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem
                    break
            
            # Strategy 2: Look for div with mw-content-text (Wikipedia style)
            if not content:
                content_div = soup.find('div', id='mw-content-text')
                if content_div:
                    parser_output = content_div.find('div', class_='mw-parser-output')
                    content = parser_output if parser_output else content_div
            
            # Strategy 3: Fall back to body
            if not content:
                content = soup.find('body')
            
            if content:
                # Extract text from paragraphs, lists, and headings
                text_parts = []
                
                for element in content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'div']):
                    text = element.get_text(strip=True)
                    if text and len(text) > 20:  # Filter out very short snippets
                        # Avoid duplicates from nested elements
                        if text not in text_parts:
                            text_parts.append(text)
                
                result['content'] = '\n\n'.join(text_parts)
                
                # Limit content length to avoid API limits
                if len(result['content']) > 30000:
                    result['content'] = result['content'][:30000] + "\n\n[Content truncated for analysis...]"
                
                result['success'] = True
            else:
                result['error'] = "Could not find policy content on the page."
                
        except requests.exceptions.RequestException as e:
            result['error'] = f"Failed to fetch the page: {str(e)}"
        except Exception as e:
            result['error'] = f"Error processing the page: {str(e)}"
        
        return result


class PolicyAnalyzer:
    """
    Analyzes privacy policies using OpenAI's ChatGPT API.
    """
    
    ANALYSIS_PROMPT = """You are a privacy policy expert. Analyze the following privacy policy and provide:

1. **Privacy Protection Grade**: Rate the policy from A+ (most protective) to F (least protective) based on how well it protects user privacy.

2. **Overall Summary**: A brief 2-3 sentence summary of what this policy covers.

3. **Key Findings**: List the most important points users should know, organized into:
   - **Good Practices** (things that protect users)
   - **Concerns** (things users should be aware of)
   - **Red Flags** (serious privacy concerns if any)

4. **Data Collection**: What types of data are collected?

5. **Data Sharing**: Who is the data shared with?

6. **User Rights**: What rights do users have over their data?

7. **Recommendations**: What should users do or be aware of?

Format your response in a clear, easy-to-read manner with headers and bullet points. Use simple language that anyone can understand.

Here is the privacy policy to analyze:

---
{policy_content}
---
"""

    @classmethod
    def analyze_policy(cls, policy_content: str, api_key: str) -> dict:
        """
        Analyze a privacy policy using ChatGPT.
        Returns a dict with 'success', 'analysis', 'grade', and 'error' keys.
        """
        result = {
            'success': False,
            'analysis': '',
            'grade': '',
            'error': None
        }
        
        if not api_key:
            result['error'] = "OpenAI API key is not configured. Please set the OPENAI_API_KEY."
            return result
        
        if not policy_content or len(policy_content.strip()) < 100:
            result['error'] = "Not enough policy content to analyze."
            return result
        
        try:
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert privacy policy analyst. Your goal is to help users understand privacy policies and make informed decisions about their data."
                    },
                    {
                        "role": "user",
                        "content": cls.ANALYSIS_PROMPT.format(policy_content=policy_content)
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            result['analysis'] = analysis_text
            result['success'] = True
            
            # Extract grade from the analysis
            grade_patterns = [
                r'\*\*Privacy Protection Grade\*\*:\s*([A-F][+-]?)',
                r'Grade:\s*([A-F][+-]?)',
                r'Rating:\s*([A-F][+-]?)',
                r'\b([A-F][+-]?)\b.*(?:grade|rating)',
            ]
            
            for pattern in grade_patterns:
                match = re.search(pattern, analysis_text, re.IGNORECASE)
                if match:
                    result['grade'] = match.group(1).upper()
                    break
            
            if not result['grade']:
                result['grade'] = 'N/A'
                
        except Exception as e:
            result['error'] = f"Error calling ChatGPT API: {str(e)}"
        
        return result


def analyze_privacy_policy(url: str, api_key: str = None) -> dict:
    """
    Main function to scrape and analyze a privacy policy.
    
    Args:
        url: The URL of the privacy policy page
        api_key: OpenAI API key (optional, will use environment variable if not provided)
    
    Returns:
        A dict containing the scrape and analysis results
    """
    # Use environment variable if API key not provided
    if not api_key:
        api_key = os.environ.get('OPENAI_API_KEY', '')
    
    result = {
        'url': url,
        'scrape_success': False,
        'analysis_success': False,
        'title': '',
        'content_preview': '',
        'analysis': '',
        'grade': '',
        'error': None
    }
    
    # Step 1: Scrape the policy
    scrape_result = PolicyScraper.scrape_policy(url)
    
    if not scrape_result['success']:
        result['error'] = scrape_result['error']
        return result
    
    result['scrape_success'] = True
    result['title'] = scrape_result['title']
    result['content_preview'] = scrape_result['content'][:500] + '...' if len(scrape_result['content']) > 500 else scrape_result['content']
    
    # Step 2: Analyze with ChatGPT
    analysis_result = PolicyAnalyzer.analyze_policy(scrape_result['content'], api_key)
    
    if not analysis_result['success']:
        result['error'] = analysis_result['error']
        return result
    
    result['analysis_success'] = True
    result['analysis'] = analysis_result['analysis']
    result['grade'] = analysis_result['grade']
    
    return result

