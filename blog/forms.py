from django import forms
from .models import Post, Category 

class PostForm(forms.ModelForm):
    category_name = forms.CharField(
        max_length=100, 
        required=False, 
        label="Chủ đề bài viết",
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-pill mb-2', 
            'placeholder': 'Nhập tên chủ đề (VD: Góc Chill, Code Dạo...)'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'category_name', 'body', 'image', 'audio', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-pill mb-2', 'placeholder': 'Nhập tiêu đề bài viết...'}),
            'body': forms.Textarea(attrs={'class': 'form-control rounded-4 mb-2', 'placeholder': 'Bạn đang nghĩ gì thế?'}),
            'image': forms.FileInput(attrs={'class': 'form-control rounded-pill mb-2'}),
            'audio': forms.FileInput(attrs={'class': 'form-control rounded-pill mb-2'}),
            'video': forms.FileInput(attrs={'class': 'form-control rounded-pill mb-2'}),
        }

    # Hàm này giúp hiển thị lại tên chủ đề cũ khi bấm vào Sửa bài viết
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.category:
            self.fields['category_name'].initial = self.instance.category.name

    # Hàm tự động tìm hoặc tạo mới chủ đề khi lưu bài
    def save(self, commit=True):
        post = super().save(commit=False) 
        cat_name = self.cleaned_data.get('category_name') 
        
        if cat_name:
            category, created = Category.objects.get_or_create(name=cat_name.strip())
            post.category = category
        else:
            post.category = None 
            
        if commit:
            post.save()
        return post