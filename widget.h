#ifndef _WIDGET_H_
#define _WIDGET_H_

struct _widget_vtable;
typedef struct _widget {
	struct _widget_vtable* vtable;
	uint16_t x;
	uint16_t y;
	uint16_t w;
	uint16_t h;
} widget_t;

typedef struct _widget_vtable {
	void (*destroy)(struct _widget*);
} widget_vtable_t;

#endif // _WIDGET_H_
