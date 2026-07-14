from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category

def blog_list(request):
    post_list = Post.objects.filter(status='published')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__icontains=query)
        )
        
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        post_list = post_list.filter(category=category)
        
    # Tag filter
    tag_name = request.GET.get('tag')
    if tag_name:
        post_list = post_list.filter(tags__icontains=tag_name)

    # Pagination (6 posts per page)
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    
    # Extract recent posts
    recent_posts = Post.objects.filter(status='published').order_by('-published_date')[:4]

    context = {
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_query': query or '',
        'selected_category': category_slug or '',
        'selected_tag': tag_name or '',
    }
    return render(request, 'blog.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment views (safe from race conditions)
    Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
    # Refresh in-memory object to reflect database change
    post.refresh_from_db()
    
    # Get related posts (same category, excluding current post)
    related_posts = Post.objects.filter(status='published', category=post.category).exclude(pk=post.pk)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts
    }
    return render(request, 'blog_detail.html', context)
