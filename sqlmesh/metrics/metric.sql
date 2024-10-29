METRIC (
    name total_items,
    expression COUNT(sqlmesh_example.full_model.item_id)
);

METRIC (
    name total_orders,
    expression COUNT(sqlmesh_example.incremental_model.id)
);

METRIC (
    name total_days_with_purchases,
    expression COUNT(distinct sqlmesh_example.incremental_model.event_date)
);
