-- SQLite
SELECT cr.agent_no,
    a.agent_name,
    cr.periode,
    cr.type,
    cr.total_commission,
    sum(cri.commission) AS commission_sum
FROM commission_reports cr
    JOIN commission_report_items cri ON cri.commission_report_id = cr.id
    JOIN agents a ON a.agent_no = cr.agent_no
GROUP BY cr.agent_no,
    a.agent_name,
    cr.periode,
    cr.type,
    cr.total_commission