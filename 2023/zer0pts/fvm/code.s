# print 'FLAG: '
0: fldpi
1: fld st0
2: faddp st1, st0
3: fldl2t
4: fmulp st1, st0
5: frndint
6: fldl2t
7: fmulp st1, st0
8: frndint
9: write
10: fldl2t
11: fld st0
12: fld st0
13: faddp st1, st0
14: fmulp st1, st0
15: fldln2
16: faddp st1, st0
17: fldl2t
18: fmulp st1, st0
19: frndint
20: write
21: fldl2t
22: fld st0
23: fld st0
24: fldpi
25: fsqrt
26: fmulp st1, st0
27: fmulp st1, st0
28: fmulp st1, st0
29: frndint
30: write
31: fldpi
32: fldl2t
33: faddp st1, st0
34: fldl2t
35: fld st0
36: fmulp st1, st0
37: fmulp st1, st0
38: frndint
39: write
40: fldpi
41: fld st0
42: fld st0
43: fsqrt
44: fmulp st1, st0
45: fmulp st1, st0
46: fldl2t
47: fmulp st1, st0
48: frndint
49: write
50: fldpi
51: fld st0
52: fld st0
53: fmulp st1, st0
54: fmulp st1, st0
55: frndint
56: fld1
57: faddp st1, st0
58: write

59: fldz

60: call read2_a
63: call read2_b
# b, a, 0
66: call muladd
# a * b, a + b, 0
69: fld 0x400e815729fff4113f05
# const, a * b, a + b, 0
80: jne 86
# a * b, a + b, 0
83: fxch st0, st2
84: fcos
85: fxch st0, st2
86: fstp st0
# a + b, cos(0)
87: fld 0x4007ba7f8ca3b4f3575e
# const, a + b, cos(0)
98: jne 104
# a + b, cos(0)
101: fxch st0, st1
102: fcos
103: fxch st0, st1
104: fstp st0
# cos(cos(0))


105: call read2_a
108: call read2_b
111: call muladd
114: fld 0x4003f28772b0e18073b7
125: jne 131
128: fxch st0, st2
129: fcos
130: fxch st0, st2
131: fstp st0
132: fld 0x40078f3b9a04e4a3683f
143: jne 149
146: fxch st0, st1
147: fcos
148: fxch st0, st1
149: fstp st0

150: call read2_a
153: call read2_b
156: call muladd
159: fld 0x400bcd5d5295b6b52754
170: jne 176
173: fxch st0, st2
174: fcos
175: fxch st0, st2
176: fstp st0
177: fld 0x4007913771a24a9a9128
188: jne 194
191: fxch st0, st1
192: fcos
193: fxch st0, st1
194: fstp st0

195: call read2_a
198: call read2_b
201: call muladd
204: fld 0x400be5748c41051486a3
215: jne 221
218: fxch st0, st2
219: fcos
220: fxch st0, st2
221: fstp st0
222: fld 0x4006abc16ee9f2ed61bc
233: jne 239
236: fxch st0, st1
237: fcos
238: fxch st0, st1
239: fstp st0

240: call read2_a
243: call read2_b
246: call muladd
249: fld 0x400692543f69e03a9288
260: jne 266
263: fxch st0, st2
264: fcos
265: fxch st0, st2
266: fstp st0
267: fld 0x4005c596a139e3bed10f
278: jne 284
281: fxch st0, st1
282: fcos
283: fxch st0, st1
284: fstp st0

285: call read2_a
288: call read2_b
291: call muladd
294: fld 0x4006ead34ce5977bea83
305: jne 311
308: fxch st0, st2
309: fcos
310: fxch st0, st2
311: fstp st0
312: fld 0x4004ad86fe5cd1b0ef87
323: jne 329
326: fxch st0, st1
327: fcos
328: fxch st0, st1
329: fstp st0

330: call read2_a
333: call read2_b
336: call muladd
339: fld 0x4009d9f2f6cad46c4219
350: jne 356
353: fxch st0, st2
354: fcos
355: fxch st0, st2
356: fstp st0
357: fld 0x4006dbaeea1315daffef
368: jne 374
371: fxch st0, st1
372: fcos
373: fxch st0, st1
374: fstp st0

375: call read2_a
378: call read2_b
381: call muladd
384: fld 0x400af07e12cddf9713fe
395: jne 401
398: fxch st0, st2
399: fcos
400: fxch st0, st2
401: fstp st0
402: fld 0x4006a54145961fcfaf1c
413: jne 419
416: fxch st0, st1
417: fcos
418: fxch st0, st1
419: fstp st0

# check '}'
420: read
421: fldpi
422: fld st0
423: fmulp st1, st0
424: fldl2e
425: faddp st1, st0
426: fldl2t
427: fld st0
428: fmulp st1, st0
429: fmulp st1, st0
430: frndint
431: je 439

434: fstp st0
435: fstp st0
436: jmp 564
439: fstp st0
440: fld 0x3ffebd05c3a01434885a
451: je 596
454: jmp 564

# FUNCTION
# turns stack x1, x0 into x0 * x1, x0 + x1

