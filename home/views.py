from django.shortcuts import render, redirect, get_object_or_404 # Thêm get_object_or_404 ở đây
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .forms import HomeContentForm 
from .models import HomeContent
from .models import UserProfile, Project, ContactMessage
from .forms import (
    RegistrationForm, LoginForm, AvatarUpdateForm, 
    UserProfileForm, ProjectForm, ContactForm
)

def edit_home(request):
    # Chỉ cho phép user đã đăng nhập vào sửa
    if not request.user.is_authenticated:
        return redirect('login')

    content, created = HomeContent.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = HomeContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tuyệt vời! Trang chủ đã được cập nhật.')
            return redirect('home') # Đảm bảo 'home' là tên url trang chủ của Sêu
    else:
        form = HomeContentForm(instance=content)

    return render(request, 'page/edit_home.html', {'form': form})
# 1. TRANG CHỦ
def home(request):
    # Lấy bản ghi duy nhất, nếu chưa có thì tạo mới bằng giá trị mặc định
    content, created = HomeContent.objects.get_or_create(pk=1)
    
    context = {
        'content': content
    }
    return render(request, 'page/home.html', context) # Đổi tên file HTML cho đúng đường dẫn của Sêu

# 2. TRANG THÔNG TIN CÁ NHÂN
@login_required(login_url='/login/')
def info(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    projects = request.user.projects.all().order_by('-id')
    
    profile_form = UserProfileForm(instance=profile)
    project_form = ProjectForm()

    return render(request, 'page/info.html', {
        'profile': profile, 'projects': projects,
        'profile_form': profile_form, 'project_form': project_form
    })

# 3. TRANG LIÊN HỆ
def contact(request):
    profile = UserProfile.objects.filter(user__is_superuser=True).first()
    contact_form = ContactForm()
    profile_form = UserProfileForm(instance=profile) if request.user.is_authenticated else None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'contact':
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                msg = contact_form.save() 
                subject = f"Tin nhắn mới từ: {msg.name}"
                content = f"Tiêu đề: {msg.subject}\nEmail khách: {msg.email}\nNội dung: {msg.message}"
                try:
                    send_mail(subject, content, 'yseu12006@gmail.com', ['yseu12006@gmail.com'], fail_silently=False)
                    messages.success(request, "Cảm ơn bạn! Tin nhắn đã bay thẳng đến Gmail của Sêu rồi nhé.")
                except Exception as e:
                    messages.warning(request, "Đã lưu tin nhắn, nhưng hệ thống mail đang bận xíu.")
                return redirect('contact')

        elif form_type == 'profile' and request.user.is_authenticated:
            profile_form = UserProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Đã cập nhật thông tin thành công!")
                return redirect('contact')

    return render(request, 'page/contact.html', {
        'profile': profile, 'form': contact_form, 'profile_form': profile_form
    })

# 4. QUẢN LÝ DỰ ÁN (THÊM - SỬA - XÓA)
@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user # Gán dự án cho đúng người dùng
            project.save()
            messages.success(request, "Đã phóng thêm một tên lửa dự án mới! ")
    return redirect('info')

@login_required
def edit_project(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Dự án đã được cập nhật thành công!")
            return redirect('info')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'page/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    project.delete()
    messages.success(request, "Dự án đã được gỡ bỏ gọn gàng.")
    return redirect('info')

# 5. QUẢN LÝ USER
def register(request):
    if request.user.is_authenticated: return redirect('/')
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            messages.success(request, "Đăng ký thành công!")
            return redirect('/login/') 
    return render(request, 'page/register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated: return redirect('/')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            messages.error(request, "Sai tài khoản hoặc mật khẩu!")
    return render(request, 'page/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def update_avatar(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AvatarUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AvatarUpdateForm(instance=profile)
    return render(request, 'page/update_avatar.html', {'form': form})