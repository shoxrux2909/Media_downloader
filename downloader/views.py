import os
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from .forms import DownloadForm
import yt_dlp
import tempfile

def download_video(request):
    video_file_path = None

    if request.method == "POST":
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            
            # Create a temporary file for download
            tmp_dir = tempfile.mkdtemp()
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": os.path.join(tmp_dir, "%(title)s.%(ext)s"),
                "noplaylist": True,
                "quiet": True,
                "merge_output_format": "mp4",
                # "nocheckcertificate": True,
                # "proxy": None  # avoid proxy issues
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_file_path = ydl.prepare_filename(info)

                if video_file_path and os.path.exists(video_file_path):
                    return FileResponse(open(video_file_path, "rb"), as_attachment=True, filename=os.path.basename(video_file_path))

            except Exception as e:
                return HttpResponse(f"Error downloading video: {e}")

    else:
        form = DownloadForm()

    return render(request, "download.html", {"form": form})
