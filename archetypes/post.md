{{- $now := now -}}
+++
categories = ["TIL"]
date = "{{ .Date }}"
description = ""
draft = true
id = "{{ print .File.Path $now.UnixNano | sha1 }}"
link = ""
tags = ["TIL"]
title = "{{ replace (strings.TrimPrefix (print ($now.Format `2006-01-02`) `-`) .Name) `-` ` ` | title }}"
+++

<!--more-->

## {{ .Name }}
