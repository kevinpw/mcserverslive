def my_custom_upload_to_func():
	pass

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    'width': '100%',
    'height': '300',

    # Use proper language setting automatically (default)
 #   'lang': None

    # Or, set editor language/locale forcely
#    'lang': 'ko-KR',

    # Customize toolbar buttons
    'toolbar': [
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'clear']],
#        ['fontname', ['fontname']],
#        ['fontsize', ['fontsize']],
#        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
#        ['height', ['height']],
#        ['table', ['table']],
#        ['insert', ['link', 'picture', 'video', 'hr']],
        ['insert', ['link', 'video', 'hr', 'fullscreen', 'codeview']],
#        ['view', ['fullscreen']],
        ['help', ['help']],
    ],

    # Set `upload_to` function for attachments.
#    'attachment_upload_to': my_custom_upload_to_func(),

    # Set custom storage class for attachments.
#    'attachment_storage_class': 'my.custom.storage.class.name',

}
