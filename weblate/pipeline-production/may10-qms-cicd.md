# May10 QMS – CI tổng quát

Phạm vi ở đây chỉ là CI: kiểm tra chất lượng code, chạy test, quét bảo mật và build Docker image. Phần CD như backup, deploy, update server image và rollback không nằm trong sơ đồ này.

Nguồn cấu hình:

- `pipelines/may10-qms.yml`
- `templates/odoo-cicd.yml`
- `templates/docker-cicd.yml`

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'background': '#ffffff', 'primaryTextColor': '#111827', 'primaryBorderColor': '#64748b', 'lineColor': '#475569', 'clusterBkg': '#f8fafc', 'clusterBorder': '#94a3b8', 'fontFamily': 'Arial, sans-serif'}}}%%
flowchart TB
    EVENT["GitLab event"] --> RULE{"workflow.rules"}

    RULE -->|"Merge request"| TEST["ACTION=test<br/>Vault: DEV"]
    RULE -->|"Push dev + thay đổi .build/**"| BUILD["ACTION=build<br/>Vault: DEV"]

    subgraph INIT["Khởi tạo CI job"]
        CLONE["Clone/sync template<br/>vào .gitlab-cicd"]
        VAULT["Vault JWT auth<br/>đọc secret và export variables"]
        CLONE --> VAULT
    end

    TEST --> CLONE
    BUILD --> CLONE

    subgraph ODOO_CI["Odoo CI – runner: $TEST_RUNNER_TAG"]
        RUFF["ruff<br/>Python lint<br/>auto, blocking"]
        UNIT["unit-test<br/>Odoo + PostgreSQL Docker<br/>auto, blocking"]
        SAST["security-scan<br/>Bandit SAST<br/>manual, allow_failure"]
        RUFF ~~~ UNIT
        UNIT ~~~ SAST
    end
    TEST --> RUFF
    TEST --> UNIT
    TEST -. "manual" .-> SAST

    subgraph IMAGE_CI["Docker image CI"]
        DOCKER_BUILD["docker-build<br/>runner: $TEST_RUNNER_TAG<br/>build .build/Dockerfile<br/>push :latest + :YYYYMMDD"]
    end
    BUILD --> DOCKER_BUILD

    DISABLED["pylint<br/>ENABLE_PYLINT=false<br/>được khai báo nhưng không chạy"]
    TEST -. "disabled" .-> DISABLED

    NOTE["May10 QMS hiện bật ruff và unit-test cho ACTION=test.<br/>security-scan có thể chạy thủ công cho ACTION=test/deploy.<br/>docker-build chạy khi dev thay đổi .build/**.<br/>Không đưa các job CD vào sơ đồ này."]
    RULE -.-> NOTE

    classDef route fill:#e0f2fe,stroke:#0369a1,stroke-width:2px,color:#111827
    classDef job fill:#fef3c7,stroke:#b45309,stroke-width:1px,color:#111827
    classDef disabled fill:#f3f4f6,stroke:#6b7280,stroke-dasharray:5 5,color:#111827
    classDef note fill:#f3f4f6,stroke:#4b5563,stroke-dasharray:5 5,color:#111827

    class RULE,TEST,BUILD route
    class CLONE,VAULT,RUFF,UNIT,SAST,DOCKER_BUILD job
    class DISABLED disabled
    class NOTE note
```

## Các CI job tổng quát

| Job | Mục đích | Trạng thái trong May10 QMS |
|---|---|---|
| `ruff` | Lint Python | Bật, chạy tự động ở `ACTION=test` |
| `pylint` | Lint Python bổ sung | Tắt bởi `ENABLE_PYLINT=false` |
| `unit-test` | Chạy Odoo test trên PostgreSQL/Docker | Bật, chạy tự động ở `ACTION=test` |
| `security-scan` | Bandit SAST | Manual, `allow_failure` |
| `docker-build` | Build và push Docker image | Normal flow: push `dev` có thay đổi `.build/**` |

Các job `update-server-image`, `create-backup`, `deploy-server` và `rollback-on-upgrade-failure` là CD, nên đã loại khỏi sơ đồ này.
