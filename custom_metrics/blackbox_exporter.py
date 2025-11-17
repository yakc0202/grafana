# Sample config for Grafana Agent
# For a full configuration reference, see: https://grafana.com/docs/agent/latest/configuration/.
server:
  log_level: info
metrics:
  global:
    scrape_interval: 1m
    remote_write:
    - url: "https://aps-workspaces.ap-south-1.amazonaws.com/workspaces/ws-0246d7a9-77a1-4109-bf19-c322ae84c98b/api/v1/remote_write"
      sigv4:
        region: ap-south-1
        role_arn: arn:aws:iam::560412178918:role/grafana-agent_to_amp
  wal_directory: /var/lib/grafana-agent
  configs:
    - name: blackbox
      scrape_configs:
      - job_name: black
        metrics_path: /integrations/blackbox/metrics
        params:
          module: ["tcp_connect"]  # Look for a HTTP 200 response.
        static_configs:
          - targets:
            - 10.0.146.208:22
            - 10.0.25.46:22
        relabel_configs:
          - source_labels: [__address__]
            target_label: __param_target
          - source_labels: [__param_target]
            target_label: instance
          - target_label: __address__
            replacement: 10.0.146.208:9115  # The blackbox exporter's real hostname:port.

integrations:
  blackbox:
    enabled: true
    blackbox_targets:
      - name: 10.0.146.208
        address: 100.146.208:22
        module: tcp_connect
      - name: 10.0.25.46
        address: 10.0.25.46:22
        modules: tcp_connect
    blackbox_config:
      modules:
        tcp_connect:
          prober: tcp
          timeout: 5s
          tcp:
            preferred_ip_protocol: ipv4
                                        