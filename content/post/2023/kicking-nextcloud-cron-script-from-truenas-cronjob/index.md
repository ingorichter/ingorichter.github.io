+++
title = "Kicking Nextcloud Cron Script from TrueNAS Cron Job"
categories = ["TIL"]
tags = ["TIL", "TrueNAS", "Nextcloud", "Tips"]
date = 2023-02-01
draft = false
+++

# Kicking Nextcloud Cron Script from TrueNAS Cron Job

## Tl;DR

I'm running [TrueCharts Nextcloud](https://truecharts.org/charts/stable/nextcloud/) in my TrueNAS SCALE at home. After the setup, I discovered that none of the cron jobs was running. I'm using the Nextcloud News App and never saw any new stories. I didn't find a way to make the Nextcloud cron work, so I decided to have a cron job that runs every hour to kick the Nextclodu cron job in the Nextcloud docker container.

## Setup

After reading how to trigger the [Nextcloud Preview generator](https://www.truenas.com/community/threads/nextcloud-preview-generator.96870/) manually, I thought this approach would help me to solve my problem with the cron job and the missing News App updates.

After some experimenting, I came up with this docker command.

{{< highlight bash >}}
/usr/bin/docker exec -t --user 33 $(docker ps -qf "name=k8s_nextcloud_nextcloud") /usr/local/bin/php cron.php
{{< /highlight >}}

Once I verified that the script was working for me, I created a cron job in TrueNAS to execute this script every hour.

{{< img src="cronjob-truenas.png" title="TrueNAS Cron Job Configuration" alt="TrueNAS Cron Job Configuration" full="true">}}
