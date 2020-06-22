#!/bin/bash
tag=$(git for-each-ref --sort=-v:refname --count=1 --format '%(refname)'  refs/tags/${tag_prefix}[0-9]*.[0-9]*.[0-9]* refs/tags/${tag_prefix}v[0-9]*.[0-9]*.[0-9]* | cut -d / -f 3-)
if [[ ! -z $tag ]];
then
	docker build -t gcr.io/tranquility-base-images/tb-houston-service:$tag .
	docker push gcr.io/tranquility-base-images/tb-houston-service:$tag
else
	echo "Unable to find latest tag!"
	exit 1
fi
