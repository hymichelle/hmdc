# Example

Below are some examples of new and existing valid HMD syntax:

## Schema

There can be arbitrary number of categories. However, you can [declare a limit](https://github.com/initbar/hmdc/blob/388fb0b30b0b452351efcba762ba27b9aceead81/hmdc/__main__.py#L78-L85) and manually override the category counts:

```
(category)  ..  (category)	(definition)
```

## Comment

Comments are indicated by `#`.

```bash
# categories can be single.
A    (a)
B    (b)

## or multiple. ###
C    D  (e)

#
##
### comments also be nested.
##
#
```

## Variable

When declaring a variable, there should not be space between identifier and declaration.

```bash
$x=(a)
$y=(b)
$z=(c)
A B	(a)$x
C D	(a)$y
E F	(a)$z
G H	$x
I J	$y
K L	$z
M N	$x$x
O P	$x$y$z
```

## Spaces

Rules can be declared with arbitrary number of leading and trailing spaces/tabs:

```bash
A	A	(a)
 A	B	(a)
  A	C	(a)
   A	D	(a)
    A	E	(a)
     A	F	(a)
      A	G	(a)
```

## Sorting

If rules are not organized, you can set **hmdc** to sort the output result using [sort](https://github.com/initbar/hmdc/blob/388fb0b30b0b452351efcba762ba27b9aceead81/hmdc/__main__.py#L87-L91) flag:

```bash
# before
C (c)
B (b)
A (a)
A (b)

# after
A (a)
A (b)
B (b)
C (c)
```

## Unique

If you accidentally copy-and-paste identical rules, you can set **hmdc** to de-dup the results using [unique](https://github.com/initbar/hmdc/blob/388fb0b30b0b452351efcba762ba27b9aceead81/hmdc/__main__.py#L93-L97) flag:

```bash
# before
A (a)
B (b)
C (c)
A (a)
A (a)

# after
A (a)
B (b)
C (c)
```
