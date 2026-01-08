# backend/data_sources/api_client.py - Real API Integrations
"""
Real-time data fetching from various sources:
- Twitter/X API
- Reddit API
- News APIs
- Google Play Store reviews
"""

import os
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterClient:
    """Twitter/X API client for fetching complaints"""
    
    def __init__(self):
        # FORCE FREE MODE: Twitter API is paid, so always use mock data
        # Set FORCE_FREE_MODE=True to ensure no paid API usage
        force_free_mode = os.getenv('FORCE_FREE_MODE', 'true').lower() == 'true'
        
        if force_free_mode:
            self.bearer_token = ''  # Force mock data (free)
            self.enabled = False
        else:
            self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN', '')
            self.enabled = bool(self.bearer_token) and not force_free_mode
        
        self.api_url = "https://api.twitter.com/2"
        # Always default to mock if no token (FREE)
        if not self.bearer_token:
            self.enabled = False
    
    def search_tweets(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search tweets for financial product complaints"""
        if not self.enabled:
            logger.warning("Twitter API not configured. Using mock data.")
            return self._mock_tweets(query, max_results)
        
        try:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
            params = {
                "query": query,
                "max_results": min(max_results, 100),
                "tweet.fields": "created_at,author_id,public_metrics"
            }
            
            response = requests.get(
                f"{self.api_url}/tweets/search/recent",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                tweets = []
                for tweet in data.get('data', []):
                    tweets.append({
                        'text': tweet.get('text', ''),
                        'source': 'twitter',
                        'source_id': tweet.get('id', ''),
                        'author': tweet.get('author_id', ''),
                        'review_date': datetime.fromisoformat(
                            tweet.get('created_at', '').replace('Z', '+00:00')
                        ),
                        'engagement': tweet.get('public_metrics', {})
                    })
                return tweets
            else:
                logger.error(f"Twitter API error: {response.status_code}")
                return self._mock_tweets(query, max_results)
        
        except Exception as e:
            logger.error(f"Twitter API error: {e}")
            return self._mock_tweets(query, max_results)
    
    def _mock_tweets(self, query: str, max_results: int) -> List[Dict]:
        """Mock tweets for demo when API not available"""
        return [
            {
                'text': f"Complaint about {query}: Hidden charges everywhere!",
                'source': 'twitter',
                'source_id': f'tweet_{i}',
                'author': f'user_{i}',
                'review_date': datetime.utcnow() - timedelta(days=i),
                'engagement': {'likes': i*10, 'retweets': i*2}
            }
            for i in range(min(max_results, 10))
        ]


class RedditClient:
    """Reddit API client for fetching discussions"""
    
    def __init__(self):
        self.client_id = os.getenv('REDDIT_CLIENT_ID', '')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET', '')
        self.user_agent = "VeritasFinance/1.0"
        self.enabled = bool(self.client_id and self.client_secret)
        self.access_token = None
        self.token_expires = None
    
    def _get_access_token(self) -> Optional[str]:
        """Get Reddit OAuth access token"""
        if not self.enabled:
            return None
        
        if self.access_token and self.token_expires and datetime.utcnow() < self.token_expires:
            return self.access_token
        
        try:
            auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
            data = {'grant_type': 'client_credentials'}
            headers = {'User-Agent': self.user_agent}
            
            response = requests.post(
                'https://www.reddit.com/api/v1/access_token',
                auth=auth,
                data=data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires = datetime.utcnow() + timedelta(seconds=expires_in)
                return self.access_token
        except Exception as e:
            logger.error(f"Reddit auth error: {e}")
        
        return None
    
    def search_posts(self, query: str, subreddit: str = 'all', limit: int = 100) -> List[Dict]:
        """Search Reddit posts"""
        if not self.enabled:
            logger.warning("Reddit API not configured. Using mock data.")
            return self._mock_posts(query, limit)
        
        token = self._get_access_token()
        if not token:
            return self._mock_posts(query, limit)
        
        try:
            headers = {
                'Authorization': f'bearer {token}',
                'User-Agent': self.user_agent
            }
            
            response = requests.get(
                f'https://oauth.reddit.com/r/{subreddit}/search',
                headers=headers,
                params={'q': query, 'limit': min(limit, 100), 'sort': 'new'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                posts = []
                for post in data.get('data', {}).get('children', []):
                    post_data = post.get('data', {})
                    posts.append({
                        'text': f"{post_data.get('title', '')} {post_data.get('selftext', '')}",
                        'source': 'reddit',
                        'source_id': post_data.get('id', ''),
                        'author': post_data.get('author', ''),
                        'review_date': datetime.fromtimestamp(
                            post_data.get('created_utc', 0)
                        ),
                        'upvotes': post_data.get('ups', 0),
                        'subreddit': post_data.get('subreddit', '')
                    })
                return posts
            else:
                logger.error(f"Reddit API error: {response.status_code}")
                return self._mock_posts(query, limit)
        
        except Exception as e:
            logger.error(f"Reddit API error: {e}")
            return self._mock_posts(query, limit)
    
    def _mock_posts(self, query: str, limit: int) -> List[Dict]:
        """Mock Reddit posts for demo"""
        return [
            {
                'text': f"Reddit discussion about {query}: Beware of hidden fees!",
                'source': 'reddit',
                'source_id': f'reddit_{i}',
                'author': f'redditor_{i}',
                'review_date': datetime.utcnow() - timedelta(days=i),
                'upvotes': i*5,
                'subreddit': 'personalfinance'
            }
            for i in range(min(limit, 10))
        ]


class NewsAPIClient:
    """News API client for financial news"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY', '')
        self.api_url = "https://newsapi.org/v2"
        self.enabled = bool(self.api_key)
    
    def search_news(self, query: str, max_results: int = 50) -> List[Dict]:
        """Search news articles"""
        if not self.enabled:
            logger.warning("News API not configured. Using mock data.")
            return self._mock_news(query, max_results)
        
        try:
            response = requests.get(
                f"{self.api_url}/everything",
                params={
                    'q': query,
                    'apiKey': self.api_key,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': min(max_results, 100)
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', ''),
                        'text': f"{article.get('title', '')} {article.get('description', '')}",
                        'source': 'news',
                        'source_id': article.get('url', ''),
                        'author': article.get('author', ''),
                        'review_date': datetime.fromisoformat(
                            article.get('publishedAt', '').replace('Z', '+00:00')
                        ) if article.get('publishedAt') else datetime.utcnow(),
                        'url': article.get('url', '')
                    })
                return articles
            else:
                logger.error(f"News API error: {response.status_code}")
                return self._mock_news(query, max_results)
        
        except Exception as e:
            logger.error(f"News API error: {e}")
            return self._mock_news(query, max_results)
    
    def _mock_news(self, query: str, max_results: int) -> List[Dict]:
        """Mock news articles for demo"""
        return [
            {
                'title': f"Financial News: {query} under scrutiny",
                'text': f"News article about {query} regulatory concerns",
                'source': 'news',
                'source_id': f'news_{i}',
                'author': f'reporter_{i}',
                'review_date': datetime.utcnow() - timedelta(days=i),
                'url': f'https://example.com/news/{i}'
            }
            for i in range(min(max_results, 10))
        ]


class DataSourceAggregator:
    """Aggregates data from all sources"""
    
    def __init__(self):
        self.twitter = TwitterClient()
        self.reddit = RedditClient()
        self.news = NewsAPIClient()
    
    def fetch_all_sources(self, product_name: str, max_per_source: int = 50) -> List[Dict]:
        """Fetch data from all available sources"""
        all_data = []
        
        # Search queries
        queries = [
            product_name,
            f"{product_name} complaint",
            f"{product_name} review",
            f"{product_name} scam",
            f"{product_name} fraud"
        ]
        
        for query in queries[:2]:  # Limit to avoid rate limits
            # Twitter
            tweets = self.twitter.search_tweets(query, max_per_source)
            all_data.extend(tweets)
            time.sleep(1)  # Rate limiting
            
            # Reddit
            posts = self.reddit.search_posts(query, limit=max_per_source)
            all_data.extend(posts)
            time.sleep(1)
            
            # News (only once)
            if query == product_name:
                articles = self.news.search_news(query, max_per_source)
                all_data.extend(articles)
        
        return all_data
    
    def get_status(self) -> Dict[str, bool]:
        """Get status of all data sources"""
        return {
            'twitter': self.twitter.enabled,
            'reddit': self.reddit.enabled,
            'news': self.news.enabled
        }


if __name__ == "__main__":
    # Test data sources
    aggregator = DataSourceAggregator()
    print("Data Sources Status:")
    print(aggregator.get_status())
    
    print("\nFetching sample data...")
    data = aggregator.fetch_all_sources("Alpha Growth Mutual Fund", max_per_source=5)
    print(f"Fetched {len(data)} items")
    for item in data[:3]:
        print(f"- {item['source']}: {item['text'][:100]}...")
