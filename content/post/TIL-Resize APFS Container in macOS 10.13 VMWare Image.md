+++
title = "Resize APFS Container in macOS 10.13 VMWare Image"
description = "Resize APFS VoContainerlume in macOS 10.13 VMWare Image"
categories = ["Tips", "Tricks"]
tags = ["TIL", "VMWare", "Tricks", "Notes"]
featuredalt = ""
linktitle = ""
date = "2018-03-07T22:45:27-07:00"
author = "Ingo Richter"
+++

## Resize VMWare Disk size

VMWare provides an option to resize the Hard disk of a VM. The Settings dialog provides this option under **Hard Disk**.
If the VM is not running and you don't have a snapshot, the slider is enabled, and you can size the disk to your desired size.

I wanted to increase the size of the hard disk from 50 GB to 100 GB. That's a matter of seconds, and I was ready to go.

I've launched the VM image and checked the hard disk size. To my surprise, the size was still 50 GB and not the promised 100 GB.

## What happened

The request to change the hard disk size didn't make it to macOS. I started to examine the disk with `diskutil`.

{{< highlight bash session"linenos=inline,hl_lines=2 3" >}}
lab-vm: user$ diskutil list
/dev/disk0 (internal, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *107.4 GB   disk0
   1:                        EFI EFI                     209.7 MB   disk0s1
   2:                 Apple_APFS Container disk1          50.2 GB   disk0s2

/dev/disk1 (synthesized):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      APFS Container Scheme -                       +50.2 GB   disk1
                                 Physical Store disk0s2
   1:                APFS Volume macOS 10.13             23.2 GB    disk1s1
   2:                APFS Volume Preboot                 18.6 MB    disk1s2
   3:                APFS Volume Recovery                509.8 MB   disk1s3
   4:                APFS Volume VM                      20.5 KB    disk1s4
{{< /highlight >}}

Well, the size was changed successfully. That's good to see. But the reported size for the disk was still 50 GB.
I noticed the **Container disk1**. This one had the reported size of 50 GB. It looks like; this has to be changed to make use of all the available space of that hard disk.
After reading a little bit about APFS and how to deal with APFS, I learned that the hard disk is called a Volume. A Volume can have multiple containers.

I found this command to change the size of the container to grow and use all the available space of the Volume (I had sweaty palms)

{{< highlight bash session"linenos=inline,hl_lines=2 3" >}}
diskutil apfs resizeContainer /dev/disk1 0
{{< /highlight >}}

Break down of the command, and its arguments,

- diskutil apfs => tell diskutil that we are gonna modify something that has an APFS filesystem
- resizeContainer /dev/disk1 0 => resize container /dev/disk1 and grow to the maximum available space (0)

Not bad! That worked smoother than expected. Now I have the full 100 GB available and can continue filling it up. :-)

Thanks for reading. I hope it's helpful.

Feel free to share and leave a comment. I'm happy to learn about your experience.
