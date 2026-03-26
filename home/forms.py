from django import forms
import re
from django.contrib.auth.models import User
# Dòng này cực kỳ quan trọng: Nhập các Model từ file models.py sang đây
from .models import UserProfile, Project, ContactMessage, HomeContent

# 1. FORM ĐĂNG KÝ
class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', widget=forms.TextInput(attrs={'class': 'form-control rounded-pill mb-2'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control rounded-pill mb-2'}))
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill mb-2'}))
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill mb-2'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu nhập lại không khớp!")
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản không được chứa kí tự đặc biệt")   
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tài khoản này đã có người sử dụng")
        return username

    def save(self):
        return User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )

# 2. FORM ĐĂNG NHẬP
class LoginForm(forms.Form):
    username = forms.CharField(label='Tài khoản', widget=forms.TextInput(attrs={'class': 'form-control rounded-pill mb-2'}))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill mb-2'}))

# 3. FORM CẬP NHẬT ẢNH ĐẠI DIỆN
class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        labels = {'avatar': 'Chọn ảnh đại diện mới'}
        widgets = {'avatar': forms.FileInput(attrs={'class': 'form-control rounded-pill'})}

# 4. FORM SỬA HỒ SƠ & THÔNG TIN LIÊN HỆ
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'student_id', 'birth_date', 'gender', 'hometown', 
            'hobbies', 'university', 'major', 'class_name', 'academic_year',
            'github_url', 'phone', 'email_contact', 'address', 'facebook_url'
        ]
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control rounded-pill mb-2'})
            for field in [
                'full_name', 'student_id', 'birth_date', 'gender', 'hometown', 
                'university', 'major', 'class_name', 'academic_year',
                'github_url', 'phone', 'email_contact', 'address', 'facebook_url'
            ]
        }
        widgets['hobbies'] = forms.Textarea(attrs={'class': 'form-control rounded-4 mb-2', 'rows': 3})

# 5. FORM THÊM DỰ ÁN MỚI
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'border_color']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-pill mb-2', 'placeholder': 'Tên dự án...'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-4 mb-2', 'rows': 3}),
            'border_color': forms.Select(attrs={'class': 'form-select rounded-pill mb-2'}),
        }

# 6. FORM GỬI TIN NHẮN LIÊN HỆ
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-light border-0 py-2', 'placeholder': 'Nhập tên...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-light border-0 py-2', 'placeholder': 'Nhập email...'}),
            'subject': forms.TextInput(attrs={'class': 'form-control bg-light border-0 py-2', 'placeholder': 'Chủ đề...'}),
            'message': forms.Textarea(attrs={'class': 'form-control bg-light border-0 py-2', 'rows': 5, 'placeholder': 'Nội dung...'}),
        }

# 7. FORM CHỈNH SỬA TRANG CHỦ
class HomeContentForm(forms.ModelForm):
    class Meta:
        model = HomeContent
        fields = '__all__'
        widgets = {
            'greeting_title': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'greeting_text_1': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3}),
            'greeting_text_2': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3}),
            
            'col1_title': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'col1_icon': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'col1_text': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3}),
            
            'col2_title': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'col2_icon': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'col2_text': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3}),
            
            'col3_title': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'col3_icon': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'col3_text': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3}),
            
            'footer_text': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 2}),
            'footer_thanks': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
        }