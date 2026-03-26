from django.db import models
from django.utils.text import slugify

# chuyên mục (Category)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên chuyên mục")
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Chuyên mục"

# bài viết (Post)
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tiêu đề")
    body = models.TextField(verbose_name="Nội dung")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='posts',
        verbose_name="Chuyên mục"
    )
    
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Hình ảnh")
    audio = models.FileField(upload_to='audio/', null=True, blank=True, verbose_name="Âm thanh")
    video = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name="Video")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Bài viết"
        ordering = ['-date'] # Bài mới nhất hiện lên đầu