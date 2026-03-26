from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q 
from .models import Post, Category
from .forms import PostForm


def blog(request, category_slug=None):
    query = request.GET.get('q', '').strip()
    category = None
    
    # lấy tất cả bài viết và danh sách chuyên mục
    posts = Post.objects.all().order_by('-date')
    categories = Category.objects.all()
    
    # lọc theo chuyên mục 
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    
    # lọc theo từ khóa tìm kiếm
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).distinct()

    return render(request, 'blog/blog.html', {
        'posts': posts, 
        'categories': categories, 
        'category': category, 
        'search_query': query,
    })

# chi tiết bài viết
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/detail.html', {'post': post})

# hàm tạo bài viết
@login_required(login_url='/login/')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Chúc mừng {request.user.username}! Bài viết mới đã được lên sóng thành công.')
            return redirect('blog:post_list') 
    return render(request, 'blog/create_post.html', {'form': form})

# hàm sửa bài viết
@login_required(login_url='/login/')
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.user.username} ơi, đã lưu các thay đổi!')
            return redirect('blog:post_detail', id=post.id) 
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

# hàm xóa bài viết
@login_required(login_url='/login/')
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, f'{request.user.username} ơi, đã xóa bài viết thành công.')
    return redirect('blog:post_list') 

# hàm xóa chủ đề dành cho Admin dọn dẹp
@login_required(login_url='/login/')
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    cat_name = category.name
    category.delete() 
    messages.success(request, f'Đã xóa chủ đề "{cat_name}" dọn dẹp sạch sẽ!')
    return redirect('blog:post_list')