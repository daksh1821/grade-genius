#  def extract_text():
#         text = ""
#         with fitz.open(file_path) as doc:
#             for page_num in request.selected_pages:
#                 if 0 <= page_num < len(doc):
#                     text += doc[page_num].get_text()
#         return text