#!/bin/sh

hostname="`cat ../setting/hostname.txt`"
port="`cat ../setting/port_nuxt.txt`"

npx nuxt --hostname $hostname --port $port