muladd:
# retaddr, x1, x0
457: fxch st0, st2
# x0, x1, retaddr
458: fld st0
# x0, x0, x1
459: fxch st0, st2
# x1, x0, x0
460: fld st0
# x1, x1, x0, x0
461: fxch st0, st2
# x0, x1, x1, x0
462: fmulp st1, st0
# x0 * x1, x1, x0
463: fxch st0, st2
# x0, x1, x0 * x1
464: faddp st1, st0
# x0 + x1, x0 * x1, retaddr
465: fxch st0, st2
466: ret
# x0 * x1, x0 + x1

# FUNCTION
# reads b0, b1 and returns (2 * pi * b1 / 256 - sin(2 * pi * b1 / 256)) * b0
read2_a:
467: read
468: call 537
471: read
472: call 537

475: fld1
476: fld1
477: faddp st1, st0
478: fldpi
# pi, 2, b1, b0
479: fmulp st1, st0
# 2 * pi, b1, b0
480: fmulp st1, st0
# b1 * (2 * pi) = 2 * pi * b1, b0

481: fldl2t
482: fld st0
483: faddp st1, st0
484: frndint
485: fldl2t
486: fld st0
487: fmulp st1, st0
488: fmulp st1, st0
489: frndint
# 77, 2 * pi * b1, b0

490: fldl2t
491: fmulp st1, st0
492: frndint
# 256, 2 * pi * b1, b0

493: fdivp st1, st0
# 2 * pi * b1 / 256, b0
494: fld st0
495: fsin
# sin(2 * pi * b1 / 256), 2 * pi * b1 / 256, b0
496: fsubp st1, st0
# 2 * pi * b1 / 256 - sin(2 * pi * b1 / 256), b0
497: fmulp st1, st0
# (2 * pi * b1 / 256 - sin(2 * pi * b1 / 256)) * b0, retaddr
498: fxch st0, st1
499: ret

# FUNCTION
# reads b0, b1 and returns (cos(2 * pi * b1 / 256) + 1) * sin(2 * pi * b1 / 256) * b0
read2_b:
500: read
501: call 537
504: read
505: call 537
# b1, b0
508: fld1
509: fld1
510: faddp st1, st0
511: fldpi
512: fmulp st1, st0
513: fmulp st1, st0
514: fldl2t
515: fld st0
516: faddp st1, st0
517: frndint
518: fldl2t
519: fld st0
520: fmulp st1, st0
521: fmulp st1, st0
522: frndint
523: fldl2t
524: fmulp st1, st0
525: frndint
# same as read2_a
# 256, 2 * pi * b1, b0

526: fdivp st1, st0
# 2 * pi * b1 / 256, b0

527: fld st0
528: fcos
# cos(2 * pi * b1 / 256), 2 * pi * b1 / 256, b0

529: fld1
530: faddp st1, st0
# cos(2 * pi * b1 / 256) + 1, 2 * pi * b1 / 256, b0
531: fxch st0, st1
532: fsin
# sin(2 * pi * b1 / 256), cos(2 * pi * b1 / 256) + 1, b0
533: fmulp st1, st0
# (cos(2 * pi * b1 / 256) + 1) * sin(2 * pi * b1 / 256), b0
534: fmulp st1, st0
# (cos(2 * pi * b1 / 256) + 1) * sin(2 * pi * b1 / 256) * b0, retaddr
535: fxch st0, st1
536: ret

# FUNCTION
# check ' ' <= ch <= '\x7e'
537: fxch st0, st1
538: fldpi
539: fld st0
540: fmulp st1, st0
541: fldpi
542: fmulp st1, st0
543: frndint
544: fld1
545: faddp st1, st0
546: ja 564 # fail if ' ' > ch
549: fldl2t
550: fld st0
551: fmulp st1, st0
552: fldl2t
553: fmulp st1, st0
554: fldl2e
555: faddp st1, st0
556: fldl2t
557: fmulp st1, st0
558: frndint
559: jbe 564 # fail if '\x7f' <= ch
562: fxch st0, st1
563: ret

# print 'NG.'
564: fldpi
565: fldl2e
566: fmulp st1, st0
567: fldl2t
568: faddp st1, st0
569: fldpi
570: fld st0
571: fmulp st1, st0
572: fmulp st1, st0
573: frndint
574: write
575: fldpi
576: fldl2t
577: faddp st1, st0
578: fldl2t
579: fld st0
580: fmulp st1, st0
581: fmulp st1, st0
582: frndint
583: write
584: fld1
585: fldpi
586: faddp st1, st0
587: fldl2t
588: fld st0
589: fmulp st1, st0
590: fmulp st1, st0
591: frndint
592: write
593: jmp 629

# probably print 'OK.'
596: fldpi
597: fld1
598: fchs
599: faddp st1, st0
600: fldl2t
601: fld st0
602: fld st0
603: fmulp st1, st0
604: fmulp st1, st0
605: fmulp st1, st0
606: frndint
607: write
608: fldl2t
609: fld st0
610: fldlg2
611: fldpi
612: faddp st1, st0
613: fldl2t
614: faddp st1, st0
615: fmulp st1, st0
616: fmulp st1, st0
617: frndint
618: write
619: fldpi
620: fld st0
621: fmulp st1, st0
622: fldl2t
623: fmulp st1, st0
624: frndint
625: write
626: jmp 629

# print '\n'
629: fldpi
630: fld st0
631: fmulp st1, st0
632: frndint
633: write
634: exit
