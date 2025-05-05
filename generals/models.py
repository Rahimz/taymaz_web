from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import fitz  # PyMuPDF
from PIL import Image
import io
import os
from django.core.files.base import ContentFile
from tools.models import TimeStampedModel


class Catalogue(TimeStampedModel):
    name = models.CharField(
        max_length=150,        
    )
    file = models.FileField(
        upload_to='catalogues/'        
    )
    resolution = models.PositiveSmallIntegerField(
        default=150
    )
    quality = models.PositiveSmallIntegerField(
        default=85
    )
    
    def __str__(self):
        return self.name


class CatalogueImage(TimeStampedModel):
    catalogue = models.ForeignKey(
        Catalogue,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        upload_to='catalogue/images/',        
    )
    page = models.PositiveSmallIntegerField(
        default=1
    )
    
    class Meta:
        ordering = ('page', )
        
    def __str__(self):
        return f"{self.catalogue.name} - Page {self.page}"
    
    
@receiver(post_save, sender=Catalogue)
def create_images_from_pdf(sender, instance, created, **kwargs):
    if created and instance.file:
        # Open the PDF file
        pdf_file = fitz.open(instance.file.path)
        
        for page_num in range(len(pdf_file)):
            # Get the page
            page = pdf_file.load_page(page_num)
            
            # Render page to an image (pix)
            pix = page.get_pixmap(dpi=instance.resolution)  # 300 DPI for good quality
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Save to BytesIO
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=instance.quality)
            
            # Create the CatalogueImage instance
            img_name = f"{instance.name}_page_{page_num + 1}_.jpg"
            img_file = ContentFile(img_io.getvalue(), name=img_name)
            
            CatalogueImage.objects.create(
                catalogue=instance,
                image=img_file,
                page=page_num + 1
            )
        
        pdf_file.close()