from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {"keywords":"Acer negundo","limit":2,"print_urls":True}
paths = response.download(arguments)
print(paths)