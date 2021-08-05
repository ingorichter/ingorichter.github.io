+++
title = "TIL - Organize a Folder of Thousands of Images Into Subfolders"
categories = ["TIL"]
tags = ["exiftool", "organisation", "TIL", "notetomyself", "shell"]
date = 2021-08-05
draft = false
+++
[1]: https://www.exiftool.org/ "ExifTool"
[2]: https://www.exiftool.org/filename.html "ExifTool Examples"
[3]: https://nextcloud.com/ "Nextcloud"

## Reorg Time

I use [Nextclouds][3] image upload feature to backup all photos from my phone. I recently discovered that you could upload pictures from your phone into subfolders in the `YEAR/MONTH/DAY/picturefile` format.

After switching this feature on, I realized that all my previously uploaded 3000+ images and short videos lie flat in the Pictures folder. I needed a solution to organize all existing photos into the same subfolder structure.

I was thinking about writing a shell script and using [ExifTool][1] to read the EXIF metadata and move the pictures into their respective folder location based on their creation date. After checking the [ExifTool][1] documentation, I found out that [ExifTool][1] itself can help with this task. No need to write a script unless you need something very, very special.

This is what I used to reorganize all pictures files into their respective subfolders:

{{< highlight bash >}}
exiftool -d %Y/%m/%d "-directory<filemodifydate" "-directory<createdate" "-directory<datetimeoriginal" .
{{< /highlight >}}

This one-liner will inspect all files in the current directory (.), examine the `filemodifydate`, `createdate` and `datetimeoriginal` exif tags in that order to determine the needed information to move the file into a subdirectory that will match the year (%Y), month (%m) and day (%d).

More examples about [ExifTools][1] superpower is available from the [example page][2].