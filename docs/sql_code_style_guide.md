# SQL code style guide

- [Definitions](#definitions)
- [Modifications](#modifications)
- [General guidelines](#general-guidelines)
- [Table/Column Naming Conventions](#tablecolumn-naming-conventions)
- [SELECT statement](#select-statement)
- [FROM statement](#from-statement)
- [JOIN statements](#join-statements)
- [WHERE statement](#where-statement)
- [GROUP BY statement](#group-by-statement)
- [WINDOW statements](#window-statements)
- [HAVING and QUALIFY statements](#having-and-qualify-statements)
- [ARRAY_AGG + STRUCT statements](#array_agg--struct)
- [WITH statements and sub-queries](#with-statements-and-sub-queries)
- [CASE statements](#case-statements)
- [UNION statements](#union-statements)
- [CREATE statements](#create-statements)

This guide defines the BigQuery coding standards to be used when contributing SQL code. The intent of this guide is to
help contributors create BigQuery queries that are readable, portable, easy to maintain, and bug-free.

## Definitions

The key words **MUST**, **MUST NOT**, **MAY**, **SHOULD**, **SHOULD NOT**, and **OPTIONAL** in this document are to be
interpreted as follows:

- **MUST** and **MUST NOT**: these words mean that the definition is an absolute requirement of the specification.
  Deviations from these rules are considered sufficient grounds for rejecting a contribution.
- **MAY**: this word means that the specification is allowed, though not encouraged.
- **SHOULD** and **SHOULD NOT**: these words mean that there may exist valid reasons in particular circumstances to
  ignore a particular item, but the full implications must be understood and carefully weighed before choosing a
  different course. Deviations from these rules could be accepted, but additional clarification/justification will have
  to be provided by the contributor.
- **OPTIONAL**: this word means that the contributor may initially choose to ignore the specification. Nevertheless, all
  contributors are encouraged to follow them and Code owners may still request additional clarifications as to why the
  contributor is choosing to ignore it.

## Modifications

This document is subject to periodic revisions and adjustments.

## General guidelines

### G1

All BigQuery SQL files **MUST** have the `.sql` extension.

### G2

File names **MUST** only contain lowercase letters (a-z) and underscore `_`. This is known as `snake_case`.

### G3

A file **MUST** end with a new line, and only one.

### G4

All BigQuery SQL reserved words **MUST** be written in upper case.

### G5

Lines **MUST NOT** exceed 120 characters in length, including white-spaces.

### G6

If a line is broken into two, the subsequent **MUST** be indented with 2 white spaces. For example, the following
condition:

```sql
-- Bad
AND (GREATEST(COALESCE(TIMESTAMP_DIFF(rider_picked_up_at, rider_near_restaurant_at, SECOND), 0), 0)
+ COALESCE(TIMESTAMP_DIFF(rider_near_restaurant_at, o.original_scheduled_pickup_at, SECOND), 0)) < 0
```

is broken into:

```sql
-- Good
AND (
  GREATEST(COALESCE(TIMESTAMP_DIFF(rider_picked_up_at, rider_near_restaurant_at, SECOND), 0), 0)
    + COALESCE(TIMESTAMP_DIFF(rider_near_restaurant_at, o.original_scheduled_pickup_at, SECOND), 0)
) < 0
```

### G7

If the query is short (less than 120 characters), it **MAY** be written as a single line.

```sql
SELECT * FROM vendors WHERE created_date = '2021-12-10'
```

otherwise

- each statement **MUST** be written in a separate line.
- each statement **MUST** have the same indentation level.

```sql
SELECT
  global_entity_id
  , country_code
  , vendor_id
FROM vendors
WHERE TRUE
  AND created_date = '2019-09-09'
  AND is_online
GROUP BY 1, 2
ORDER BY 1 DESC
```

## Table/Column naming conventions

### TC1

All tables intended for internal/intermediate usage should start with an underscore (`_`).

### TC2

All tables intended for shared layer should have meaningful naming and not start with an underscore (`_`), tmp, dim,
fct, etc.

### TC3

All column names should be either self-explanatory with respect to table or parent columns (in case of complex data
types) or have proper descriptions available.

### TC4

Table names should be as self-explanatory as possible.

### TC5

Table names should be plural. For example, use `orders` not `order`, `warehouses` nor `warehouse`.

### CC1 - Names

- All column names **MUST** be written in `snake_case`.
- All column names should be as self-explanatory as possible.

### CC2 - Dates and timestamps

- Date columns **MUST** end with the suffix `_date`.
- Timestamp columns **MUST** end with the suffix `_at`.

### CC3 - Booleans

- Boolean columns **MUST** have an appropriate prefix: `is_`, `has_`. Examples: `is_online` or `has_orders`.

### CC4 - Nested fields

- All nested fields should be suffixed with `info` OR `_details` OR should indicate the aggregation it holds.

## SELECT statement

### S1

All attributes of a `SELECT` statement **MUST** be in its own line.

### S2

The use of `SELECT *` **MUST** be avoided.

### S3

All attributes of a `SELECT` statement **MUST** have a leading comma (except for the first one).

### S4

Each leading comma **MUST** be indented by two spaces with respect to the `SELECT` statement.

```sql
SELECT
  country_code
  , zone_id
  , id
```

### S5

A white-space, and only one, **MUST** always follow the leading comma.

## FROM statement

### F1

The table/view in the `FROM` statement **MUST** appear in the same line as the `FROM` keyword itself.

### F2

Proper parametrization of Project IDs and Datasets **MUST** be used in all `FROM` statements.

## JOIN statements

### J1

All `JOIN` statements **MUST** indicate the type of join being used:

- `INNER JOIN`
- `LEFT JOIN`
- `RIGHT JOIN`
- `FULL JOIN`
- `CROSS JOIN`

### J2

Each `JOIN` statement **MUST** be written on a new line at the same level of indentation as its `SELECT` statement.

### J3

All tables involved in a `JOIN` operation **SHOULD** have an alias.

### J4

The keyword `AS` **MUST** precede all aliases.

### J5

In query statements that involve only two tables (one `FROM` and one `JOIN`), the `USING` clause **MAY** be used.

### J6

In query statements that involve more than two tables (multiple `JOIN` statements), the `USING` clause **MUST NOT** be
used.

### J7

Each joining condition **MUST** be written in a new line with 2 spaces of indentation with respect to its `JOIN`
keyword.

```sql
FROM orders AS o
LEFT JOIN vendors AS v
  ON o.global_entity_id = v.global_entity_id
  AND o.vendor_id = v.vendor_id
```

## WHERE statement

### W1

The first condition of the `WHERE` statement **SHOULD** be `TRUE`.

**Rationale:**

- Better readability as each condition appears in its own line.
- As code evolves, GitHub diffs will highlight only the modified condition, and not the `WHERE` itself.
- This makes debugging filtering conditions easier as they can be commented-out one at a time without having to modify
  the `WHERE` keyword itself.

### W2

Each condition **MUST** be written on a new line with two spaces of indentation with respect to the `WHERE` clause.

### W3

The condition **MAY** be included in the same line as the `WHERE` keyword when only one condition is needed.

## GROUP BY statement

### GB1

Numbers **MUST** be used to specify `GROUP BY` statement columns. This allows us to keep it in a single line.

```sql
SELECT
  country_code
  , zone_id
FROM events
GROUP BY 1, 2
```

### GB2

In cases where BigQuery does not allow the use of numbers, column names **SHOULD** be used, following the same rules as
with `SELECT` statements.

```sql
SELECT
  country_code
  , zone_id
FROM events
GROUP BY
  country_code
  , zone_id
```

## WINDOW statements

### WI1

All window declarations **MUST** be made using the `WINDOW` clause.

### WI2

When defining new windows, the `WINDOW` keyword **MUST** be in its own line.

### WI3

The name of the window **MUST** be in the same line as the `WINDOW` keyword.

### WI4

The `AS` keyword following the name of the window **MUST** be in the same line as the window's name.

### WI5

The opening (`(`) parenthesis **MUST** be in the same line as the name of the window. When only one window is been
defined, the closing (`)`) parenthesis **MUST** be in its own line with the same level of indentation as the `WINDOW`
keyword.

When defining more than one windows, the subsequent windows **MUST** start in the same line as the one closing the
first window. For example,

```sql
WINDOW first_window AS (
  PARTITION BY ...
  ORDER BY ...
), second_window AS (
  PARTITION BY ...
  ORDER BY ...
), third_window AS (
  PARTITION BY ...
  ORDER BY ...
)
```

### WI6

The target elements of the different keywords in the window definition (`PARTITION BY`, `ORDER BY`, etc) **MUST** be in
the same line as the keyword, unless the 120 characters line-limit is reached. If this occurs, targets **MUST** follow
the same rules as with `SELECT` targets. For example:

```sql
-- Good
WINDOW some_window AS (
  PARTITION BY t.column1, t.column2
  ORDER BY t.column3
)

-- Good
WINDOW some_window AS (
  PARTITION BY
    t.column1
    , t.column2
    , t.column3
    , t.column4
    , t.column5
  ORDER BY
    t.column6
)

-- Bad
WINDOW some_window AS (
  PARTITION BY t.column1
    , t.column2
    , t.column3
  ORDER BY t.column4
)
```

## HAVING and QUALIFY statements

### HQ1

`HAVING` and `QUALIFY` **MAY** be written in a single line

**Rationale:**

Even though these clauses could follow the same rules as the `WHERE` clause, there's usually only one condition used in
these statements.

### HQ2

If more than one `HAVING` or `QUALIFY`ing conditions need to be used:

- The line containing the `HAVING` or `QUALIFY` keyword **SHOULD** use be followed by `TRUE` (see `WHERE` clause for
  rationale).
- Each subsequent condition should be written in its own line, preceded by the keyword `AND`.

## ARRAY_AGG + STRUCT

When aggregating into an array of `STRUCT`s, the following guidelines should be followed.

``` sql
SELECT
  a.country_code
  , ARRAY_AGG(
      STRUCT(
        a.id
        , a.start_at
        , a.end_at
      )
    ) AS absences_history
FROM temp.foo AS a
```

### AGS1

The opening parenthesis of the `ARRAY_AGG` **MUST** be on the same line as the `ARRAY_AGG` keyword.

### AGS2

The `STRUCT` **MUST** be in a new line with two spaces of indent in respect to `ARRAY_AGG`.

### AGS3

The opening parenthesis of the `STRUCT` **MUST** be on the same line as the `STRUCT` keyword.

### AGS4

The first element of the `STRUCT` **MUST** be in a new line indented by 2 spaces with respect to the `STRUCT`
keyword.

### AGS5

All columns in the `STRUCT` **MUST** have leading commas.

### AGS6

The closing parenthesis of `STRUCT` **MUST** be in the same level as the `STRUCT` keyword.

### AGS7

The closing parenthesis of `ARRAY_AGG` **MUST** be in the same level and the `ARRAY_AGG` keyword.

### AGS8

The aggregation `ARRAY_AGG` **SHOULD** be given an alias.

## WITH statements and sub-queries

```sql
WITH foo AS (

  SELECT
    country_code
  FROM foo
  WHERE action = 'close'

), bar AS (

  SELECT
    country_code
  FROM bar
  WHERE action = 'close'

)
SELECT
  f.country_code
FROM foo AS f
LEFT JOIN bar AS b
  ON f.country_code = b.country_code
```

### WSQ1

The use of sub-queries **MUST** be avoided, with the only exception of scalar sub-queries.

### WSQ2

The table expression name **MUST** be in the same line as the `WITH` keyword.

### WSQ3

The `AS` keyword **MUST** be in the same line as the `WITH` keyword.

### WSQ4

The opening parenthesis of the table expression **MUST** be in the same line as the `WITH` keyword.

### WSQ5

You **MUST** use a line break at the start and the end of the table expression.

### WSQ6

All statements of the table expression **MUST** be indented by two space in respect to the `WITH` statement.

### WSQ7

The closing parenthesis **MUST** be at the same indentation level as the `WITH` keyword.

### WSQ8

In any subsequent table expression name, the `AS` keyword and opening parenthesis **MUST** be in the same line as the
previous closing parenthesis.

### WSQ9

The query expression indent level **MUST** match the `WITH` keyword.

## CASE statements

### CA1

If the `CASE` statement is short (less than 120 characters), it **MAY** be written in a single line.

```sql
CASE WHEN action = 'lock-down' THEN 'close' ELSE action END AS event_type
```

### CA2

If the `CASE` has only one condition, it **MAY** be written as an `IF` statement.

```sql
IF(action = 'lock-down', 'close', action) AS event_type
```

### CA3

When the conditional has more than one condition, the following guidelines **MUST** be followed.

- The `WHEN` keyword **MUST** be written in a new line indented by two spaces in respect to the `CASE` keyword.
- All conditions **MUST** be written in the same line as the `WHEN` keyword, as long as they don't exceed the 120
  characters per line limit.
- The `THEN` keyword **MAY** be written on the same line as the `WHEN` keyword, if the number of characters does not
  exceed 120. Otherwise, it **MUST** be written on a new line.
- All new `WHEN` statements **MUST** have the same indentation of the first `WHEN` statement.
- The `ELSE` keyword **MUST** be at the same indentation level of the `WHEN` statements.
- The `END` keyword **MUST** be at the same indentation level of `CASE`.

Example:

``` sql
CASE
  WHEN action = 'lock-down' THEN 'close'
  WHEN action = 'shrink' THEN 'close'
  ELSE action
END AS event_type
```

### CA4

The `WHEN` conditions **SHOULD NOT** exceed the 120 characters, instead consider using `WITH`.

In the example below, notice how `TIMESTAMP_DIFF(rider_near_restaurant_at, o.original_scheduled_pickup_at, SECOND)` is
repeated several times. This is an anti pattern for performance, as this operation **SHOULD** be done only once in a
table expression.

```sql
CASE
  WHEN (
    atr.pickup IS NULL
    AND atr.drop_off IS NULL
    AND TIMESTAMP_DIFF(rider_near_restaurant_at, o.original_scheduled_pickup_at, SECOND) <= 0
  )
    THEN TIMESTAMP_DIFF(rider_dropped_off_at, rider_picked_up_at, SECOND)
  WHEN (
    atr.pickup IS NULL
    AND atr.drop_off IS NULL
    AND TIMESTAMP_DIFF(rider_near_restaurant_at, o.original_scheduled_pickup_at, SECOND) > 0
    AND TIMESTAMP_DIFF(rider_picked_up_at, rider_near_restaurant_at, SECOND) < 300
  )
    THEN TIMESTAMP_DIFF(rider_dropped_off_at, o.updated_scheduled_pickup_at, SECOND)
  WHEN (
    atr.pickup IS NULL
    AND atr.drop_off IS NULL
    AND TIMESTAMP_DIFF(rider_near_restaurant_at, o.original_scheduled_pickup_at, SECOND) > 0
    AND TIMESTAMP_DIFF(rider_picked_up_at, rider_near_restaurant_at, SECOND) >= 300
  )
    THEN TIMESTAMP_DIFF(rider_dropped_off_at, rider_picked_up_at, SECOND)
  ELSE NULL
END AS foo
```

## UNION statements

### U1

`SELECT` statements for the final `UNION` operation **MUST** select required columns and not use `SELECT *`.

```sql
SELECT
  columns
FROM table

UNION [ALL|DISTINCT]

SELECT
  columns
FROM table
```

## CREATE statements

### C1

The `CREATE`, `PARTITION BY`, `CLUSTER BY`, and `AS` statements **MUST** be written into new lines without indentation.

```sql
CREATE OR REPLACE TABLE `temp.foo`
PARTITION BY created_date
CLUSTER BY country_code, zone_id, id
AS
```

### C2

The `CLUSTER BY` statement **MUST NOT** have more than 4 columns. For further information, read [here][1].

[1]: https://cloud.google.com/bigquery/docs/creating-clustered-tables#limitations
