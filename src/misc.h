/* misc.h: miscellaneous utils
 *
 * Copyright (c) 2015, Aliaksei Katovich <aliaksei.katovich at gmail.com>
 *
 * Released under the GNU General Public License, version 2
 */

#ifndef MISC_H
#define MISC_H

#include <errno.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#ifndef ARRAY_SIZE
#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))
#endif

#define eval(cond, act) { if (cond) { ee("assert "#cond"\n"); act; } }

#define ee(fmt, ...) {\
	int errno_save__ = errno;\
	fprintf(stderr, "(ee) %s: " fmt, __func__, ##__VA_ARGS__);\
	if (errno_save__ != 0)\
		fprintf(stderr, "(ee) %s: %s, errno=%d\n", __func__,\
		     strerror(errno_save__), errno_save__);\
	errno = errno_save__;\
	fprintf(stderr, "(ee) %s: %s at %d\n", __func__, __FILE__, __LINE__);\
}

#ifdef DEBUG
#define dd(fmt, ...) printf("(dd) %s: " fmt, __func__, ##__VA_ARGS__)
#else
#define dd(fmt, ...) do {} while(0)
#endif

#ifdef VERBOSE
#define mm(fmt, ...) printf("(==) " fmt, ##__VA_ARGS__)
#else
#define mm(fmt, ...) do {} while(0)
#endif

#define ww(fmt, ...) printf("(ww) " fmt, ##__VA_ARGS__)
#define ii(fmt, ...) printf("(ii) " fmt, ##__VA_ARGS__)

#ifdef TRACE
#define tt(fmt, ...) printf("(tt) %s: " fmt, __func__, ##__VA_ARGS__)
#else
#define tt(fmt, ...) do {} while(0)
#endif

int16_t pollfd(int fd, int16_t events, int timeout);
size_t pull(int fd, void *data, size_t size, int timeout);
size_t push(int fd, const void *data, size_t size);
size_t pushv(int fd, const struct iovec *iov, int8_t iovcnt);
size_t pullv(int fd, const struct iovec *iov, int8_t iovcnt, int timeout);

struct request {
	char *str;
	int16_t len;
	int16_t flag; /* mark incomplete string */
};

size_t pullstr(int fd, char *buf, int16_t len, struct request *req,
	       int8_t reqcnt);

#endif /* MISC_H */
