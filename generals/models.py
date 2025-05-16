from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import fitz  # PyMuPDF
from PIL import Image
import io
import os
from django.core.files.base import ContentFile
from django.utils.functional import cached_property

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

    @cached_property
    def filesize(self):
        """
        Returns the file's size in a human-readable format.
        """
        if self.file:
            try:
                size_bytes = self.file.size
                # Convert to human-readable format
                for unit in ['bytes', 'KB', 'MB', 'GB']:
                    if size_bytes < 1024.0:
                        return f"{size_bytes:.1f} {unit}"
                    size_bytes /= 1024.0
                return f"{size_bytes:.1f} TB"
            except (ValueError, OSError):
                return "0 bytes"
        return "0 bytes"


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
        try:
            # Open the PDF file
            pdf_file = fitz.open(instance.file.path)
            
            for page_num in range(len(pdf_file)):
                try:
                    # Get the page
                    page = pdf_file.load_page(page_num)
                    
                    # Render page to an image (pix)
                    pix = page.get_pixmap(dpi=instance.resolution)
                    
                    # Convert to PIL Image
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    
                    # Create in-memory image file
                    img_io = io.BytesIO()
                    img.save(img_io, format='JPEG', quality=instance.quality)
                    img_io.seek(0)
                    
                    # Create and save the CatalogueImage instance immediately
                    img_name = f"{instance.name}_page_{page_num + 1}.jpg"
                    CatalogueImage.objects.create(
                        catalogue=instance,
                        image=ContentFile(img_io.getvalue(), name=img_name),
                        page=page_num + 1
                    )
                    
                    # Explicitly clean up
                    del img
                    del pix
                    del page
                    img_io.close()
                    
                except Exception as page_error:
                    print(f"Error processing page {page_num + 1}: {str(page_error)}")
                    continue
                        
        except Exception as e:
            print(f"Error processing PDF {instance.file.name}: {str(e)}")
            # Consider adding some cleanup here if needed
        #     # Get the page
        #     page = pdf_file.load_page(page_num)
            
        #     # Render page to an image (pix)
        #     pix = page.get_pixmap(dpi=instance.resolution)  # 300 DPI for good quality
            
        #     # Convert to PIL Image
        #     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
        #     # Save to BytesIO
        #     img_io = io.BytesIO()
        #     img.save(img_io, format='JPEG', quality=instance.quality)
            
        #     # Create the CatalogueImage instance
        #     img_name = f"{instance.name}_page_{page_num + 1}_.jpg"
        #     img_file = ContentFile(img_io.getvalue(), name=img_name)
            
        #     CatalogueImage.objects.create(
        #         catalogue=instance,
        #         image=img_file,
        #         page=page_num + 1
        #     )
        
        # pdf_file.close()