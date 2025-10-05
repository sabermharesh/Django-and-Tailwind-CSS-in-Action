from django.db import models
from publishers.models import Publisher
from authors.models import Author
from django.utils.text import slugify
import uuid

# import for qrcode generation
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
# Create your models here.

class BookTitle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Book position: {self.title}"
    
    def save(self,*args, **kwargs):
        if not self.slug:
            # generate the slug
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Book(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=24, blank=True)
    # qr_code rq_codes/name.png
    # http://127.0.0.1:8000/media/qr_codes/name.png
    qr_code = models.ImageField(upload_to='qr_codes',blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args,**kwargs):
        # if not self.book_id:
        #     self.book_id = str(uuid.uuid4()).replace("-","")[:24].lower()

        # # generate qr code 
        # qrcode_img = qrcode.make(self.book_id)
        # canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
        # canvas.paste(qrcode_img)
        # fname = f'qr_code-{self.title}.png'
        # buffer = BytesIO()
        # canvas.save(buffer, 'PNG')
        # self.qr_code.save(fname, File(buffer), save=False)
        # canvas.close()
        # super().save(*args,**kwargs)

        # def save(self, *args, **kwargs):
        if not self.book_id:
            self.book_id = str(uuid.uuid4()).replace("-", "")[:24].lower()

        if not self.qr_code:
            qrcode_img = qrcode.make(self.book_id)

            buffer = BytesIO()
            qrcode_img.save(buffer, format='PNG')

            fname = f'qr_code-{self.title.title}.png'
            self.qr_code.save(fname, File(buffer), save=False)

        super().save(*args, **kwargs)
