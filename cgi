#!/bin/sh

ifs_=$IFS

. ./lib/libcgi
. ./lib/libsym

getcmdargs_() { shift 1; echo $@; }

## main()

if [ $# -ne 1 ]; then
	exit 1
fi

trace_ "uuid: $1"

echo OK # handshake response
read data # receive payload

trace_ "data: $data"

mkdir -p files
if [ $? -ne 0 ]; then
	trace_ "files: failed to create directory"
	exit 1
fi

if [ "$data" = "/" ]; then
	. $cgi_/home > files/index.html
	echo "files/index.html"
	exit 0
fi

tmp_=$base_/tmp/$1
temp_=/tmp/$1 # this one is for href
mkdir -p $tmp_
if [ $? -ne 0 ]; then
	trace_ "$tmp_: failed to create directory"
	exit 1
fi

getval_ '?' $data
split_ '&' $val_; args_=$str_

case "$data" in
/cgi?home)
	. $cgi_/home > files/index.html
	echo "files/index.html"
	;;
/cgi?apps)
	. $cgi_/apps > $tmp_/apps.html
	echo "$tmp_/apps.html"
	;;
/cgi?wincfg)
	. $cgi_/wincfg > $tmp_/wins.html
	echo "$tmp_/wins.html"
	;;
/cgi?show=*)
	getopt_ "show" $args_

	if [ -n "$val_" ]; then
		xdotool windowraise $val_
		xdotool windowfocus $val_
	fi
	. $cgi_/wincfg > $tmp_/wins.html
	echo "$tmp_/wins.html"
	;;
/cgi?close=*)
	getopt_ "close" $args_

	if [ -n "$val_" ]; then
		xdotool windowkill $val_
	fi
	. $cgi_/wincfg > $tmp_/wins.html
	echo "$tmp_/wins.html"
	;;
/cgi?pidinfo=*)
	getopt_ "pidinfo" $args_
	top -H -b -n 1 -p $val_ > $tmp_/pid.txt
	echo >> $tmp_/pid.txt
	ls -l /proc/$val_/fd >> $tmp_/pid.txt 2>&1
	echo "$tmp_/pid.txt"
	;;
/cgi?wininfo=*)
	getopt_ "wininfo" $args_
	xprop -id $val_ > $tmp_/win.txt
	echo "$tmp_/win.txt"
	;;
/cgi?scrcfg)
	. $cgi_/scrcfg > $tmp_/scrcfg.html
	echo "$tmp_/scrcfg.html"
	;;
/cgi?tagcfg)
	. $cgi_/tagcfg > $tmp_/tagcfg.html
	echo "$tmp_/tagcfg.html"
	;;
/cgi?netstat)
	. $cgi_/netstat > $tmp_/netstat.html
	echo "$tmp_/netstat.html"
	;;
/cgi?route)
	. $cgi_/route > $tmp_/route.html
	echo "$tmp_/route.html"
	;;
/cgi?netcfg)
	. $cgi_/netcfg > $tmp_/netcfg.html
	echo "$tmp_/netcfg.html"
	;;
/cgi?cmd=ifcfg*)
	. $cgi_/ifcfg > $tmp_/ifcfg.html
	echo $tmp_/ifcfg.html
	;;
/cgi?cmd=ifup*)
	getopt_ "dev" $args_
	trace_ "UP: $val_"
	sudo ifdown $val_ 1>&2
	sudo ifup $val_ 1>&2
	. $cgi_/netcfg > $tmp_/netcfg.html
	echo $tmp_/netcfg.html
	;;
/cgi?cmd=ifdown*)
	getopt_ "dev" $args_
	trace_ "DOWN: $val_"
	sudo ifdown $val_ 1>&2
	. $cgi_/netcfg > $tmp_/netcfg.html
	echo $tmp_/netcfg.html
	;;
/cgi?cmd=ifsave*)
	. $cgi_/ifsave 1>&2
	. $cgi_/netcfg > $tmp_/netcfg.html
	echo $tmp_/netcfg.html
	;;
'post.wpa'*=*)
	split_ '&' $data; args_=$str_
	. $cgi_/wpacli > $tmp_/wpacli.html
	args_=''
	. $cgi_/netcfg > $tmp_/netcfg.html
	echo $tmp_/netcfg.html
	;;
'post.run.'*=*)
#	data=$(getval_ '.' $data) # strip post
#	data=$(getval_ '.' $data) # strip run
#	cmd=$(getvar_ '=' $data)
#	arg=$(getval_ '=' $data)
#	trace_ "exec: $arg $cmd"
	# FIXME: command should be in white-list
	if [ -n "$arg" -a "$arg" == "term" ]; then
		exec xterm -e "$cmd" >/dev/null &
	else
		exec $cmd >/dev/null &
	fi
	sleep 1
	. $cgi_/wincfg > $tmp_/wins.html
	echo "$tmp_/wins.html"
	;;
/cgi?cmd=tagcfg*)
	args=$(IFS='?'; getcmdargs_ $data)
	trace_ "tagcfg cmd args: $args"
	. ./lib/libyawm
	IFS='&'; modtags_ $args; IFS=$ifs_
	. $cgi_/tagcfg > $tmp_/tagcfg.html
	echo "$tmp_/tagcfg.html"
	;;
*) trace_ "bad request '$data'"; exit 1;;
esac
