# May10 QMS – CI/CD thực tế

Sơ đồ dưới đây được dựng từ `pipelines/may10-qms.yml` và hai template mà pipeline này include:

- `templates/odoo-cicd.yml`
- `templates/docker-cicd.yml`

```mermaid
flowchart TB
    EVENT["GitLab event"] --> RULE{"workflow.rules<br/>first matching rule"}

    RULE -->|"Merge request"| TEST["ACTION=test<br/>Vault: DEV"]
    RULE -->|"Push dev + thay đổi .build/**"| BUILD["ACTION=build<br/>Vault: DEV"]
    RULE -->|"Push dev + không thay đổi .build/**"| DEV["ACTION=deploy<br/>Vault: DEV"]
    RULE -->|"Push production"| PROD["ACTION=deploy<br/>Vault: PROD"]
    RULE -->|"Run pipeline từ Web"| WEB["Pipeline được tạo<br/>workflow không tự set ACTION/VAULT_SECRET_PATHS"]

    subgraph INIT["Khởi tạo ở các job có chạy"]
        CLONE["Clone/sync infra/cicd-pipeline-template<br/>vào .gitlab-cicd"]
        VAULT["Vault JWT auth<br/>đọc secret paths và export biến môi trường"]
        CLONE --> VAULT
    end

    TEST --> CLONE
    BUILD --> CLONE
    DEV --> CLONE
    PROD --> CLONE

    subgraph MR["MR test – runner: $TEST_RUNNER_TAG"]
        RUFF_T["ruff<br/>auto, blocking"]
        UNIT_T["unit-test<br/>auto, blocking"]
        SAST_T["security-scan / Bandit<br/>manual, allow_failure"]
        RUFF_T ~~~ UNIT_T
        UNIT_T ~~~ SAST_T
    end
    TEST --> RUFF_T
    TEST --> UNIT_T
    TEST -.-> SAST_T

    subgraph DOCKER["Dev image build"]
        DBUILD["docker-build<br/>runner: $TEST_RUNNER_TAG<br/>build .build/Dockerfile<br/>push :latest + :YYYYMMDD"]
        UPDATE_DEV["update-server-image-dev<br/>runner: may10-dev-runner<br/>pull image, docker compose down/up"]
        DBUILD --> UPDATE_DEV
    end
    BUILD --> DBUILD

    subgraph DEV_DEPLOY["Dev Odoo deploy – runner: may10-dev-runner"]
        BACKUP_DEV["create-backup-dev"]
        BDEV_DETAIL["lock HTTP config<br/>pg_dump + filestore.tar<br/>zip vào SERVER_DEPLOY_PATH/backup<br/>restart Odoo + emit build.env"]
        DEPLOY_DEV["deploy-server-dev"]
        DDEV_DETAIL["checkout CI_COMMIT_SHA<br/>diff addon với SAVED_HEAD_SHA<br/>update/init addon, restart Odoo"]
        ROLLBACK_DEV["rollback-on-upgrade-failure-dev<br/>when: on_failure"]
        RESTORE_DEV["checkout SAVED_HEAD_SHA<br/>restore DB + filestore + config<br/>up Odoo + notify"]
        BACKUP_DEV --> BDEV_DETAIL --> DEPLOY_DEV --> DDEV_DETAIL
        DEPLOY_DEV -. "deploy fail" .-> ROLLBACK_DEV --> RESTORE_DEV
        BACKUP_DEV -. "backup artifact / dotenv" .-> ROLLBACK_DEV
    end
    DEV --> BACKUP_DEV

    subgraph PROD_DEPLOY["Production Odoo deploy – runner: may10-qms-prod-runner"]
        BACKUP_PROD["create-backup-prod"]
        BPROD_DETAIL["lock HTTP config<br/>pg_dump + filestore.tar<br/>zip vào SERVER_DEPLOY_PATH/backup<br/>restart Odoo + emit build.env"]
        DEPLOY_PROD["deploy-server-prod"]
        DPROD_DETAIL["checkout CI_COMMIT_SHA<br/>diff addon với SAVED_HEAD_SHA<br/>update/init addon, restart Odoo"]
        ROLLBACK_PROD["rollback-on-upgrade-failure-prod<br/>when: on_failure"]
        RESTORE_PROD["checkout SAVED_HEAD_SHA<br/>restore DB + filestore + config<br/>up Odoo + notify"]
        BACKUP_PROD --> BPROD_DETAIL --> DEPLOY_PROD --> DPROD_DETAIL
        DEPLOY_PROD -. "deploy fail" .-> ROLLBACK_PROD --> RESTORE_PROD
        BACKUP_PROD -. "backup artifact / dotenv" .-> ROLLBACK_PROD
    end
    PROD --> BACKUP_PROD

    DEV -. "security-scan manual, không phải gate" .-> SAST_D["security-scan / Bandit"]
    PROD -. "security-scan manual, không phải gate" .-> SAST_P["security-scan / Bandit"]

    NOTE["May10 QMS hiện override ruff/unit-test chỉ chạy ACTION=test;<br/>deploy dev/prod không có unit-test tự động.<br/>update-server-image-prod chỉ chạy ACTION=build,<br/>nhưng push production đang set ACTION=deploy."]
    PROD -.-> NOTE

    classDef route fill:#e0f2fe,stroke:#0369a1,stroke-width:2px
    classDef job fill:#fef3c7,stroke:#b45309,stroke-width:1px
    classDef deploy fill:#dcfce7,stroke:#15803d,stroke-width:1px
    classDef recovery fill:#fee2e2,stroke:#b91c1c,stroke-width:1px
    classDef note fill:#f3f4f6,stroke:#4b5563,stroke-dasharray:5 5

    class RULE,TEST,BUILD,DEV,PROD,WEB route
    class CLONE,VAULT,DBUILD,UPDATE_DEV,RUFF_T,UNIT_T,SAST_T,SAST_D,SAST_P job
    class BACKUP_DEV,BDEV_DETAIL,DEPLOY_DEV,DDEV_DETAIL,BACKUP_PROD,BPROD_DETAIL,DEPLOY_PROD,DPROD_DETAIL deploy
    class ROLLBACK_DEV,RESTORE_DEV,ROLLBACK_PROD,RESTORE_PROD recovery
    class NOTE note
```

## Đọc nhanh

- Merge request: `ruff` và `unit-test` chạy trên Docker runner; Bandit là manual và cho phép fail.
- Push `dev` có thay đổi `.build/**`: build/push image rồi update server image trên dev.
- Push `dev` không thay đổi `.build/**`: backup dev → deploy dev; deploy lỗi thì rollback.
- Push `production`: backup prod → deploy prod; deploy lỗi thì rollback.
- `pylint` bị tắt (`ENABLE_PYLINT=false`).
- Backup hiện được tạo local ở `SERVER_DEPLOY_PATH/backup` và truyền đường dẫn qua dotenv; trong code pipeline hiện tại không có bước upload MinIO.

## Các điểm cần lưu ý khi đối chiếu README cũ

README tổng quát đang mô tả `integration-test`, MinIO và chuỗi `ruff → unit-test → integration-test`, nhưng cấu hình hiện tại của `may10-qms` không triển khai integration-test và override deploy thành `backup → deploy`. `unit-test` cũng có `needs: []`, nên khi nó được bật thì chạy độc lập, không chờ `ruff`.