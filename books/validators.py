from django.core.exceptions import ValidationError
from winmagic import magic
def validate_pdf(value):
        mime=magic.from_buffer(value.file.read(2048),mime=True)
        if value.size > 104857600:
            raise ValidationError("The maximum file size is 100MB")
        elif mime!='application/pdf' and mime!='application/epub+zip':
            raise ValidationError("Not a valid file, it should be pdf or epub")
        elif mime=='application/pdf' and value.name[-4:] != ".pdf":
            raise ValidationError("A PDF file must have .pdf extension")
        elif mime=='application/epub+zip' and value.name[-5:] != ".epub":
            raise ValidationError("A EPUB file must have .epub extension")
        return value

