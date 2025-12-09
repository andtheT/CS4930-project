from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import os

from .services import analyze_privacy_policy, PolicyScraper


def index(request):
    """Home page with URL input form."""
    return render(request, 'index.html')


def about(request):
    """About page."""
    return render(request, 'about.html')


def privacy(request):
    """Privacy policy page."""
    return render(request, 'privacy.html')


def analyze(request):
    """
    Handle privacy policy analysis request.
    Accepts POST with 'url' parameter.
    """
    if request.method != 'POST':
        return redirect('index')
    
    url = request.POST.get('url', '').strip()
    api_key = request.POST.get('api_key', '').strip()
    
    if not url:
        messages.error(request, 'Please enter a URL to analyze.')
        return redirect('index')
    
    # Ensure URL has a protocol
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    
    # Use provided API key or fall back to environment variable
    if not api_key:
        api_key = os.environ.get('OPENAI_API_KEY', '')
    
    # Perform analysis
    result = analyze_privacy_policy(url, api_key)
    
    context = {
        'url': url,
        'result': result,
        'has_error': result.get('error') is not None,
        'error_message': result.get('error', ''),
        'scrape_success': result.get('scrape_success', False),
        'analysis_success': result.get('analysis_success', False),
        'title': result.get('title', 'Privacy Policy Analysis'),
        'content_preview': result.get('content_preview', ''),
        'analysis': result.get('analysis', ''),
        'grade': result.get('grade', 'N/A'),
    }
    
    return render(request, 'results.html', context)


def results(request):
    """
    Results page - redirects to home if accessed directly without analysis.
    """
    # If accessed directly without POST data, redirect to home
    if request.method == 'GET' and not request.GET.get('url'):
        return redirect('index')
    
    # Handle GET request with URL parameter (for direct linking)
    url = request.GET.get('url', '').strip()
    api_key = request.GET.get('api_key', '').strip()
    
    if url:
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        
        if not api_key:
            api_key = os.environ.get('OPENAI_API_KEY', '')
        
        result = analyze_privacy_policy(url, api_key)
        
        context = {
            'url': url,
            'result': result,
            'has_error': result.get('error') is not None,
            'error_message': result.get('error', ''),
            'scrape_success': result.get('scrape_success', False),
            'analysis_success': result.get('analysis_success', False),
            'title': result.get('title', 'Privacy Policy Analysis'),
            'content_preview': result.get('content_preview', ''),
            'analysis': result.get('analysis', ''),
            'grade': result.get('grade', 'N/A'),
        }
        
        return render(request, 'results.html', context)
    
    return redirect('index')
