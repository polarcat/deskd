cc = $(CROSS_COMPILE)gcc
cflags = -Wall -Wunused-function

deskdout = deskd
getipout = getip

.PHONY: all clean distclean
all: $(deskdout) $(getipout)

deskdsrc = src/deskd.c src/misc.c
deskdcflags = $(cflags) $(CFLAGS) -DHAVE_SENDFILE

$(deskdout):
	$(cc) -o sbin/$(deskdout) $(deskdsrc) $(deskdcflags)
	@printf "(==) \033[0;32m$(deskdout)\033[0m done\n"

clean-$(deskdout):
	-rm -f $(deskdout)

getipsrc = src/getip.c
getipcflags = $(cflags) $(CFLAGS)

$(getipout):
	$(cc) -o sbin/$(getipout) $(getipsrc) $(getipcflags)
	@printf "(==) \033[0;32m$(getipout)\033[0m done\n"

clean-$(getipout):
	-rm -f utils/$(getipout)

install:
	-mkdir -p $(HOME)/.deskd
	-unlink $(HOME)/.deskd/sbin/$(deskdout)
	-cp -fa cgi $(HOME)/.deskd/
	-cp -fra etc $(HOME)/.deskd/
	-cp -fra lib $(HOME)/.deskd/
	-cp -fra sbin $(HOME)/.deskd/
	-cp -fra styles $(HOME)/.deskd/

clean:
	-rm -f sbin/$(deskdout)
	-rm -f sbin/$(getipout)

distclean: clean
