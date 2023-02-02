+++
title = "Kicking Nextcloud Cron Script from TrueNAS Cronjob"
categories = ["TIL"]
tags = ["TIL"]
date = 2023-02-01
draft = true
+++

# Kicking Nextcloud Cron Script from TrueNAS Cronjob

## Tl;DR

I'm running [TrueCharts Nextcloud](https://truecharts.org/charts/stable/nextcloud/) in my TrueNAS SCALE at home. After the setup, I discovered that none of the cronjobs was running. I'm using the Nextcloud News App and never saw any new stories. I didn't find a way to make the Nextcloud cron work, so I decided to have a cronjob that runs every hour to kick the Nextclodu cronjob in the Nextcloud docker container.

## Setup

After reading how to trigger the [Nextcloud Preview generator](https://www.truenas.com/community/threads/nextcloud-preview-generator.96870/) manually, I thought this approach would help me to solve my problem with the cronjob and the missing News App updates.

After some experimenting, I came up with this docker command.

{{< highlight bash >}}
/usr/bin/docker exec -t --user 33 $(docker ps -qf "name=k8s_nextcloud_nextcloud") /usr/local/bin/php cron.php
{{< /highlight >}}

Once I verified that the script was working for me, I created a cronjob in TrueNAS to execute this script every hour.

{{< img src="cronjob-truenas.png" title="TrueNAS Cronjob Configuration" alt="TrueNAS Cronjob Configuration" full="true">}}
