from django.db import models
from django.contrib.auth.models import User

# 1. Bảng Bài Viết
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# 2. Bảng Trang Chủ
class HomeContent(models.Model):
    # Lời chào trên cùng
    greeting_title = models.CharField(max_length=200, default='Chào mừng bạn đến với "Góc Nhỏ Của Mình"', verbose_name="Tiêu đề chào mừng")
    greeting_text_1 = models.TextField(default='Nơi mình lưu giữ những điều giản dị nhưng ý nghĩa...', verbose_name="Đoạn giới thiệu 1")
    greeting_text_2 = models.TextField(default='Mình là Sêu - một người đang cố gắng mỗi ngày...', verbose_name="Đoạn giới thiệu 2")
    
    # Cột 1: Học tập
    col1_title = models.CharField(max_length=100, default='Hành trình học tập', verbose_name="Tiêu đề Cột 1 (Học tập)")
    col1_text = models.TextField(default='Học tập là con đường rèn luyện tư duy...', verbose_name="Nội dung Cột 1")
    
    # Cột 2: Âm nhạc
    col2_title = models.CharField(max_length=100, default='Giai điệu cuộc sống', verbose_name="Tiêu đề Cột 2 (Âm nhạc)")
    col2_text = models.TextField(default='Âm nhạc là một phần không thể thiếu...', verbose_name="Nội dung Cột 2")
    
    # Cột 3: Thể thao
    col3_title = models.CharField(max_length=100, default='Đam mê sân cỏ', verbose_name="Tiêu đề Cột 3 (Thể thao)")
    col3_text = models.TextField(default='Đá bóng không chỉ là thể thao...', verbose_name="Nội dung Cột 3")
    
    # Lời kết
    footer_text = models.TextField(default='“Góc Nhỏ Của Sêu” sẽ là nơi mình chia sẻ...', verbose_name="Lời nhắn gửi cuối trang")
    footer_thanks = models.CharField(max_length=200, default='Cảm ơn bạn đã đến với góc nhỏ của mình', verbose_name="Lời cảm ơn (In đậm)")

    def save(self, *args, **kwargs):
        self.pk = 1 
        super(HomeContent, self).save(*args, **kwargs)

    def __str__(self):
        return "Nội dung Trang Chủ"
# 3. Bảng Hồ Sơ 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', null=True, blank=True)
    
    full_name = models.CharField(max_length=100, default="Sêu", verbose_name="Họ và tên")
    birth_date = models.CharField(max_length=50, default="15/01/2006", verbose_name="Ngày sinh")
    gender = models.CharField(max_length=10, default="Nam", verbose_name="Giới tính")
    hometown = models.CharField(max_length=200, default="Xã Ia Băng, Gia Lai", verbose_name="Quê quán")
    hobbies = models.TextField(default="Thích nghe nhạc, Chơi thể thao, Chơi guitar và piano, Rất thích hát...", verbose_name="Sở thích")
    
    student_id = models.CharField(max_length=20, default="107937", verbose_name="Mã sinh viên")
    academic_year = models.CharField(max_length=20, default="2024-2028", verbose_name="Khóa học")
    university = models.CharField(max_length=200, default="Đại học Đông Á", verbose_name="Trường học")
    major = models.CharField(max_length=200, default="Công nghệ thông tin", verbose_name="Chuyên ngành")
    class_name = models.CharField(max_length=50, default="IT24B", verbose_name="Lớp")
    github_url = models.URLField(max_length=200, blank=True, verbose_name="Link GitHub")

    phone = models.CharField(max_length=15, default="0348337534", verbose_name="Số điện thoại")
    email_contact = models.EmailField(default="yseu17924@gmail.com", verbose_name="Email liên lạc")
    address = models.CharField(max_length=255, default="Gia Lai, Việt Nam", verbose_name="Địa chỉ")
    facebook_url = models.URLField(max_length=200, blank=True, verbose_name="Link Facebook")
    
    def __str__(self):
        return f"Hồ sơ của {self.user.username}"

# 4. Bảng Dự Án 
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200, verbose_name="Tên dự án")
    description = models.TextField(verbose_name="Mô tả dự án")
    
    COLOR_CHOICES = [
        ('primary', 'Xanh dương'),
        ('success', 'Xanh lá'),
        ('danger', 'Đỏ'),
        ('warning', 'Vàng'),
        ('dark', 'Đen'),
    ]
    border_color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='primary')

    def __str__(self):
        return self.title

# 5. Bảng Tin Nhắn Liên Hệ
class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên người gửi")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Tiêu đề")
    message = models.TextField(verbose_name="Nội dung")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày gửi")

    def __str__(self):
        return f"{self.name} - {self.subject}"