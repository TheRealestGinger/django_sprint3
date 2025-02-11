from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Post, Category


def get_posts():
    return Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    return render(request,
                  'blog/index.html',
                  {'post_list': get_posts()[0:5]})


def post_detail(request, post_id):
    return render(request,
                  'blog/detail.html',
                  {'post': get_object_or_404(
                      get_posts(),
                      id=post_id
                  )
                  })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(is_published=True),
        slug=category_slug
    )
    return render(request,
                  'blog/category.html',
                  {'category': category,
                   'post_list': get_posts(
                   ).filter(category__slug=category_slug)})
