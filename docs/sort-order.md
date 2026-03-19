# How Chronological Sort Is Determined

The app stores three candidate dates for each file:

1. `filename_date`
2. `metadata_date`
3. `filesystem_date`

It then computes `derived_sort_date` using the configured priority order.

Default priority: `filename,metadata,filesystem`
